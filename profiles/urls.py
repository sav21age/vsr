from django.urls import path
from profiles.views import (
    ProfileFavorites, ProfileIndex, ProfileOrderDetail, 
    ProfileOrderList, profile_update)


urlpatterns = (
    path('', ProfileIndex.as_view(), name='index'),
    path('update/', profile_update, name='update'),
    path('orders/', ProfileOrderList.as_view(), name='order_list'),
    path('order/<int:pk>/', ProfileOrderDetail.as_view(), name='order_detail'),
    path('favorites/', ProfileFavorites.as_view(), name='favorites'),
)