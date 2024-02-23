import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum


#    ...: users = []
#    ...:
#    ...: for i in range(1000):
#    ...:     user = User(first_name='User%dFirstName' % i,
#    ...:                 last_name='User%dLastName' % i,
#    ...:                 username='user%d' % i,
#    ...:                 email='user%d@mydomain.com' % i,
#    ...:                 password='hashedPasswordStringPastedHereFromStep1!',
#    ...:                 is_active=True,
#    ...:                 )
#    ...:     users.append(user)
#    ...:
#    ...: User.objects.bulk_create(users)

lst = ['Кевин Бейкон',
       'Жаклин Биссет',
       'Эрнест Боргнайн',
       'Джеймс Каан',
       'Алек Болдуин',
       'Джим Керри',
       'Чеви Чейз',
       'Кевин Костнер',
       'Билли Кристал',
       'Клэр Дэйнс',
       'Джина Дэвис',
       'Лора Дерн',
       'Мэтт Диллон',
       'Ричард Дрейфус',
       'Джеки Чан',
       'Клинт Иствуд',
       'Миа Фэрроу',
       'Бриджит Фонда',
       'Питер Фонда',
       'Морган Фримен',
       'Тери Гарр',
       'Вупи Голдберг',
       'Джефф Голдблюм',
       'Вуди Харрельсон',
       'Ричард Харрис',
       'Голди Хоун',
       'Грегори Хайнс',
       'Дастин Хоффман',
       'Анджелина Джоли',
       'Майкл Китон',
       'Мартин Ландау',
       'Джессика Лэнг',
       'Ширли Маклейн',
       'Марша Мейсон',
       'Марли Мэтлин',
       'Майк Майерс',
       'Эдвард Нортон',
       'Эдвард Джеймс Олмос',
       'Мисс Пигги',
       'Линн Редгрейв',
       'Джулия Робертс',
       'Джина Роулендс',
       'Кевин Спейси',
       'Сильвестр Сталлоне',
       'Род Стайгер',
       'Шэрон Стоун',
       'Билли Боб Торнтон',
       'Лили Томлин',
       'Эмили Уотсон',
       'Джеймс Вудс',]


class Command(BaseCommand):
    def handle(self, *args, **options):
        
        domains = ['com', 'ru', 'co.uk', 'net', 'us', ]
        domain_names = ['gmail', 'mail', 'yandex', 'rambler', 'amazon', ]

        i = 0
        for value in lst:
            try:
                email = f"{lorem_ipsum.words(1, False).lower()}{i}@{random.choice(domain_names)}.{random.choice(domains)}"
                user = User.objects.create(
                    username=email,
                    first_name=value.split()[0],
                    last_name=value.split()[1],
                    email=email,
                    password='1234567',
                    is_active=True,
                )
                user.set_password('1234567')
                user.save()
                i +=1

                self.stdout.write('+', ending='')
            except Exception as e:
                print(e)