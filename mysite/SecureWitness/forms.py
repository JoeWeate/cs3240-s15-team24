from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'first_name', 'last_name')

class DocumentForm(forms.Form):
	docfile = forms.FileField(
		label='Select a file',
		help_text='max. 42 megabytes'
	)

