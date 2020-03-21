# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class SignUpView(TemplateView):
	template_name = 'registration/signup.html'

def home(request):
	if request.user.is_authenticated:
		return redirect('index')
	return render(request, 'index.html')