from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from trainboard.models import Student, Tutor
from django.db import transaction
from .choices import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from phonenumber_field.formfields import PhoneNumberField
   

class StudentSignUpForm(UserCreationForm):
	# first_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(),label='First Name')
	# last_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(),label='Last Name')
	# email = forms.CharField(max_length=255, required=True, widget=forms.EmailInput(),help_text="example@example.com")	
	country = forms.CharField(max_length=100,required=True,widget=forms.TextInput())
	region = forms.CharField(max_length=100,required=True,widget=forms.TextInput())	
	sex = forms.ChoiceField(choices=Sex_Choice,widget=forms.RadioSelect(),label='Gender')
	mobile = forms.RegexField(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}')
	id_num = forms.IntegerField(required=True, label='ID Number')
	id_image = forms.ImageField(required=True,label='ID Photo')
	
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('username','email', 'password1', 'password2','first_name', 'last_name',
			'country', 'region', 'sex', 'mobile','id_num','id_image')

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_student = True
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()
		std = Student.objects.create(user=user)
		#std.email.add(*self.cleaned_data.get('email'))
		std.country = self.cleaned_data['country']
		std.region = self.cleaned_data['region']
		std.sex = self.cleaned_data['sex']
		std.mobile = self.cleaned_data['mobile']
		std.id_num = self.cleaned_data['id_num']
		std.id_image = self.cleaned_data['id_image']
		std.save()
		return user


class StudentEditForm(UserChangeForm):
	country = forms.CharField(max_length=100,required=True,widget=forms.TextInput())
	region = forms.CharField(max_length=100,required=True,widget=forms.TextInput())	
	sex = forms.ChoiceField(choices=Sex_Choice,widget=forms.RadioSelect(),label='Gender')
	mobile = forms.RegexField(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}')
	id_num = forms.IntegerField(required=True, label='ID Number')
	id_image = forms.ImageField(required=True,label='ID Photo')

	#Remove password field
	password = None

	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name',
			'country', 'region', 'sex', 'mobile','id_num','id_image']
	

class TutorSignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(),label='First Name')
	last_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(),label='Last Name')
	email = forms.CharField(max_length=255, required=True, widget=forms.EmailInput(),help_text="example@example.com")
	# mobile = forms.IntegerField(required=True, label='Mobile')
	mobile = PhoneNumberField(widget=forms.TextInput(),required=True)

	class Meta(UserCreationForm.Meta):
		model = User

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_tutor = True
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()
		tutor = Tutor.objects.create(user=user)
		tutor.mobile = self.cleaned_data['mobile']
		tutor.save()
		return user





