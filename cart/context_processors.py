from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}

def cart_pk(request):
    if request.session.get('cart'):
        pk = [int(i) for i in request.session.get('cart')]
    else:
        pk = None
    return {'cart_pk': pk}
