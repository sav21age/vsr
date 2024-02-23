from django.urls import path
from carts.views import IndexView, cart_add, cart_remove, cart_update

app_name = 'carts'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add/', cart_add, name='add'),
    path('update/', cart_update, name='update'),
    path('remove/', cart_remove, name='remove'),
]