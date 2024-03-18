from itertools import chain
from django.shortcuts import render
from django.views.generic import ListView
from conifers.models import ConiferProduct
from deciduous.models import DecProduct
from fruits.models import FruitProduct
from other.models import OtherProduct
from perennials.models import PerProduct
from roses.models import RoseProduct
from pure_pagination.mixins import PaginationMixin


class SearchView(PaginationMixin, ListView):
    paginate_by = 12
    template_name = 'search/list.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        
        if q:
            query_sets = []

            query_sets.append(
                ConiferProduct.objects.search(query=q) \
                    .filter(is_visible=True) \
                    .select_related('species') \
                    .prefetch_related('images') \
                    .prefetch_related('coniferproductprice_set')
            )
            
            query_sets.append(
                DecProduct.objects.search(query=q) \
                    .select_related('species') \
                    .prefetch_related('images') \
                    .prefetch_related('decproductprice_set')
            )

            query_sets.append(
                FruitProduct.objects.search(query=q) \
                    .select_related('species') \
                    .prefetch_related('images') \
                    .prefetch_related('fruitproductprice_set')
            )

            query_sets.append(
                PerProduct.objects.search(query=q) \
                    .select_related('species') \
                    .prefetch_related('images') \
                    .prefetch_related('perproductprice_set')
            )

            query_sets.append(
                OtherProduct.objects.search(query=q) \
                    .prefetch_related('images') \
                    .prefetch_related('otherproductprice_set')
            )
            
            query_sets.append(
                RoseProduct.objects.search(query=q) \
                    .prefetch_related('images') \
                    .prefetch_related('roseproductprice_set')
            )

            return list(chain(*query_sets))

        return []
    
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q' or None)
        return context


    # def get(self, request, *args, **kwargs):
    #     context = {}

    #     q = request.GET.get('q')
    #     if q:
    #         query_sets = []  # Total QuerySet

    #         # Searching for all models
    #         query_sets.append(
    #             ConiferProduct.objects.search(query=q) \
    #                 .filter(is_visible=True) \
    #                 .select_related('species') \
    #                 .prefetch_related('images') \
    #                 .prefetch_related('coniferproductprice_set')
    #         )

    #         query_sets.append(
    #             DecProduct.objects.search(query=q) \
    #                 .select_related('species') \
    #                 .prefetch_related('images') \
    #                 .prefetch_related('decproductprice_set')
    #         )

    #         query_sets.append(
    #             FruitProduct.objects.search(query=q) \
    #                 .select_related('species') \
    #                 .prefetch_related('images') \
    #                 .prefetch_related('fruitproductprice_set')
    #         )

    #         query_sets.append(
    #             PerProduct.objects.search(query=q) \
    #                 .select_related('species') \
    #                 .prefetch_related('images') \
    #                 .prefetch_related('perproductprice_set')
    #         )

    #         query_sets.append(
    #             OtherProduct.objects.search(query=q) \
    #                 .prefetch_related('images') \
    #                 .prefetch_related('otherproductprice_set')
    #         )

    #         query_sets.append(
    #             RoseProduct.objects.search(query=q) \
    #                 .prefetch_related('images') \
    #                 .prefetch_related('roseproductprice_set')
    #         )

    #         # and combine results
    #         final_set = list(chain(*query_sets))

    #         # final_set.sort(key=lambda x: x.pub_date, reverse=True)  # Sorting
    #         context['object_list'] = final_set
    #         context['q'] = self.request.GET.get('q' or None)

    #     return render(request=request, template_name=self.template_name, context=context)
