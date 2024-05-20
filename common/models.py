from django.db import models
from common.managers import IsVisibleManager
from django.contrib.contenttypes import fields
from django.core.exceptions import ValidationError
from common.errors import MSG_ONE_REQUIRED
from common.managers import SearchManager
from favorites.models import Favorites
from images.models import Image


class PageAbstract(models.Model):
    head_title = models.CharField('заголовок', max_length=80)
    meta_description = models.CharField('мета описание', max_length=160)

    name = models.CharField('название', max_length=80, unique=True)
    slug = models.SlugField('слаг',
                            max_length=80, blank=False, unique=True)

    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('дата обновления', auto_now=True)
    is_visible = models.BooleanField('показывать?', default=1, db_index=True)

    objects = models.Manager()

    is_visible_objects = IsVisibleManager()

    def __str__(self):
        return str(self.name)

    class Meta:
        abstract = True


class ProductAbstract(PageAbstract):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_trans_words = models.CharField(
        'перевод слов в названии', max_length=100, blank=True,
        help_text='Перечисление слов через запятую. Например: если название "Alberta Globe", то: альберта, глоб, глоуб. Скрытое поле, предназначено для поиска.')

    short_description = models.CharField('короткое описание', max_length=250)
    description = models.TextField('описание', blank=True)

    images = fields.GenericRelation(Image)
    favorites = fields.GenericRelation(Favorites)

    objects = SearchManager()

    @property
    def get_image(self):
        try:
            # return self.images.order_by('order_number').first()
            return self.images.first()
        except self.DoesNotExist:
            return ''
        except IndexError:
            return ''

    def __str__(self):
        return str(self.name)

    class Meta:
        abstract = True


class ProductPriceAbstract(models.Model):
    price = models.DecimalField('цена, руб', max_digits=9, decimal_places=2)

    class Meta:
        abstract = True
        ordering = ('price',)
        verbose_name = 'цена'
        verbose_name_plural = 'цены'

    @property
    def get_complex_name(self):
        try:
            s = ''
            if hasattr(self, 'container') and self.container:
                s = f"{self.container} "

            if (hasattr(self, 'height') and self.height) and (hasattr(self, 'width') and self.width):
                s = f"{s}{self.height}x{self.width} "
            else:
                if hasattr(self, 'height') and self.height:
                    s = f"{s}{self.height} "

                if hasattr(self, 'width') and self.width:
                    s = f"{s}{self.width} "

            if hasattr(self, 'trunk_diameter') and self.trunk_diameter:
                s = f"{s}{self.trunk_diameter} "

            if hasattr(self, 'shtamb') and self.shtamb:
                # s = f"{s}{self._meta.get_field('shtamb').verbose_name} {self.shtamb} "
                s = f"{s} штамб {self.shtamb} "

            if hasattr(self, 'rs') and self.rs:
                s = f"{s}{self.rs} "

            if hasattr(self, 'planting_year') and self.planting_year:
                s = f"{s}{self.planting_year} г. "

            if hasattr(self, 'age') and self.age:
                s = f"{s}{self.age} "

            if hasattr(self, 'rootstock') and self.rootstock:
                s = f"{s}{self.rootstock} "

            if hasattr(self, 'extra') and self.extra:
                s = f"{s}{self._meta.get_field('extra').verbose_name} "

            if hasattr(self, 'bush') and self.bush:
                s = f"{s}{self._meta.get_field('bush').verbose_name} "

            if hasattr(self, 'name') and self.name:
                s = f"{s}{self.name} "

            return s.strip()

        except self.DoesNotExist:
            return ''
        except IndexError:
            return ''

    @property
    def get_complex_popover(self):
        try:
            s = ''
            if hasattr(self, 'container') and self.container:
                s = f"<div><strong>{self.container}</strong> - {self.container.description}</div>"

            if hasattr(self, 'height') and self.height:
                s = f"{s}<div><strong>{self.height}</strong> - Высота растения, см.</div>"

            if hasattr(self, 'width') and self.width:
                s = f"{s}<div><strong>{self.width}</strong> - Ширина растения, см.</div>"

            if hasattr(self, 'trunk_diameter') and self.trunk_diameter:
                s = f"{s}<div><strong>{self.trunk_diameter}</strong> - Диаметр ствола, см.</div>"

            if hasattr(self, 'shtamb') and self.shtamb:
                field = self._meta.get_field('shtamb')
                s = f"{s}<div><strong>штамб {self.shtamb}</strong> - {field.help_text}</div>"

            if hasattr(self, 'rs') and self.rs:
                s = f"{s}<div><strong>{self.rs}</strong> - {self.rs.description}</div>"

            if hasattr(self, 'planting_year') and self.planting_year:
                s = f"{s}<div><strong>{self.planting_year} г.</strong> - Год посадки.</div>"

            if hasattr(self, 'age') and self.age:
                s = f"{s}<div><strong>{self.age}</strong> - Возраст растения.</div>"

            if hasattr(self, 'rootstock') and self.rootstock:
                s = f"{s}<div><strong>{self.rootstock}</strong> - Подвой.</div>"

            if hasattr(self, 'extra') and self.extra:
                field = self._meta.get_field('extra')
                s = f"{s}<div><strong>{field.verbose_name}</strong> - {field.help_text}</div>"

            if hasattr(self, 'bush') and self.bush:
                field = self._meta.get_field('bush')
                s = f"{s}<div><strong>{field.verbose_name}</strong> - {field.help_text}</div>"

            return s.strip()

        except self.DoesNotExist:
            return ''
        except IndexError:
            return ''

    def validate_one_of_required(self, field_list):
        msg = {}
        msg.update({value: MSG_ONE_REQUIRED for value in field_list})

        if all(not getattr(self, name) for name in field_list):
            raise ValidationError(msg, code='required')
