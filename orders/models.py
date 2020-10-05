from decimal import Decimal

from django.db import models
from freestuff.models import Things

from coupons.models import Coupon

DELIVERY = (
    ('Ukrposhta', 'Укрпошта'),
    ('NovaPoshta', 'Нова пошта'),)

ORDER_SRATUS = (
    ('Created', 'Створено'),
    ('Paid', 'Оплачено'),
    ('Formed', 'Сформовано'),
    ('Send', 'Відправлено'),
    ('Arrived', 'Прибуло'),
    ('Received', 'Отримано'),
    ('Return', 'Повернуто'),
    ('Archive', 'В архіві'),
)

class Order(models.Model):
    user = models.CharField('User', max_length=50, null=True, blank=True)
    first_name = models.CharField(verbose_name="І'мя", max_length=30)
    last_name = models.CharField(verbose_name='Прізвище', max_length=30)
    email = models.EmailField(verbose_name='Email')
    phone = models.PositiveIntegerField(verbose_name='Номер телефону')
    street = models.CharField(verbose_name='Вулиця', max_length=50, null=True, blank=True)
    postal_code = models.CharField(verbose_name='Індекс', max_length=20, null=True, blank=True)
    city = models.CharField(verbose_name='Місто/село', max_length=50)
    region = models.CharField(verbose_name='Район', max_length=50, blank=True, null=True)
    province = models.CharField(verbose_name='Область', max_length=50, blank=True, null=True)
    shipping = models.CharField(verbose_name='Перевізник', max_length=20, choices=DELIVERY, blank=True, null=True)
    department = models.PositiveIntegerField(verbose_name='відділення Нової пошти №', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updates = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(verbose_name='Статус', max_length= 20, choices=ORDER_SRATUS,
                              default='Created')
    coment = models.TextField(verbose_name='Коментар', null=True, blank=True)

    class Meta():
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    thing = models.ForeignKey(Things, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return ' {} '.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

