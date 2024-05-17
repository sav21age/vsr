from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

decimal_comma = '\d{1,3}(\,\d{1,3})?'

NumericValidator = RegexValidator(
    r'^[0-9+]+$', 'Можно вводить цифры')

SizeValidator = RegexValidator(
    r'^[0-9+\-\+\/дот, ]+$', 'Можно вводить цифры, "/", "-" и "+"')

# SizeUnitValidator = RegexValidator(
#     r'^[0-9+\-дотсм, ]+$', 'Можно вводить цифры, от, до, м, см, "-" и ","')

SizeUnitValidator = RegexValidator(
    fr'^((от|до)[\s])?{decimal_comma}(\-?{decimal_comma})?([\s](м|см))?$',
    'Можно вводить цифры, от, до, м, см, "-" и ","')

LetterValidator = RegexValidator(
    r'^[а-яА-Я]+$', 'Можно вводить только буквы')

PhoneNumberValidator = RegexValidator(
    r'^\+?\d{0,1}?[\s]?\(?\d{1,3}?\)?[\s]?\d{1,3}[-\s]?\d{1,2}[-\s]?\d{1,2}$',
    'Формат ввода: +7 (777) 777-77-77')

FloweringPeriodValidator = RegexValidator(
    r'(IX|IV|V?I{0,3}|\-)', 'Можно вводить только римские цифры и "-"')

# PhoneNumberValidator = RegexValidator(
#     r'^[0-9+\-\+\(\) ]+$', 'Можно вводить цифры, "+", "-" и "()"')

# SizeMeterValidator = RegexValidator(r'^[0-9+\-дот, ]+$', 'Можно вводить цифры, от, до, "-" и ","')

# SizeСentimeterValidator = RegexValidator(
#     r'^[0-9+\-дот ]+$', 'Можно вводить цифры, от, до и "-"' )

# regex = r'^\+?1?\d{9,15}$'

# ^\+?\d{1}?[\s]?\(?\d{1,3}?\)?[\s]?\d{1,4}[-\s]?\d{1,4}[-\s]?\d{1,9}$


def YearStringValidator(value):
    if value and int(value) < 2015:
        raise ValidationError('Год должен быть больше 2015')
