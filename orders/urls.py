from django.urls import path
from django.views.generic import TemplateView
from orders.views import ConfirmOrderAnonymView, create


urlpatterns = [
    path('', create, name='create'),
    path('confirm/', ConfirmOrderAnonymView.as_view(), name='confirm'),
    # path('success/', SuccessOrderTemplateView.as_view(), name='success'),
    path('success/', TemplateView.as_view(
        template_name="orders/success.html"), name='success'),
]