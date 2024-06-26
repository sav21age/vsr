from django.views.generic import ListView
from catalog.models import CatalogItem


class CatalogItemList(ListView):
    model = CatalogItem
    template_name = 'catalog/index.html'
    queryset = CatalogItem.is_visible_objects.all()
