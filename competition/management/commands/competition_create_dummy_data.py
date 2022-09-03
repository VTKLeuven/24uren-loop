from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from competition.models import Runner, University

class Command(BaseCommand):
  help = 'Create basic dummy data for competition'

  def handle(self, *args, **options):
    print('Creating competition dummy data...')

    if User.objects.filter(username='competition').count() == 0:
      user = User.objects.create_user('competition', 'it@vtk.be', 'competition')
      user.groups.set([Group.objects.get(name='competition')])
      user.save()

    if User.objects.filter(username='admin').count() == 0:
      superuser = User.objects.create_superuser(
            username='admin',
            email='admin@vtk.be',
            password='admin')
      superuser.save()

    for i in range(20):
      id = f'r00000{str(i) if i >= 10 else "0"+str(i)}'
      if Runner.objects.filter(identification=id).count() == 0:
        runner = Runner(first_name=f'IT ({i})', last_name='VTK', identification=id,
                        university=University.objects.first())
        runner.save()

    print('Competition dummy data created')
