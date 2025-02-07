from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from solo.models import SingletonModel
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType


class OrderStatus(models.Model):
    name = models.CharField('статус', max_length=50, unique=True,)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class AcceptingOrders(SingletonModel):
    CHOICES = (
        ('ORDER', 'Принимаются заказы'),
        ('PRE_ORDER', 'Принимаются предзаказы'),
        ('CLOSE_UNTIL_APRIL', 'Не принимаются до первых чисел апреля'),
    )
    name = models.CharField(
        'Режим приема заказов', max_length=50, default='ORDER', unique=True, choices=CHOICES,
    )

    def __str__(self):
        return f"{dict(self.CHOICES)[self.name]}"

    class Meta:
        verbose_name = 'прием заказов*'
        verbose_name_plural = 'прием заказов'


@receiver(post_save, sender=AcceptingOrders)
def invalidate_cache(instance, **kwargs):
    if kwargs.get('raw'):  # add for test, pass fixtures
        return

    cache.clear()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT,
        blank=True, null=True, verbose_name='Пользователь', default=None)

    number = models.CharField(max_length=8, verbose_name='номер заказа')

    created_at = models.DateTimeField('дата создания', auto_now_add=True)

    customer_first_name = models.CharField('имя', max_length=50, )
    customer_last_name = models.CharField('фамилия', max_length=50, blank=True, )
    customer_email = models.EmailField('адрес электронной почты', max_length=70, )
    customer_phone_number = models.CharField(max_length=20, verbose_name='номер телефона', )
    customer_comment = models.TextField(
        'комментарий к заказу', blank=True, validators=[MaxLengthValidator(1000)], )

    # confirm_code = models.CharField(
    #     'код подтверждения заказа', max_length=4, default='-')
    # confirmed_by_email = models.BooleanField(
    #     verbose_name='заказ подтвержден по электронной почте', blank=True, null=True, default=None)

    ip = models.CharField(
        'IP адрес', max_length=39, blank=True, )
    user_agent = models.TextField('user agent', blank=True)

    status_change_email = models.BooleanField(
        'отправить письмо при смене статуса', default=False)
    status = models.ForeignKey(
        OrderStatus, verbose_name='статус заказа', default=1, on_delete=models.CASCADE)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.order_items.all())

    @property
    def total_quantity(self):
        return sum(item.total_quantity for item in self.order_items.all())

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ № {self.number}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='заказ')

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id',)

    name = models.CharField(max_length=150, verbose_name='название')

    price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='цена')

    quantity = models.PositiveIntegerField(
        default=0, verbose_name='количество')

    created_at = models.DateTimeField('дата создания', auto_now_add=True)

    @property
    def total_price(self):
        # return self.content_object.price * self.quantity
        return self.price * self.quantity
    total_price.fget.short_description = 'Сумма, руб.'

    @property
    def total_quantity(self):
        return self.quantity

    @property
    def product(self):
        # return f"{self.content_object.product} {self.content_object.get_complex_name}"
        return self.name
    product.fget.short_description = 'Товар'

    def __str__(self):
        return f"{self.name} - заказ № {self.order.number}"

    class Meta:
        # indexes = [
        #     models.Index(fields=["content_type", "object_id"]),
        # ]
        verbose_name = 'заказанный товар'
        verbose_name_plural = 'заказанные товары'
