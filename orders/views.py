import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.db.models import F

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from users.models import Profile, CustomUser
from freestuff.models import Things


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/detail.html', {'order': order})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/detail.html', {'order': order})

def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm()
    data = None
    if request.user.is_authenticated:
        data = Profile.objects.prefetch_related('user').get(user=request.user)
        data = {'first_name': data.user.first_name, 'last_name': data.user.last_name,
                'email': data.user.email, 'phone': data.phone, 'street': data.street,
                'postal_code': data.postal_code, 'city': data.city, 'region': data.region,
                'province': data.province,}
        form = OrderCreateForm(data)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            order = form.save(commit=False)
            order.user = request.user.id
            order.save()
            for item in cart:
                if item['quantity'] > item['thing_quantity']:
                    item['quantity'] = item['thing_quantity']
                OrderItem.objects.create(
                    order=order, thing=item['thing'],
                    quantity=item['quantity'],
                    price=item['price'])
                Things.objects.filter(pk=item['pk']).update(quantity=F('quantity') - item['quantity'])
            cart.clear()
            if data:
                data['first_name'] = cd['first_name'] if not data['first_name'] \
                                    or (data['first_name'] != cd['first_name']) else data['first_name']
                data['last_name'] = cd['last_name'] if not data['last_name'] \
                                    or (data['last_name'] != cd['last_name'])else data['last_name']
                data['phone'] = cd['phone'] if not data['phone'] \
                                    or (data['phone'] != cd['phone']) else data['phone']
                data['street'] = cd['street'] if not data['street'] \
                                    or (data['street'] != cd['street']) else data['street']
                data['city'] = cd['city'] if not data['city'] \
                                    or (data['city'] != cd['city']) else data['city']
                data['region'] = cd['region'] if not data['region'] \
                                    or (data['region'] != cd['region']) else data['region']
                data['province'] = cd['province'] if not data['province'] \
                                    or (data['province'] != cd['province']) else data['province']
                data['postal_code'] = cd['postal_code'] if not data['postal_code'] \
                                    or (data['postal_code'] != cd['postal_code']) else data['postal_code']
                Profile.objects.filter(user=request.user).update(phone=data['phone'], street=data['street'],
                                                                 city=data['city'], region=data['region'],
                                                                 province=data['province'],postal_code=data['postal_code'],
                                                                 )
                CustomUser.objects.filter(id=request.user.id).update(first_name=data['first_name'], last_name=data['last_name'],
                                                                     )

            order_created.delay(order.id)
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

