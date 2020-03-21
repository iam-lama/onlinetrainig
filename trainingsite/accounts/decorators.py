from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

#If you want to execute the view according to the user role, we can write decorators using model methods

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
	actual_decorator = user_passes_test(
		lambda u: u.is_active and u.is_student,
		login_url = login_url, redirect_field_name=redirect_field_name
		)
	if function:
		return actual_decorator(function)
	return actual_decorator

def tutor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
	actual_decorator = user_passes_test(
		lambda u: u.is_active and u.is_tutor,
		login_url = login_url, redirect_field_name=redirect_field_name
		)
	if function:
		return actual_decorator(function)
	return actual_decorator