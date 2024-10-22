from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone

now = timezone.now()

from datetime import timedelta

from competition.models import University, Criterium, HappyHour, Counter, RainStatus


class Command(BaseCommand):
  help = 'Initialise basic competition data in the database'

  def handle(self, *args, **options):
    print('Initialising competition...')
    group = Group.objects.create(name='competition')
    group.permissions.set(Permission.objects.filter(codename__startswith="rest"))
    group.save()

    University.objects.create(full_name="Katholieke Universiteit Leuven", abbreviation="KUL")

    Criterium.objects.create(base=True, score=0, upper_limit=timedelta())
    HappyHour.objects.create(base=True, multiplier=1, name='Base', start_time=timezone.now(), end_time=timezone.now())
    RainStatus.objects.create(is_raining=False)

    Counter.objects.create(name='queue_op', count=0)
    print('Competition initialised')


