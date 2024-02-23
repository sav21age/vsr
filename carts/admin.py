from django.contrib import admin
from carts.models import Cart, CartItem
from django.contrib.contenttypes.admin import GenericStackedInline
from common.helpers import get_price_properties

class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 0
    # show_change_link = True
    fields = ('product', 'quantity', 'price', 'total_price')
    readonly_fields = ('product', 'price', 'total_price', )

    def has_add_permission(self, request, obj=None):
        return False

    # def get_content_object(self, obj):
    #     return f"{obj.content_object.product} {get_price_properties(obj.content_object)}"
    # get_content_object.short_description = 'Товар'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # save_on_top = True
    inlines = (CartItemInline, )
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name',)
    search_help_text = 'Поиск по пользователю'
    list_display = ('get_user', 'created_at', 'get_total_price',)
    readonly_fields = ('user', 'created_at', 'get_total_price',
                       'ip', 'user_agent',)
    fieldsets = (
        ('', {
            'fields': ('user', 'created_at', 'get_total_price',)
        }),
        ('Служебные заголовки', {
            "classes": ("collapse",),
            'fields': ('ip', 'user_agent',)
        }),
    )

    def get_user(self, obj):
        if not obj.user:
            return 'Анонимный пользователь'
        return obj.user
    get_user.short_description = 'Пользователь'

    def get_total_price(self, obj):
        return f"{obj.total_price} руб."
    get_total_price.short_description = 'Общая цена'

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     extra_context = extra_context or {}

    #     # extra_context['show_save'] = False
    #     extra_context['show_save_and_continue'] = False

    #     return super().changeform_view(request, object_id, form_url, extra_context)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('get_content_object', 'quantity', 'get_price',)

#     def get_content_object(self, obj):
#         return f"{obj.content_object.product} {get_price_properties(obj.content_object)}"
#     get_content_object.short_description = 'Товар'

#     def get_price(self, obj):
#         return f"{obj.content_object.price} руб."
#     get_price.short_description = 'Цена'

#     def has_add_permission(self, request, obj=None):
#         return False
