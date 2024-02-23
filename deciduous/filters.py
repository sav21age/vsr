from common.filters import PlantGenusFilter, ProductGenusFilter, ProductPriceGenusFilter


class DecGenusFilter(PlantGenusFilter):
    division_name = 'DEC'


class DecProductGenusFilter(ProductGenusFilter, DecGenusFilter):
    pass


class DecProductPriceGenusFilter(ProductPriceGenusFilter, DecGenusFilter):
    pass
