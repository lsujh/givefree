import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator, MinLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import CustomUserManager



class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField("Ім'я",  max_length=30, validators=
                                    [MinLengthValidator(2), RegexValidator(r'^[-a-zA-ZА-Яа-я]+\Z', message='Enter your name')],
                                    help_text=None, error_messages={'required': 'Enter your name'}, blank=True)
    last_name = models.CharField('Прізвище', max_length=30, validators=
                                 [MinLengthValidator(2), RegexValidator(r'^[-a-zA-ZА-Яа-я]+\Z', message='Enter your last name')],
                                 help_text=None, error_messages={'required': 'Enter your last name'}, blank=True)
    image = models.ImageField('Фото', upload_to='image/', blank=True)
    email = models.EmailField('email адреса', unique=True)
    email_confirm = models.BooleanField(default=False)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    address = models.CharField('Адреса', max_length=250, blank=True, null=True)
    postal_code = models.CharField('Індекс', max_length=20, blank=True, null=True)
    city = models.CharField('Місто/село', max_length=100, blank=True, null=True)

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

