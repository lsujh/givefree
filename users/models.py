import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(verbose_name="Ім'я", max_length=30, validators=
                                    [MinLengthValidator(2), RegexValidator(r'^[-a-zA-ZА-Яа-я]+\Z', message='Введіть Ваше Імʼя')],
                                    blank=True)
    last_name = models.CharField(verbose_name='Прізвище', max_length=30, validators=
                                 [MinLengthValidator(2), RegexValidator(r'^[-a-zA-ZА-Яа-я]+\Z', message='Введіть Ваше Прізвище')],
                                 blank=True)
    image = models.ImageField(verbose_name='Фото', upload_to='image/', blank=True)
    email = models.EmailField(verbose_name='email адреса', unique=True)
    email_confirm = models.BooleanField(default=False)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(verbose_name='Телефон', max_length=20, blank=True, null=True)
    street = models.CharField(verbose_name='Вулиця', max_length=50, blank=True, null=True)
    postal_code = models.CharField(verbose_name='Індекс', max_length=20, blank=True, null=True)
    city = models.CharField(verbose_name='Місто/село', max_length=50, blank=True, null=True)
    region = models.CharField(verbose_name='Район', max_length=50, blank=True, null=True)
    province = models.CharField(verbose_name='Область', max_length=50, blank=True, null=True)

    @receiver(post_save, sender=CustomUser)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    # def save(self, *args, **kwargs):
    #     super(self.__class__, self).save(*args, **kwargs)
    #     if self._state.adding is True:
    #         Profile.objects.create()


    # def __str__(self):
    #     return self.user__profile.email


class TemporaryBanIp(models.Model):
    ip_address = models.GenericIPAddressField('IP адреса', unique=True)
    attempts = models.IntegerField('Невдалих спроб', default=0)
    time_unblock = models.DateTimeField('Час розблокування', blank=True)
    status = models.BooleanField('Статус блокування', default=False)

    def __str__(self):
        return self.ip_address
