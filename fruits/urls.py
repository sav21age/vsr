from django.urls import path
from fruits.views import FruitProductDetail, FruitProductList, filter_form


urlpatterns = (
    path('',
        FruitProductList.as_view(), name='list'),
    path('filter-form/', filter_form, name='filter_form'),
    path('<slug:slug>/',
         FruitProductDetail.as_view(), name='detail'),
)