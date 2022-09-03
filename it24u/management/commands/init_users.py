from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
  help = 'Initialise basic users in the database'

  def handle(self, *args, **options):
    print('Initialising basic users...')
    User.objects.create_superuser('admin', 'it@vtk.be', 'admin')
    User.objects.create_user('user', '', 'user')
    print('Initialised basic users')

