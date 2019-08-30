from django import forms
from django.utils import timezone
from phones_app.models import Order


class OrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+375447256776'}))
    address = forms.CharField(required=False)
    BUYING_TYPES = (
        ('Picking up', 'Picking up'),
        ('At home', 'At home')
    )
    buying_type = forms.CharField(widget=forms.Select(choices=BUYING_TYPES))
    date = forms.DateField(initial=timezone.now())
    comment = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        buying_type = cleaned_data.get('buying_type')
        address = cleaned_data.get('address')
        if buying_type == 'At home' and not address:
            raise forms.ValidationError({'address': ['Please enter your address.']})
        return cleaned_data

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
