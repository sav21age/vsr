from common.forms import ProductAdminForm
from other.models import OtherProduct


class OtherProductAdminForm(ProductAdminForm):
    class Meta(ProductAdminForm.Meta):
        model = OtherProduct
        exclude = []
