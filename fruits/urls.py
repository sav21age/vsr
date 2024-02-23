from django.urls import path
from fruits.views import FruitProductDetail, FruitProductList


urlpatterns = (
    path('',
        FruitProductList.as_view(), name='list'),
    path('<slug:slug>/',
         FruitProductDetail.as_view(), name='detail'),
)