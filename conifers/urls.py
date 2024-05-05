from django.urls import path
from conifers.views import ConiferProductDetail, ConiferProductList, filter_form

urlpatterns = (
    path('', ConiferProductList.as_view(), name='list'),
    # path('<int:genus>/', ConiferProductList.as_view(), name='list_genus'),
    # path('<int:genus>/<int:species>/',
    #      ConiferProductList.as_view(), name='list_genus_species'),
    path('filter-form/', filter_form, name='filter_form'),
    path('<slug:slug>/', ConiferProductDetail.as_view(), name='detail'),
)