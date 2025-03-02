import json
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from carts.models import Cart, CartItem
from common.loggers import logger


@method_decorator(never_cache, name='dispatch')
class CartView(View):
    template_name = 'carts/index.html'

    def get(self, request, *args, **kwargs):
        context = {}

        cart = None
        cart_items = None

        if not request.session.session_key:
            request.session.create()

        cart_id = request.session.get('cart_id', None)

        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                request.session['cart_id'] = cart.id
            except Cart.DoesNotExist:
                if cart_id:
                    try:
                        cart = Cart.objects.get(id=cart_id)
                        cart.user = request.user
                        cart.save()
                    except Cart.DoesNotExist as e:
                        logger.error(e)
        else:
            if cart_id:
                try:
                    cart = Cart.objects.get(id=cart_id)
                except Cart.DoesNotExist as e:
                    logger.error(e)

        if cart:
            cart_items = CartItem.objects.filter(cart=cart) \
                .prefetch_related('content_object')

        context['cart'] = cart
        context['cart_items'] = cart_items

        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return f"{ip}"


def cart_add(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
        raise Http404

    if request.POST.get('id') and (request.POST.get('id')).isdigit():
        object_id = request.POST.get('id')
    else:
        return HttpResponse(status=404)

    try:
        content_type = ContentType.objects.get_for_id(
            request.POST.get('ct_id'))
    except:
        return HttpResponse(status=404)

    try:
        content_type.get_object_for_this_type(pk=object_id)
    except:
        return HttpResponse(status=404)

    defaults = {
        'ip': get_ip(request),
        'user_agent': request.headers.get('User-Agent'),
    }

    if request.user.is_authenticated:
        try:
            cart, _ = Cart.objects.get_or_create(
                user=request.user,
                defaults=defaults,
            )
        except Exception as e:
            logger.error(e)

    else:
        if not request.session.session_key:
            request.session.create()

        cart_id = request.session.get('cart_id', None)

        if cart_id:
            try:
                cart, _ = Cart.objects.get_or_create(
                    id=cart_id,
                    defaults=defaults,
                )
            except Exception as e:
                logger.error(e)

        else:
            cart = Cart(**defaults)
            cart.save()

    request.session['cart_id'] = cart.id
    
    try:
        cart_item = CartItem.objects.get(
            cart=cart, content_type=content_type, object_id=object_id,)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            cart=cart, content_type=content_type, object_id=object_id, )

    response = {
        'cart': {'total_quantity': cart.total_quantity},
        # 'total_quantity': cart.total_quantity,
    }

    return HttpResponse(json.dumps(response))


def cart_update(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
        raise Http404

    cart_item_id = request.POST.get('ci_id')
    if not cart_item_id or not cart_item_id.isdigit():
        return HttpResponse(status=404)

    value = request.POST.get('value')
    if value not in ('+', '-'):
        return HttpResponse(status=404)
    
    if not request.session.session_key:
        request.session.create()

    cart_id = request.session.get('cart_id', None)

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(id=cart_id)
    except Exception as e:
        logger.error(e)
        return HttpResponse(status=500)

    try:
        cart_item = CartItem.objects.get(
            cart=cart, id=cart_item_id)
        
        if value == '+':
            cart_item.quantity += 1
        else:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
    
        cart_item.save()
    except CartItem.DoesNotExist as e:
        logger.info(e)
    
    cart_items = CartItem.objects.filter(cart=cart) \
        .prefetch_related('content_object')

    template = render_to_string(
        "carts/cart.html", {
            'cart': cart,
            'cart_items': cart_items
        },
        request=request
    )

    response = {
        # 'total_quantity': cart.total_quantity,
        'cart': {
            'total_quantity': cart.total_quantity,
            },
        'template': template,
    }

    # return JsonResponse(response_data)
    return HttpResponse(json.dumps(response, ensure_ascii=False, default=str))


def cart_remove(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
        raise Http404

    cart_item_id = request.POST.get('ci_id')
    if not cart_item_id or not cart_item_id.isdigit():
        return HttpResponse(status=404)

    if not request.session.session_key:
        request.session.create()

    cart_id = request.session.get('cart_id', None)

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist as e:
        logger.error(e)
        return HttpResponse(status=500)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist as e:
        logger.info(e)

    cart_items = CartItem.objects.filter(cart=cart)

    template = render_to_string(
        "carts/cart.html", {
            'cart': cart,
            'cart_items': cart_items
        },
        request=request
    )

    response_data = {
        'cart': {
            'total_quantity': cart.total_quantity,
        },
        "template": template,
    }

    return JsonResponse(response_data)
