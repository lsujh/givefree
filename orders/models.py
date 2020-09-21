from django.db import models
from freestuff.models import Things
from coupons.models import Coupon

DELIVERY = (
    ('Ukrposhta', 'Укрпошта'),
    ('NovaPoshta', 'Нова пошта'),)

class Order(models.Model):
    user = models.CharField('User', max_length=50, null=True, blank=True)
    first_name = models.CharField('Прізвище', max_length=50)
    last_name = models.CharField('І`мя', max_length=50)
    email = models.EmailField()
    phone = models.PositiveIntegerField('Номер телефону')
    address = models.CharField('Адреса', max_length=250, null=True, blank=True)
    postal_code = models.CharField('Індекс', max_length=20, null=True, blank=True)
    city = models.CharField('Місто/село', max_length=100)
    shipping = models.CharField(max_length=20, choices=DELIVERY, blank=True, null=True)
    department = models.PositiveIntegerField('відділення Нової пошти №', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updates = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta():
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    thing = models.ForeignKey(
        Things, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return ' {} '.format(self.id)

