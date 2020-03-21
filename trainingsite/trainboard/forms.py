from django import forms
from .models import User
from trainboard.models import Student
from django.db import transaction
from django.conf import settings
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
   


class CourseRegister(forms.ModelForm):

	class Meta:
		model = Student
		fields = []

	
	





