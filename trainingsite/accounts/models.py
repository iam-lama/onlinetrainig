# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class User(AbstractUser):
	is_tutor = models.BooleanField(default=False)
	is_student = models.BooleanField(default=False)
    