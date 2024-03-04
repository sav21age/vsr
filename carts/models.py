from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from common.helpers import get_price_properties


# class CartManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset() \
#             .select_related('user')
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True,
                             related_name='cart', verbose_name='Пользователь',)

    ip = models.CharField(
        'IP адрес', max_length=39, blank=True, )
    user_agent = models.TextField('user agent', blank=True, null=True)

    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('дата обновления', auto_now=True)

    # objects = CartManager()

    def __str__(self):
        if self.user:
            return f"{self.user}"
        return f"Анонимный пользователь - {self.session_key}"

    @property
    def total_price(self):
        total_price = sum(item.total_price for item in self.cart_items.all())
        return total_price

    @property
    def total_quantity(self):
        total_quantity = sum(
            item.total_quantity for item in self.cart_items.all())
        return total_quantity

    class Meta:
        ordering = ('updated_at',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             related_name='cart_items', verbose_name='корзина',)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type', 'object_id',)

    quantity = models.PositiveIntegerField(
        default=1, verbose_name='Количество', db_index=True, )

    @property
    def total_price(self):
        total_price = self.content_object.price * self.quantity
        return total_price
    total_price.fget.short_description = 'Сумма, руб.'

    @property
    def total_quantity(self):
        return self.quantity

    @property
    def price(self):
        return self.content_object.price
    price.fget.short_description = 'Цена, руб.'

    @property
    def product(self):
        return f"{self.content_object.product} {get_price_properties(self.content_object)}"
    product.fget.short_description = 'Товар'

    def __str__(self):
        return f"{self.content_object}"

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
        ordering = ('id',)
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
