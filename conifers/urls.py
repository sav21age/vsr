from django.urls import path
from conifers.views import ConiferProductDetail, ConiferProductList

urlpatterns = (
    path('', ConiferProductList.as_view(), name='list'),
    # path('<int:genus>/', ConiferProductList.as_view(), name='list_genus'),
    # path('<int:genus>/<int:species>/',
    #      ConiferProductList.as_view(), name='list_genus_species'),
    path('<slug:slug>/', ConiferProductDetail.as_view(), name='detail'),
)