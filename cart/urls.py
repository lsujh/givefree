from django.urls import path
from .views import cart_detail, cart_add, cart_remove


app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:thing_pk>/', cart_add, name='cart_add'),
    path('remove/<int:thing_pk>/', cart_remove, name='cart_remove'),

]