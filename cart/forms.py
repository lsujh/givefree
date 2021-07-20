from django import forms
from django.core.exceptions import ValidationError

from freestuff.models import Things


class CartAddThingForm(forms.ModelForm):
    quantity = forms.IntegerField(initial=1, min_value=1, label='Кількість')
    price = forms.DecimalField(max_digits=10, decimal_places=2,
                               widget=forms.NumberInput(attrs={'readonly': True}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    class Meta:
        model = Things
        fields = ('quantity', 'price')

    def clean(self):
        cd = self.cleaned_data
        if cd['quantity'] > self.thing.quantity:
            CartAddThingForm.add_error(self, 'quantity', error=ValidationError(f'Повинно бути не більше {self.thing.quantity} шт.'))

