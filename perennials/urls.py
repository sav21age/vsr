from django.urls import path
from perennials.views import PerProductDetail, PerProductList, filter_form


urlpatterns = (
    path('', PerProductList.as_view(), name='list'),
    # path('<int:genus>/', PerProductList.as_view(), name='list_genus'),
    # path('<int:genus>/<int:species>/', PerProductList.as_view(), name='list_genus_species'),
    path('filter-form/', filter_form, name='filter_form'),
    path('<slug:slug>/', PerProductDetail.as_view(), name='detail'),
)