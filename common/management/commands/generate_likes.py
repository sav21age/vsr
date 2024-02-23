#coding=utf-8
import random
from sys import stdout
from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from reviews.models import Review, ReviewHelpfulness
from smartwatches.models import SmartWatch
from smartwristbands.models import SmartWristband
from wishlists.models import WishList
from wristwatches.models import WristWatch


def add_likes(qs, content_type):
    # reviews = Review.objects.all()
    users = list(User.objects.all())

    # lst = len(list(qs))
    for obj in qs:
        if random.randint(0, 1):
            random.shuffle(users)
            # random_users = users[:random.randint(1, len(users) // 3)]
            random_users = users[:random.randint(1, 7)]
            for user in random_users:
                WishList.objects.create(user=user, content_type=content_type, object_id=obj.id)

                # if user != review.user:
                    # helpfulness = random.randint(-1, 1)
                    # if helpfulness != 0:
                    #     ReviewHelpfulness.objects.create(user=user, review=review, helpfulness=helpfulness)
                    #
                    #     count = ReviewHelpfulness.objects.filter(review_id=review.id) \
                    #         .filter(helpfulness=helpfulness).count()
                    #     if helpfulness == 1:
                    #         Review.objects.filter(id=review.id).update(helpfulness_positive_counter=count)
                    #     else:
                    #         Review.objects.filter(id=review.id).update(helpfulness_negative_counter=count)

                        # if helpfulness == 1:
                        #     Review.objects.filter(id=review.id).update(helpfulness_positive_counter=F('helpfulness_positive_counter')+1)
                        # else:
                        #     Review.objects.filter(id=review.id).update(helpfulness_negative_counter=F('helpfulness_negative_counter')+1)

            #     stdout.write('+', ending='')
            # else:
            #     stdout.write('-', ending='')
            stdout.write('')
            # list_reviews -= 1
            # stdout.write(u'%s' % list_reviews)


class Command(BaseCommand):
    help = 'Add helpfulness to reviews'

    def handle(self, *args, **options):
        qs = WristWatch.objects.all()
        # qs = WristWatch.objects.filter(id=1014)
        model = apps.get_model('wristwatches', 'WristWatch')
        content_type = ContentType.objects.get_for_model(model)
        add_likes(qs, content_type)

        qs = SmartWatch.objects.all()
        model = apps.get_model('smartwatches', 'SmartWatch')
        content_type = ContentType.objects.get_for_model(model)
        add_likes(qs, content_type)

        qs = SmartWristband.objects.all()
        model = apps.get_model('smartwristbands', 'SmartWristband')
        content_type = ContentType.objects.get_for_model(model)
        add_likes(qs, content_type)