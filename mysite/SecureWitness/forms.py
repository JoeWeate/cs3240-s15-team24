from django.contrib.auth.models import User, Group, Permission
from SecureWitness.models import Report,Folder, Document
from django import forms

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'first_name', 'last_name')

class AddUserForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(AddUserForm, self).__init__(*args, **kwargs)
		self.fields['users'] = forms.ChoiceField(choices = [ (u.id, str(u)) for u in User.objects.all()])

class ReactivateUserForm(forms.Form):
	def __init__(self, members, *args, **kwargs):
		super(ReactivateUserForm, self).__init__(*args, **kwargs)
		self.fields['users'] = forms.ChoiceField(choices = [ (u.id, str(u)) for u in members])

class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = {'name'}

# class PermissionForm(forms.Form):
#   def __init__(self, ride, *args, **kwargs):
#       super(PermissionForm, self).__init__(*args, **kwargs)
#       self.fields['rides'] = forms.ChoiceField(choices = [ (r.id, str(r)) for r in Ride.objects.filter(start = ride.start, dest = ride.start)])

class DocumentForm(forms.Form):
	docfile = forms.FileField(
		label='Select a file',
		help_text='max. 42 megabytes'
	)
	name = forms.CharField(max_length=200)

class ReportForm(forms.ModelForm):
	def __init__(self, current_user, *args, **kwargs):
		super(ReportForm, self).__init__(*args, **kwargs)
		self.fields['doc'].queryset = Document.objects.filter(author = current_user)
	class Meta:
		model = Report
		fields = ('inc_date', 'author', 'short', 'detailed', 'privacy', 'doc', 'location')
		widgets = {'author':forms.HiddenInput()}

class SelectReportForm(forms.Form):
	def __init__(self, reports, *args, **kwargs):
		super(SelectReportForm, self).__init__(*args, **kwargs)
		self.fields['report'] = forms.ChoiceField(choices = [ (r.id, str(r)) for r in reports])

class EditForm(forms.ModelForm):
	def __init__(self, current_user, *args, **kwargs):
		super(EditForm, self).__init__(*args, **kwargs)
		self.fields['doc'].queryset = Document.objects.filter(author = current_user)
	class Meta:
		model = Report
		fields = ('author', 'inc_date', 'short', 'detailed', 'privacy', 'doc', 'location')
		widgets = {'author':forms.HiddenInput()}

class FolderForm(forms.ModelForm):
	def __init__(self, current_user, *args, **kwargs):
		super(FolderForm, self).__init__(*args, **kwargs)
		self.fields['reports'].queryset = Report.objects.filter(author = current_user)
	class Meta:
		model = Folder
		fields = ('name', 'reports', 'owner')
		widgets = {'owner':forms.HiddenInput()}