from django import template

from carts.models import Cart, CartItem


register = template.Library()


@register.simple_tag(takes_context=True)
def get_cart_quantity(context):
    request = context['request']
    
    cart = None

    if not request.session.session_key:
        request.session.create()

    cart_id = request.session.get('cart_id')

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        elif cart_id:
            cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        pass

    if cart:
        return cart.total_quantity

    return 0
