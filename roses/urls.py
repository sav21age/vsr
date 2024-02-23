from django.urls import path
from roses.views import RoseProductDetail, RoseProductList


urlpatterns = (
    path('',
        RoseProductList.as_view(), name='list'),
    path('<slug:slug>/',
         RoseProductDetail.as_view(), name='detail'),
)