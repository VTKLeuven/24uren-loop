from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils.timezone import now
import datetime

from competition.models import *

class Command(BaseCommand):
  help = 'Create basic dummy laps for competition'

  def handle(self, *args, **options):
    print('Creating competition dummy laps...')

    runner = Runner.objects.first()

    for i in range(1000):
      ticket = QueueTicket(runner=runner, registration_time=now(), deleted=False, ran=True)
      ticket.save()
      lap = Lap(ticket=ticket, runner=runner, start_time=now(), duration=datetime.timedelta(seconds=1))
      lap.save()

    print('Competition dummy laps created')
