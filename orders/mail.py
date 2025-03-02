from django.conf import settings

from common.mail import send_html_email
from orders.models import OrderItem


def send_order_email(order):
    template_subject = 'orders/email/order_user_subject.html'
    template_body = 'orders/email/order_user.html'

    order_items = OrderItem.objects.filter(order=order)

    full_name = f"{order.customer_first_name} {order.customer_last_name}".strip()

    context_subject = {}
    context_subject['order_number'] = order.number
    context_subject['full_name'] = full_name

    context_body = {}
    context_body['order'] = order
    context_body['order_items'] = order_items
    context_body['full_name'] = full_name

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
