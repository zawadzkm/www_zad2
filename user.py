import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www_zad2.settings")
django.setup()

from django.contrib.auth.models import User

user = User.objects.create_user('test1', 'test1@mimuw.edu.pl', 'test1')
user.first_name = "User"
user.last_name = 'Test1'
user.save()