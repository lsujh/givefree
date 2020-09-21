from django import forms


class CartAddThingForm(forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=1, label='Кількість')
    price = forms.DecimalField(initial=0, max_digits=10, decimal_places=2)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)