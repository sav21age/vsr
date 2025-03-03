from django.urls import path
from carts.views import CartView, cart_add, cart_remove, cart_update

app_name = 'carts'

urlpatterns = [
    path('', CartView.as_view(), name='index'),
    path('add/', cart_add, name='add'),
    path('update/', cart_update, name='update'),
    path('remove/', cart_remove, name='remove'),
]