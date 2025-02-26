from django.contrib import admin
from adminsortable2.admin import SortableAdminBase
from sales.forms import DiscountAdminForm, PromotionAdminForm
from sales.models import Discount, Promotion, PromotionItem
from common.helpers import formfield_overrides
from images.admin import ImageInline


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    formfield_overrides = formfield_overrides
    form = DiscountAdminForm


class PromotionItemInline(admin.StackedInline):
    model = PromotionItem
    extra = 0
    show_change_link = True
    formfield_overrides = formfield_overrides
    min_num = 1

@admin.register(Promotion)
class PromotionAdmin(SortableAdminBase, admin.ModelAdmin):
    save_on_top = True
    inlines = [PromotionItemInline, ImageInline,]
    formfield_overrides = formfield_overrides
    form = PromotionAdminForm
    

# @admin.register(Discount)
# class DiscountAdmin(SortableAdminBase, admin.ModelAdmin):
#     save_on_top = True
#     inlines = [ImageInline,]
#     formfield_overrides = formfield_overrides
#     form = DiscountAdminForm
    

# class PromotionItemInline(admin.StackedInline):
#     model = PromotionItem
#     extra = 0
#     show_change_link = True
#     formfield_overrides = formfield_overrides


# @admin.register(Promotion)
# class PromotionAdmin(SortableAdminBase, admin.ModelAdmin):
#     save_on_top = True
#     inlines = [PromotionItemInline, ImageInline,]
#     formfield_overrides = formfield_overrides
#     form = PromotionAdminForm
