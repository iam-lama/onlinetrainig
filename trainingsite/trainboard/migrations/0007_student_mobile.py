# Generated by Django 2.2.1 on 2019-09-08 15:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainboard', '0006_remove_student_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='mobile',
            field=models.CharField(default='', max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^(\\+\\d{1,3})?,?\\s?\\d{8,13}')]),
        ),
    ]