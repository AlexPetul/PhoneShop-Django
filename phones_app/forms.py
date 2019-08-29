from django import forms
from django.utils import timezone


class OrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': '+375447256776'}))
    address = forms.CharField(
        required=False, help_text='Fill this field if you want to make order at home.')
    BUYING_TYPES = (
        ('Picking up', 'Picking up'),
        ('At home', 'At home')
    )
    buying_type = forms.CharField(widget=forms.Select(choices=BUYING_TYPES))
    date = forms.DateField(initial=timezone.now())
    comment = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        fields = ('')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
