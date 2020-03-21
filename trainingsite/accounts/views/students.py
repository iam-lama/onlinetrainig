from django.contrib.auth import login
from django.shortcuts import redirect, render, render_to_response
from django.views.generic import CreateView, UpdateView
from ..decorators import student_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.decorators import method_decorator
from ..models import User
from trainboard.models import Student
from ..forms import StudentSignUpForm,StudentEditForm
from django.contrib import messages
from django.urls import reverse

class StudentSignUpView(CreateView):
	model = User
	form_class = StudentSignUpForm
	template_name = 'registration/signup_form.html'

	#Redirect logged in user to another page
	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('index')
		else:
			return super().dispatch(request, *args, **kwargs)

	#contain template and another information in a dictionary
	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'student'
		# kwargs.update({'request': self.request})			
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('index')


@method_decorator(login_required, name='dispatch')
class StudentEditView(UpdateView):

	model = Student
	form_class = StudentEditForm
	template_name= 'registration/update_form.html'
	# success_url='success.html'

	def get_form_kwargs(self):
	    kwargs = super(StudentEditView, self).get_form_kwargs()
	    kwargs['initial']['first_name'] = self.request.user.first_name
	    kwargs['initial']['last_name'] = self.request.user.last_name
	    kwargs['initial']['email'] = self.request.user.email
	    return kwargs
	

	def form_valid(self, form):
		# user = self.instance.user
		# cleaned_data = form.cleaned_data
		user = self.request.user
		user.email = form.cleaned_data['email']
		user.first_name = form.cleaned_data['first_name']
		user.last_name = form.cleaned_data['last_name']
		user.save()
		form.save()
		# messages.success(self.request, 'Your information has been updated successfuly')
		# return super().form_valid(form)
		return redirect('index')

