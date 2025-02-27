from django.views.generic import ListView, DetailView
from common.mixins import PerPageMixin
from other.models import OtherProduct
from pure_pagination.mixins import PaginationMixin


class CategoryFilterMixin():
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(category__name=self.category) \
            .select_related('category') \
            .prefetch_related('images') \
            .prefetch_related('prices')
        return qs


class BookProductList(PaginationMixin, PerPageMixin, CategoryFilterMixin, ListView):
    model = OtherProduct
    template_name = 'other/book_list.html'
    category = 'BOOK'
    queryset = OtherProduct.is_visible_objects.all()


class BookProductDetail(CategoryFilterMixin, DetailView):
    model = OtherProduct
    template_name = 'other/detail.html'
    category = 'BOOK'
    queryset = OtherProduct.is_visible_objects.all()


class RelatedProductList(PaginationMixin, PerPageMixin, CategoryFilterMixin, ListView):
    model = OtherProduct
    template_name = 'other/related_list.html'
    category = 'RELATED'
    queryset = OtherProduct.is_visible_objects.all()


class RelatedProductDetail(CategoryFilterMixin, DetailView):
    model = OtherProduct
    category = 'RELATED'
    template_name = 'other/detail.html'
    queryset = OtherProduct.is_visible_objects.all()