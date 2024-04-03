from django.contrib import admin
from django.conf import settings
from common.mail import send_html_email
from orders.models import Order, OrderItem, OrderStatus


admin.site.register(OrderStatus)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # show_change_link = True
    fields = ('name', 'quantity', 'price', 'total_price')
    readonly_fields = ('name', 'price', 'quantity', 'total_price', )

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = (OrderItemInline, )
    search_fields = ('number', 'user__username', 'user__email',
                     'user__first_name', 'user__last_name',)
    search_help_text = 'Поиск по пользователю'
    list_display = ('number', 'status', 'get_user', 'confirmed_by_email', 'created_at', 'get_total_price',)
    readonly_fields = ('number', 'user', 'customer_first_name', 'customer_last_name', 'customer_email', 'customer_phone_number', 'customer_comment', 'created_at', 'get_total_price',
                       'confirm_code', 'confirmed_by_email', 
                       'ip', 'user_agent',)
    
    list_filter = ('status',)

    def get_fieldsets(self, request, obj=None):
        # fieldsets = super().get_fieldsets(request, obj)
        anonym_fieldsets = (
            ('Подтверждение заказа анонимным пользователем', {
                # "classes": ("collapse",),
                'fields': ('confirm_code', 'confirmed_by_email',)
            }),
        )

        user_fieldsets = (
            ('', {
                'fields': ('number', 'status', 'status_change_email', 
                           'customer_first_name', 'customer_last_name', 'customer_email', 'customer_phone_number', 'customer_comment', 
                           'user', 'created_at', 'get_total_price',)
            }),
            ('Служебная информация', {
                "classes": ("collapse",),
                'fields': ('ip', 'user_agent',)
            }),
        )

        if obj.user:
            return user_fieldsets
        return anonym_fieldsets + user_fieldsets

    def get_user(self, obj):
        if not obj.user:
            return 'Анонимный пользователь'
        return obj.user
    get_user.short_description = 'Пользователь'

    def get_total_price(self, obj):
        return f"{obj.total_price} руб."
    get_total_price.short_description = 'Общая цена'

    def save_model(self, request, obj, form, change):
        if 'status_change_email' in form.changed_data:
            order = obj
            template_subject = 'orders/email/change_order_status_subject.html'
            template_body = 'orders/email/change_order_status.html'

            order_items = OrderItem.objects.filter(order=order)

            context_subject = {}
            context_subject['order_number'] = order.id

            context_body = {}
            context_body['order'] = order
            context_body['order_items'] = order_items
            context_body['full_name'] = f"{order.customer_first_name} {order.customer_last_name}".strip()

            send_html_email(
                template_subject,
                context_subject,
                template_body,
                context_body,
                settings.EMAIL_HOST_USER,
                order.customer_email
            )

            obj.status_change_email = False
            # obj.save()

        return super().save_model(request, obj, form, change)

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     extra_context = extra_context or {}

    #     # extra_context['show_save'] = True
    #     extra_context['show_save_and_continue'] = False

    #     return super().changeform_view(request, object_id, form_url, extra_context)

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
