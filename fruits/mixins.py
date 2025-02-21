from fruits.forms import FruitProductPriceFilterForm


class FruitFilterFormMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()

        form = FruitProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data

            if clean['genus']:
                id_list = list(clean['genus'].values_list('id', flat=True))
                qs = qs.filter(species__genus__in=id_list)

            if clean['container']:
                qs = qs.filter(prices__container=clean['container'])

            if clean['rs']:
                qs = qs.filter(prices__rs=clean['rs'])

            if clean['age']:
                qs = qs.filter(prices__age=clean['age'])

            return qs.distinct()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = FruitProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data
            context['form'] = FruitProductPriceFilterForm(
                initial={
                    'genus': clean['genus'],
                    'container': clean['container'],
                    'rs': clean['rs'],
                    'age': clean['age'],

                    'per_page': clean['per_page'],
                },
            )
        else:
            context['form'] = FruitProductPriceFilterForm()
        return context
