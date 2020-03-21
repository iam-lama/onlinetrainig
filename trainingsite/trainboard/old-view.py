# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django import forms
from .forms import CourseRegister
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Course, Student, Accountant

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
							  merchant_id=settings.BRAINTREE_MERCHANT,
							  public_key=settings.BRAINTREE_PUBLIC_KEY,
							  private_key=settings.BRAINTREE_PRIVATE_KEY)

# Create your views here.
class HomePageView(ListView):
	model = Course
	context_object_name = 'courses'
	template_name = 'index.html'

class CourseDetailView(FormMixin, DetailView):
	model = Course
	context_object_name = 'course'
	form_class = CourseRegister
	template_name = 'course_detail.html'

	def post(self, request, *args, **kwargs):
		student = get_object_or_404(Student, user=request.user)
		form = CourseRegister(request.POST)
		if form.is_valid():
			course = self.get_object()
			student.course.add(course)
			student.save()
			# course = get_object_or_404(Course, pk=request.user)
			token = client_token()
			return render(request, 'checkout.html' , {'student': student, 'course': course, 'client_token':token} )
		else:
			return render(request, 'error.html')


def client_token():
	client_token = braintree.ClientToken.generate()
	return client_token

def generate_payment_token(token):
	payment_token_nonce = braintree.PaymentMethod.create({
	"customer_id": token,
	"payment_method_nonce": nonce_from_the_client
	})


@login_required
@csrf_exempt
def checkout(request):
	rg = request.POST
	amount = request.POST['prise']
	user = request.user.id 
	student = get_object_or_404(Student, user=request.user)
	braintree_info = Braintree()
	braintree_info.student = student.pk
	a_customer_id = ''
	if not user.customer_id:
		result = braintree.Customer.create({
			"first_name": user.first_name,
			"last_name": user.last_name,
			"company": 'Braintree',
			"email": user.email,
			"phone": user.mobile,
			"fax": '00000000',
			"website": 'www.example.com',
			})
		if result.is_success:
			braintree_info.customer_id = result.customer_id
			user.save()
			a_customer_id = braintree_info.customer_id
		else:
			a_customer_id = braintree_info.customer_id
		if not user.client_token:
			client_token = client_token = braintree.ClientToken.generate({
				"customer_id": a_customer_id
				})
			braintree_info.client_token = client_token
			student.braintree.save()
		else:
			client_token = sbraintree_info.client_token
	variables = {'amount':amount,'client_token':client_token}
	return render(request, 'checkout.html', variables)

@login_required
@csrf_exempt
def payment(request):
	if request.POST:
		if request.POST['payment_method_nonce']:
			nonce_from_the_client = request.POST['payment_method_nonce']
			buyer = get_object_or_404(Student, user=request.user) 
			acc = Accountant()
			acc.student = buyer
			acc.payment_nonce = nonce_from_the_client
			acc.amount = request.POST['amount']
			acc.save()
			result = braintree.Transaction.sale({
				"amount": acc.amount,
				"payment_method_nonce": acc.payment_nonce
				})
			transaction_id = result.transaction.id
			acc.txnid = transaction_id
			acc.save()
			message = ''
			if result.is_success:
				acc.result = True
				acc.save()
				message =  'Transaction successfully completed'+' : '+ transaction_id
				varibles ={'message':message}
				return render(request, 'success.html',varibles)
			else:
				message = 'Error Transaction Faild'
				varibles = {'message':message,}
				return render(request, 'checkout.html',varibles)
		else:
			message = 'No transaction'

			varibles ={'message':message,}
			return render(request, 'checkout.html',varibles)



def subscription(request):
	rg = request.POST.get
	message = ''
	token = None
	customer_id = None
	if request.POST:
		if rg('fname') and rg('lname') and rg('cnumber') and rg('cvv') and rg('year') and rg('month'):
			client_token = braintree.ClientToken.generate()
		else:
			print ("enter valid page")
			message = 'Please enter valid form'
			varibles ={'message':message}
			return render(request, 'index.html', varibles)











