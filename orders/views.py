from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from users.models import Profile


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/detail.html', {'order': order})

def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm()
    if request.user.is_authenticated:
        data = Profile.objects.filter(user=request.user).first()
        print(data.user)
        form = OrderCreateForm(instance=data)
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

