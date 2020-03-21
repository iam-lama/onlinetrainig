# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver 
from accounts.models import User
from accounts.choices import *
from django.utils.text import Truncator

from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator


# Create your models here.

class Course(models.Model):
	course_name = models.CharField(max_length=200)
	description = models.TextField(max_length=4000, default="This is a default descriptin")
	price = models.FloatField(max_length=4)
	begin_date = models.DateField() #Date without (Time) value
	end_date = models.DateTimeField()
	#use '' with class name in 'Tutors' cause it is not defined yet 
	#tutor = models.ForeignKey('Tutors', related_name='courses', on_delete=models.PROTECT)
	#verbose_name of "", because we don't want the name of the field appearing next to the video upload button
	video = models.FileField(upload_to='videos/', null=True, verbose_name="", blank=True)

	def __str__(self):
		return self.course_name

	# def __str__(self):
	# 	truncated_description = Truncator(self.description)
	# 	return truncated_description.chars(30)

	def get_description_as_markdown(self):
		return mark_safe(markdown(self.description, safe_mode='escape'))

class Certificate(models.Model):
	course = models.ForeignKey(Course, related_name='certificates', on_delete=models.PROTECT)
	code = models.CharField(max_length=50, null=False)


class Tutor(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	mobile = PhoneNumberField(null=True, default="011")
	course = models.ForeignKey(Course, related_name='tutors', on_delete=models.PROTECT,null=True)

	# @receiver(post_save, sender=User)
	# def create_user_profile(sender, instance, created, **kwargs):
	# 	if created:
	# 		Tutors.objects.Create(user=instance)

	# @receiver(post_save, sender=User)
	# def save_user_profile(sender, instance, **kwargs):
	# 	instance.profile.save()


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user_profile')	
	country = models.CharField(max_length=100, null=True)
	region = models.CharField(max_length=100,null=True)
	sex = models.CharField(max_length=1,choices=Sex_Choice,null=True)
	# mobile = PhoneNumberField(unique=True,null=True, default="000")
	
	mobile_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")    
	mobile = models.CharField(validators=[mobile_regex], max_length=17,null=True, default="") # validators should be a list
	#^\+(?:[0-9]?){6,14}[0-9]$
	#^(\+\d{1,3})?,?\s?\d{8,13}
	id_num = models.PositiveIntegerField(unique=True,null=True)
	id_image = models.ImageField(upload_to='images/',null=True)		
	# course = models.ForeignKey(Course, related_name='students', on_delete=models.PROTECT,null=True)
	course = models.ManyToManyField(Course, related_name='students')
	certificate = models.ForeignKey(Certificate, related_name='students', on_delete=models.PROTECT,null=True)
	payment = models.ForeignKey('Accountant', related_name='students', on_delete=models.PROTECT,null=True)

	def __str__(self):
		return self.user.username


	# @receiver(post_save, sender=User)
	# def create_user_profile(sender, instance, created, **kwargs):
	# 	if created:
	# 		Students.objects.Create(user=instance)

	# @receiver(post_save, sender=User)
	# def save_user_profile(sender, instance, **kwargs):
	# 	instance.profile.save()

class Accountant(models.Model):
	student = models.ForeignKey(Student, related_name='accountants', on_delete=models.PROTECT, default=0)
	payment_nonce = models.CharField(max_length=100,null=True,blank=True)
	amount = models.CharField(max_length=100,null=True,blank=True)
	txnid = models.CharField(max_length=25,null=True,blank=True)
	result = models.BooleanField(default=False)

	def __str__(self):
		return self.student.first_name 

	# account_number = models.CharField(max_length=30)
	# account_name = models.CharField(max_length=30)
	# bank_number = models.CharField(max_length=30)
	# transfer_amount = models.FloatField()
	# transfer_date = models.DateTimeField(auto_now_add=True)
	# transfer_image = models.ImageField(upload_to='images/')

class Braintree(models.Model):
	student = models.ForeignKey(Student, related_name='braintree', on_delete=models.PROTECT, default=0)
	client_token = models.TextField(verbose_name=u'client token', max_length=500)
	payment_once = models.CharField(max_length=100,null=True,blank=True)
	customer_id = models.CharField(max_length=25,null=True,blank=True)
	payment_mode = models.BooleanField(default=False)

# class Contract(models.Model):
# 	#student = models.ForeignKey(Student, related_name='contracts', on_delete=models.PROTECT)
# 	course = models.ForeignKey(Course, related_name='contracts', on_delete=models.PROTECT)
# 	first_payment = models.FloatField(null=True)
# 	seconed_payment = models.FloatField(null=True)

class Page(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=4000)


