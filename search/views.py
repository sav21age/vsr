from django.views.generic import View
from conifers.models import ConiferProduct
from deciduous.models import DecProduct
from fruits.models import FruitProduct
from other.models import OtherProduct
from perennials.models import PerProduct
from pure_pagination import PaginationMixin
from roses.models import RoseProduct
from django.shortcuts import render
from itertools import chain


class SearchView(PaginationMixin, View):
    paginate_by = 12
    template_name = 'search/listview.html'

    def get(self, request, *args, **kwargs):
        context = {}

        q = request.GET.get('q')
        if q:
            query_sets = []  # Total QuerySet

            # Searching for all models
            query_sets.append(ConiferProduct.objects.search(query=q))
            query_sets.append(DecProduct.objects.search(query=q))
            query_sets.append(FruitProduct.objects.search(query=q))
            query_sets.append(PerProduct.objects.search(query=q))
            query_sets.append(OtherProduct.objects.search(query=q))
            query_sets.append(RoseProduct.objects.search(query=q))

            # and combine results
            final_set = list(chain(*query_sets))

            # final_set.sort(key=lambda x: x.pub_date, reverse=True)  # Sorting
            context['object_list'] = final_set
            context['q'] = self.request.GET.get('q' or None)

        return render(request=request, template_name=self.template_name, context=context)

    # def get_queryset(self):
    #     pass

    # def get_context_data(self, **kwargs):
    #     context = super(SearchView, self).get_context_data(**kwargs)
    #     context['q'] = self.request.GET.get('q' or None)
    #     return context
