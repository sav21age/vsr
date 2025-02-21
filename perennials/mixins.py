
from perennials.forms import (PerProductPriceFilterForm)


class PerFilterFormMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()

        form = PerProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data

            if clean['genus']:
                id_list = list(clean['genus'].values_list('id', flat=True))
                qs = qs.filter(species__genus__in=id_list)

            if clean['container']:
                qs = qs.filter(prices__container=clean['container'])

            if clean['planting_year']:
                qs = qs.filter(prices__planting_year=clean['planting_year'])

            return qs.distinct()
        # else:
        #     print(form.errors)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = PerProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data
            context['form'] = PerProductPriceFilterForm(
                initial={
                    'genus': clean['genus'],
                    'container': clean['container'],
                    'planting_year': clean['planting_year'],

                    'per_page': clean['per_page'],
                },
            )
        else:
            context['form'] = PerProductPriceFilterForm()
        return context
