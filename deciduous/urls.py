from django.urls import path
from deciduous.views import DecProductDetail, DecProductList, filter_form


urlpatterns = (
    path('',
        DecProductList.as_view(), name='list'),
    path('filter-form/', filter_form, name='filter_form'),
    path('<slug:slug>/',
        DecProductDetail.as_view(), name='detail'),
)