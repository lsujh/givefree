import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings



from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from users.models import Profile, CustomUser


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/detail.html', {'order': order})

def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm()
    if request.user.is_authenticated:
        data = Profile.objects.prefetch_related('user').get(user=request.user)
        data = {'first_name': data.user.first_name, 'last_name': data.user.last_name,
                'email': data.user.email, 'phone': data.phone, 'address': data.address,
                'postal_code': data.postal_code, 'city': data.city}
        form = OrderCreateForm(data)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            order = form.save(commit=False)
            order.user = request.user.id
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, thing=item['thing'],
                    quantity=item['quantity'],
                    price=item['price'])
            cart.clear()
            # order_created.delay(order.id)
            return render(request, 'orders/created.html', {'order': order})

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response

