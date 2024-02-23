from django.urls import path
from perennials.views import PerProductDetail, PerProductList


urlpatterns = (
    path('', PerProductList.as_view(), name='list'),
    path('<int:genus>/', PerProductList.as_view(), name='list_genus'),
    path('<int:genus>/<int:species>/', PerProductList.as_view(), name='list_genus_species'),
    path('<slug:slug>/', PerProductDetail.as_view(), name='detail'),
)