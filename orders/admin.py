from django.contrib import admin
from django.conf import settings
# from django.utils.safestring import mark_safe
from common.mail import send_html_email
from orders.models import Order, OrderItem, OrderStatus


admin.site.register(OrderStatus)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('name', 'quantity', 'price', 'total_price')
    readonly_fields = ('name', 'price', 'quantity', 'total_price', )
    template = 'orders/admin/tabular.html'

    def has_add_permission(self, request, obj=None):
        return False



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = (OrderItemInline, )
    
    search_fields = ('number', 'customer_first_name', 'customer_email',)
    search_help_text = 'Поиск по номеру заказа, имени и эл. почты заказчика'

    readonly_fields = ('number', 'user', 'get_user', 'customer_first_name', 'customer_last_name', 'customer_email', 
                       'customer_phone_number', 'customer_comment', 'created_at', 'get_created_at', 'get_total_price',
                       'ip', 'user_agent',)

    list_display = ('number', 'status', 'customer_email',
                    'customer_first_name', 'get_created_at', 'get_total_price',)
    
    list_filter = ('status',)

    fieldsets = (
        ('Заказ', {
            'fields': ('number', 'status', 'status_change_email', 'customer_comment', 'created_at', 'get_total_price',)
        }),
        ('Заказчик', {
            'fields': ('get_user', 'customer_first_name', 'customer_last_name', 'customer_email', 'customer_phone_number', )
        }),
        ('Служебная информация', {
            "classes": ("collapse",),
            'fields': ('ip', 'user_agent',)
        }),
    )

    def get_user(self, obj):
        if obj.user:
            return True
        return False
    get_user.short_description = 'Зарегистрированный пользователь'
    get_user.boolean = True

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d.%m.%Y")
    get_created_at.short_description = 'Дата'
    
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
    
    def has_add_permission(self, request, obj=None):
        return False

    # @mark_safe
    # def get_confirmed_by_email(self, obj):
    #     if obj.confirmed_by_email is None:
    #         return 'не требуется'
    #     if obj.confirmed_by_email:
    #         return '<span style="color: green;">да</span>'
    #     return '<span style="color: red;">нет</span>'
    # get_confirmed_by_email.short_description = 'Подтвержден по эл. почте'
    # get_confirmed_by_email.boolean = True

    # def get_fieldsets(self, request, obj=None):
    #     # fieldsets = super().get_fieldsets(request, obj)
    #     anonym_fieldsets = (
    #         ('Подтверждение заказа анонимным пользователем', {
    #             # "classes": ("collapse",),
    #             'fields': ('confirm_code', 'confirmed_by_email',)
    #         }),
    #     )

    #     user_fieldsets = (
    #         ('', {
    #             'fields': ('number', 'status', 'status_change_email',
    #                        'customer_first_name', 'customer_last_name', 'customer_email', 'customer_phone_number', 'customer_comment',
    #                        'user', 'created_at', 'get_total_price',)
    #         }),
    #         ('Служебная информация', {
    #             "classes": ("collapse",),
    #             'fields': ('ip', 'user_agent',)
    #         }),
    #     )

    #     if obj.user:
    #         return user_fieldsets
    #     return anonym_fieldsets + user_fieldsets

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     extra_context = extra_context or {}

    #     # extra_context['show_save'] = True
    #     extra_context['show_save_and_continue'] = False

    #     return super().changeform_view(request, object_id, form_url, extra_context)

    # def has_delete_permission(self, request, obj=None):
    #     return False
