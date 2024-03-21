# from django import template

# from common.helpers import get_price_properties


# register = template.Library()

# @register.simple_tag
# def get_price_params(obj):
#     return get_price_properties(obj)


# @register.simple_tag
# def get_price_params_popover(obj):
#     s = ''
#     if hasattr(obj, 'container') and obj.container:
#         s = f"<div><strong>{obj.container}</strong> - {obj.container.description}</div>"

#     if hasattr(obj, 'height') and obj.height:
#         s = f"{s}<div><strong>{obj.height}</strong> - Высота, см.</div>"

#     if hasattr(obj, 'width') and obj.width:
#         s = f"{s}<div><strong>{obj.width}</strong> - Ширина, см.</div>"

#     if hasattr(obj, 'trunk_diameter') and obj.trunk_diameter:
#         s = f"{s}<div><strong>{obj.trunk_diameter}</strong> - Диаметр ствола, см.</div>"

#     if hasattr(obj, 'shtamb') and obj.shtamb:
#         field = obj._meta.get_field('shtamb')
#         s = f"{s}<div><strong>штамб {obj.shtamb}</strong> - {field.help_text}</div>"

#     if hasattr(obj, 'rs') and obj.rs:
#         s = f"{s}<div><strong>{obj.rs}</strong> - {obj.rs.description}</div>"

#     if hasattr(obj, 'planting_year') and obj.planting_year:
#         s = f"{s}<div><strong>{obj.planting_year} г.</strong> - Год посадки.</div>"

#     if hasattr(obj, 'age') and obj.age:
#         s = f"{s}<div><strong>{obj.age}</strong> - Возраст.</div>"

#     if hasattr(obj, 'extra') and obj.extra:
#         field = obj._meta.get_field('extra')
#         s = f"{s}<div><strong>{field.verbose_name}</strong> - {field.help_text}</div>"

#     return s

