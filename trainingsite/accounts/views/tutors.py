from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from ..decorators import tutor_required
from django.contrib.auth.decorators import login_required

from ..models import User
from ..forms import TutorSignUpForm

class TutorSignUpView(CreateView):
	model = User
	form_class = TutorSignUpForm
	template_name = 'registration/signup_form.html'
	
	#Redirect logged in user to another page
	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('index')
		else:
			return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'tutor'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('home')

