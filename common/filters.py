from django.contrib.admin import SimpleListFilter
from plants.models import PlantGenus


class PlantGenusAdminFilter(SimpleListFilter):
    title = 'Род'
    parameter_name = 'genus'
    division_name = ''

    def lookups(self, request, model_admin):
        qs = PlantGenus.objects.filter(division__name=self.division_name)
        return [(o.id, o.name) for o in qs]


class ProductGenusAdminFilter(PlantGenusAdminFilter):
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(species__genus=self.value())
        return queryset


class ProductPriceGenusAdminFilter(PlantGenusAdminFilter):
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(product__species__genus__exact=self.value())
        return queryset


class SpeciesGenusAdminFilter(PlantGenusAdminFilter):
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(genus=self.value())
        return queryset


class ProductPriceContainerAdminFilter(SimpleListFilter):
    title = 'Контейнер'
    parameter_name = 'container'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(container__id__exact=self.value())

        return queryset



# class PriceContainerFilter(SimpleListFilter):
#     title = 'Контейнер'
#     parameter_name = 'container'
#     container = ''

#     def lookups(self, request, model_admin):
#         qs = PlantPriceContainer.objects.all()
#         lst = [(o.id, o.name) for o in qs]
#         lst.append(('None', 'Нет'))
#         return lst

#     def queryset(self, request, queryset):
#         if self.value() == 'None':
#             return queryset.filter(container__isnull=True)

#         if self.value():
#             return queryset.filter(container__id__exact=self.value())

#         return queryset
