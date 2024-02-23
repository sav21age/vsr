from common.filters import PlantGenusFilter, ProductGenusFilter, ProductPriceGenusFilter


class PerGenusFilter(PlantGenusFilter):
    division_name = 'PER'


class PerProductGenusFilter(ProductGenusFilter, PerGenusFilter):
    pass


class PerProductPriceGenusFilter(ProductPriceGenusFilter, PerGenusFilter):
    pass
