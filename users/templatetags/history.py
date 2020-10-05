from django import template

from orders.models import Order

register = template.Library()

@register.inclusion_tag('history_orders.html')
def history_orders(request):
    orders = Order.objects.filter(user=request.user.id)
    return {'orders': orders }



