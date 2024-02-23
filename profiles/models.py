from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        'номер телефона', max_length=18, blank=True,)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'профиль пользователь'
        verbose_name_plural = 'профили пользователей'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if kwargs.get('raw'): #add for test, pass fixtures
        return
    if created:
        Profile.objects.create(user=instance)
        