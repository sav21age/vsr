from django.contrib.admin import SimpleListFilter
from plants.models import PlantGenus, PlantPriceContainer


class PlantGenusFilter(SimpleListFilter):
    title = 'Род'
    parameter_name = 'genus'
    division_name = ''

    def lookups(self, request, model_admin):
        qs = PlantGenus.objects.filter(division__name=self.division_name)
        return [(o.id, o.name) for o in qs]


class ProductGenusFilter(SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(species__genus=self.value())
        return queryset


class ProductPriceGenusFilter(SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(product__species__genus=self.value())
        return queryset


class PriceContainerFilter(SimpleListFilter):
    title = 'Контейнер'
    parameter_name = 'container'
    container = ''

    def lookups(self, request, model_admin):
        qs = PlantPriceContainer.objects.all()
        lst = [(o.id, o.name) for o in qs]
        lst.append(('None', 'Нет'))
        return lst

    def queryset(self, request, queryset):
        if self.value() == 'None':
            return queryset.filter(container__isnull=True)

        if self.value():
            return queryset.filter(container__id__exact=self.value())

        return queryset
