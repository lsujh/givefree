from django import forms
from django.core.exceptions import ValidationError

from freestuff.models import Things


class CartAddThingForm(forms.ModelForm):
    quantity = forms.IntegerField(initial=1, min_value=1, label='Кількість',
                                  widget=forms.NumberInput(attrs={'step': 1}))
    price = forms.DecimalField(max_digits=5, decimal_places=0, label='Ціна:',
                               widget=forms.NumberInput(attrs={'readonly': True, 'step': 1,
                                                               }))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    class Meta:
        model = Things
        fields = ('quantity', 'price')

    def clean(self):
        quantity = self.cleaned_data['quantity']
        if quantity > self.thing.quantity:
            CartAddThingForm.add_error(self, 'quantity', error=ValidationError(f'Повинно бути не більше {self.thing.quantity} шт.'))

