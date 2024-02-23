from django.urls import path
from deciduous.views import DecProductDetail, DecProductList


urlpatterns = (
    path('',
        DecProductList.as_view(), name='list'),
    path('<slug:slug>/',
        DecProductDetail.as_view(), name='detail'),
)