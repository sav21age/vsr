from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from carts.models import Cart
from orders.models import Order
from profiles.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'профиль пользователя'
    verbose_name_plural = 'профиль пользователя'


class CartInline(admin.TabularInline):
    model=Cart
    extra = 0
    # show_change_link = True
    fields = ('get_cart_link', )
    readonly_fields = ('get_cart_link', )
    verbose_name = 'Корзина'
    verbose_name_plural = 'Корзина'

    @mark_safe
    def get_cart_link(self, obj):
        if obj.id:
            url = reverse('admin:carts_cart_change', args=(obj.id,))
            return f'<a href="{url}" rel="noopener noreferrer">Посмотреть</a>'
        return '-'
    get_cart_link.short_description = ''

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    

class OrderInline(admin.TabularInline):
    model=Order
    extra = 0
    # show_change_link = True
    fields = ('get_order_link', 'created_at', )
    readonly_fields = ('number', 'get_order_link', 'created_at', )

    @mark_safe
    def get_order_link(self, obj):
        url = reverse('admin:orders_order_change', args=(obj.id,))
        return f'<a href="{url}" rel="noopener noreferrer">{obj.number}</a>'
    get_order_link.short_description = 'Номер заказа'

    def has_add_permission(self, request, obj=None):
        return False
    

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, CartInline, OrderInline)
    save_on_top = True


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
