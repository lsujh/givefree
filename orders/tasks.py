from django.core.mail import send_mail
from django.conf import settings
from .models import Order


def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Order № {}'.format(order.id)
    message = 'Дорогий {},\n\nВаше замовлення оформлено{}'.format(
        order.first_name, order.id)
    mail_sent = send_mail(
        subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_sent
