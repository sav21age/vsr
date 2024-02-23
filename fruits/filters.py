from common.filters import PlantGenusFilter, ProductGenusFilter, ProductPriceGenusFilter


class FruitGenusFilter(PlantGenusFilter):
    division_name = 'FRU'


class FruitProductGenusFilter(ProductGenusFilter, FruitGenusFilter):
    pass


class FruitProductPriceGenusFilter(ProductPriceGenusFilter, FruitGenusFilter):
    pass
