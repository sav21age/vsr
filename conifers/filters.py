from common.filters import PlantGenusFilter, ProductGenusFilter, ProductPriceGenusFilter


class ConiferGenusFilter(PlantGenusFilter):
    division_name = 'CON'


class ConiferProductGenusFilter(ProductGenusFilter, ConiferGenusFilter):
    pass


class ConiferProductPriceGenusFilter(ProductPriceGenusFilter, ConiferGenusFilter):
    pass


# class ConiferGenusFilter(SimpleListFilter):
#     title = 'Род'
#     parameter_name = 'genus'

#     def lookups(self, request, model_admin):
#         qs = PlantGenus.objects.filter(division__name='CON')
#         return [(o.id, o.name) for o in qs]


# class ConiferProductGenusFilter(ConiferGenusFilter):
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(species__genus=self.value())
#         return queryset


# class ConiferProductPriceGenusFilter(ConiferGenusFilter):
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(product__species__genus=self.value())
#         return queryset
