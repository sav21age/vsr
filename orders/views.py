import random
# from urllib.parse import urlsplit, urlunsplit
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import FormView
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404
from carts.models import Cart, CartItem
from common.mail import send_html_email
from common.loggers import logger
from orders.models import Order, OrderItem, OrderStatus
from orders.forms import ConfirmOrderAnonymUserForm, CreateOrderAnonymUserForm, CreateOrderAuthUserForm


def send_order_email(order):
    template_subject = 'orders/email/order_user_subject.html'
    template_body = 'orders/email/order_user.html'

    order_items = OrderItem.objects.filter(order=order)

    context_subject = {}
    context_subject['order_number'] = order.number

    context_body = {}
    context_body['order'] = order
    context_body['order_items'] = order_items
    context_body['full_name'] = f"{order.customer_first_name} {order.customer_last_name}".strip(
    )

    send_html_email(
        template_subject,
        context_subject,
        template_body,
        context_body,
        settings.EMAIL_HOST_USER,
        order.customer_email
    )

    template_subject = 'orders/email/order_manager_subject.html'
    template_body = 'orders/email/order_manager.html'

    send_html_email(
        template_subject,
        context_subject,
        template_body,
        context_body,
        settings.EMAIL_HOST_USER,
        settings.EMAIL_HOST_USER
    )


def create(request):
    if request.user.is_authenticated:
        return CreateOrderAuthUserView.as_view()(request)
    return CreateOrderAnonymUserView.as_view()(request)


@method_decorator(login_required, name='dispatch')
class CreateOrderAuthUserView(FormView):
    model = Order
    template_name = 'orders/create_form.html'
    form_class = CreateOrderAuthUserForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get(self, *args, **kwargs):
        try:
            self.cart = Cart.objects.get(user=self.request.user)
            self.cart_items = CartItem.objects.filter(cart=self.cart)
        except Cart.DoesNotExist as e:
            logger.error(e)
            return redirect(reverse('carts:index'))
        except CartItem.DoesNotExist as e:
            logger.error(e)
            return redirect(reverse('carts:index'))
        except Exception as e:
            logger.error(e)
            return HttpResponse(status=500)

        if not self.cart_items.exists():
            # return HttpResponse(status=404)
            raise Http404

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['cart_items'] = self.cart_items
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user

                try:
                    cart = Cart.objects.get(user=user)
                except Exception as e:
                    logger.error(e)
                    return HttpResponse(status=500)

                cart_items = CartItem.objects.filter(cart=cart)

                if cart_items.exists():
                    customer_first_name = form.cleaned_data.get(
                        'customer_first_name', None)
                    if not customer_first_name:
                        customer_first_name = user.first_name

                    customer_last_name = form.cleaned_data.get(
                        'customer_last_name', None)
                    if not customer_last_name:
                        customer_last_name = user.last_name

                    customer_email = form.cleaned_data.get(
                        'customer_email', None)
                    if not customer_email:
                        customer_email = user.email

                    customer_phone_number = form.cleaned_data.get(
                        'customer_phone_number', None)
                    if not customer_phone_number:
                        customer_phone_number = user.profile.phone_number

                    order = Order.objects.create(
                        user=user,
                        customer_first_name=customer_first_name,
                        customer_last_name=customer_last_name,
                        customer_email=customer_email,
                        customer_phone_number=customer_phone_number,
                        customer_comment=form.cleaned_data['customer_comment'],
                        ip=cart.ip,
                        user_agent=cart.user_agent,
                        status=OrderStatus.objects.get(id=1),
                    )

                    order.number = str(order.id).rjust(8, '0')
                    order.save()

                    for cart_item in cart_items:
                        product_name = f"{cart_item.content_object.product} {cart_item.content_object.get_complex_name}"

                        OrderItem.objects.create(
                            order=order,
                            # content_type=cart_item.content_type,
                            # object_id=cart_item.object_id,
                            name=product_name,
                            price=cart_item.content_object.price,
                            quantity=cart_item.quantity,
                        )

                    send_order_email(order)

                    cart.delete()
                    cart_items.delete()

        except ValidationError:
            return redirect('carts:index')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:success')


class CreateOrderAnonymUserView(FormView):
    model = Order
    template_name = 'orders/create_form.html'
    form_class = CreateOrderAnonymUserForm

    def get(self, *args, **kwargs):
        cart_id = self.request.session.get('cart_id', None)
        try:
            self.cart = Cart.objects.get(id=cart_id)
            self.cart_items = CartItem.objects.filter(cart=self.cart)
        except Cart.DoesNotExist as e:
            logger.error(e)
            return redirect(reverse('carts:index'))
        except CartItem.DoesNotExist as e:
            logger.error(e)
            return redirect(reverse('carts:index'))
        except Exception as e:
            logger.error(e)
            return HttpResponse(status=500)

        if not self.cart_items.exists():
            # return HttpResponse(status=404)
            raise Http404

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['cart_items'] = self.cart_items
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                cart_id = self.request.session.get('cart_id', None)

                try:
                    cart = Cart.objects.get(id=cart_id)
                except Exception as e:
                    logger.error(e)
                    return HttpResponse(status=500)

                cart_items = CartItem.objects.filter(cart=cart)

                if cart_items.exists():

                    order = Order.objects.create(
                        customer_first_name=form.cleaned_data['customer_first_name'],
                        customer_last_name=form.cleaned_data['customer_last_name'],
                        customer_email=form.cleaned_data['customer_email'],
                        customer_phone_number=form.cleaned_data['customer_phone_number'],
                        customer_comment=form.cleaned_data['customer_comment'],
                        ip=cart.ip,
                        user_agent=cart.user_agent,
                        status=OrderStatus.objects.get(id=1),
                        confirm_code=random.randint(1000, 9999),
                        confirmed_by_email=False,
                    )

                    order.number = str(order.id).rjust(8, '0')
                    order.save()

                    self.request.session['order_id'] = order.id

                    for cart_item in cart_items:
                        product_name = f"{cart_item.content_object.product} {cart_item.content_object.get_complex_name}"

                        OrderItem.objects.create(
                            order=order,
                            # content_type=cart_item.content_type,
                            # object_id=cart_item.object_id,
                            name=product_name,
                            price=cart_item.content_object.price,
                            quantity=cart_item.quantity,
                        )

                    cart.delete()
                    cart_items.delete()

        except ValidationError:
            return redirect('orders:create')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:confirm')


class ConfirmOrderAnonymView(FormView):
    template_name = 'orders/confirm_form.html'
    form_class = ConfirmOrderAnonymUserForm

    def get(self, request, *args, **kwargs):

        order_id = self.request.session.get('order_id', None)
        confirm_code_sent = self.request.session.get(
            'confirm_code_sent', False)

        try:
            order = Order.objects.get(id=order_id)
        except Exception as e:
            logger.error(e)
            raise Http404 from e

        if not confirm_code_sent:
            template_subject = 'orders/email/enter_confirm_code_subject.html'
            template_body = 'orders/email/enter_confirm_code.html'

            context_subject = {}
            context_subject['order_number'] = order.number

            context_body = {}
            context_body['code'] = order.confirm_code

            send_html_email(
                template_subject,
                context_subject,
                template_body,
                context_body,
                settings.EMAIL_HOST_USER,
                order.customer_email
            )
            self.request.session['confirm_code_sent'] = True

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        order_id = self.request.session.get('order_id', None)

        try:
            order = Order.objects.get(id=order_id)
        except Exception as e:
            logger.error(e)
            raise Http404 from e

        if form.is_valid() and form.cleaned_data['confirm_code'] == order.confirm_code:
            order.confirmed_by_email = True
            order.save()

            send_order_email(order)

            request.session.pop('cart_id')
            request.session.pop('order_id')
            request.session.pop('confirm_code_sent')
            return self.form_valid(form)

        return self.form_invalid(form, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_id = self.request.session.get('order_id', None)
        try:
            order = Order.objects.get(id=order_id)
        except Exception as e:
            logger.error(e)
            raise Http404 from e

        context['email'] = order.customer_email

        return context

    def get_success_url(self):
        return reverse('orders:success')


# class SuccessOrderTemplateView(TemplateView):
#     template_name = 'orders/success.html'

#     def get(self, request, *args, **kwargs):
#         referer = request.META.get('HTTP_REFERER', None)

#         if not referer:
#             raise Http404

#         url = urlsplit(referer)
#         referer = urlunsplit(url._replace(scheme="")._replace(netloc=""))

#         if referer not in [reverse('orders:create'), reverse('orders:confirm')]:
#             raise Http404

#         return super().get(request, *args, **kwargs)
