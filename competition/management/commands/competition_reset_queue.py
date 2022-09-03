from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from competition.models import Runner, University, QueueTicket

class Command(BaseCommand):
  help = 'Reset queue for competition'

  def handle(self, *args, **options):
    print('Resetting queue...')

    for i in range(20):
      id = f'r00000{str(i) if i >= 10 else "0"+str(i)}'
      if Runner.objects.filter(identification=id).count() == 0:
        runner = Runner(first_name=f'IT ({i})', last_name='VTK', identification=id,
                        university=University.objects.first())
        runner.save()

    QueueTicket.objects.all().delete()
    for i in range(20):
      id = f'r00000{str(i) if i >= 10 else "0" + str(i)}'
      runner = Runner.objects.get(identification=id)
      ticket = QueueTicket(runner=runner)
      ticket.save()


    print('Competition queue reset')
