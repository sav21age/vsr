from conifers.forms import ConiferProductPriceFilterForm


class ConiferFilterFormMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()

        form = ConiferProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data

            if clean['genus']:
                id_list = list(clean['genus'].values_list('id', flat=True))
                qs = qs.filter(species__genus__in=id_list)

            if clean['height_from']:
                qs = qs.filter(prices__height_from__gte=clean['height_from'])

            if clean['width_from']:
                qs = qs.filter(
                    prices__width_from__gte=clean['width_from'])

            if clean['container']:
                qs = qs.filter(prices__container=clean['container'])

            if clean['rs']:
                qs = qs.filter(prices__rs=clean['rs'])

            if clean['shtamb']:
                qs = qs.filter(prices__shtamb__regex=r"\S")
                # qs = qs.filter(~Q(prices__shtamb=''))

            if clean['extra']:
                qs = qs.filter(prices__extra=True)

            return qs.distinct()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = ConiferProductPriceFilterForm(self.request.GET)
        if form.is_valid():
            clean = form.cleaned_data
            context['form'] = ConiferProductPriceFilterForm(
                initial={
                    'genus': clean['genus'],
                    'height_from': clean['height_from'],
                    'width_from': clean['width_from'],
                    'container': clean['container'],
                    'rs': clean['rs'],
                    'shtamb': clean['shtamb'],
                    'extra': clean['extra'],

                    'per_page': clean['per_page'],
                },
            )
        else:
            context['form'] = ConiferProductPriceFilterForm()
        return context
