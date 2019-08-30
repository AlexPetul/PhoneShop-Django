from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from phones_app.models import Order


class UserLoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label='Username')
	password = forms.CharField(widget=forms.PasswordInput(), label='Password')

	class Meta:
		model = User
		fields = ('username', 'password',)

	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super(UserLoginForm, self).clean()
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		if not User.objects.filter(username=username).exists():
			raise forms.ValidationError({'username': ['User with this username doesnt exist']})
		current_user = User.objects.get(username=username)
		if current_user and not current_user.check_password(password):
			raise forms.ValidationError({'password': ['Incorrect password']})
		return cleaned_data


class ShopUserCreationForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
	password2 = forms.CharField(widget=forms.PasswordInput(), label='Password check')

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(ShopUserCreationForm, self).__init__(*args, **kwargs)


	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('Passwords dont match.')


	def clean(self):
		cleaned_data = super(ShopUserCreationForm, self).clean()
		username = cleaned_data.get('username')
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError({'username': ['User with this username already exists.']})
		return cleaned_data


	def save(self, commit=True):
		user = super().save(commit=False)
		user.username = self.cleaned_data.get('username')
		user.set_password(self.cleaned_data.get('password1'))
		if commit:
			user.save()
		return user



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
			raise forms.ValidationError(
				{'address': ['Please enter your address.']})
		return cleaned_data

	class Meta:
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
