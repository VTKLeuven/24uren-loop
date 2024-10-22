from django.db import models
from django.core.validators import RegexValidator
from django.db.models.fields import related
from django.utils import timezone

identification_validator = RegexValidator('^r[0-9]{7}$', "This is not a valid university identification number.")


def rest_permissions(model):
    return [
        ('rest_list_' + str(model), 'Can list in REST'),
        ('rest_retrieve_' + str(model), 'Can retrieve in REST'),
        ('rest_create_' + str(model), 'Can create in REST'),
        ('rest_update_' + str(model), 'Can update in REST'),
        ('rest_destroy_' + str(model), 'Can delete in REST'),
    ]


class University(models.Model):
    full_name = models.CharField(max_length=30)
    abbreviation = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = 'Universities'
        permissions = rest_permissions('university')

    def __str__(self):
        return f"{self.full_name} ({self.abbreviation})"


class Runner(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    identification = models.CharField(
        validators=[
            identification_validator
        ],
        max_length=8,
        unique=True
    )
    university = models.ForeignKey('University', null=True, blank=True, on_delete=models.PROTECT)
    registration_time = models.DateTimeField(blank=True)
    group = models.ForeignKey('Group', null=True, blank=True, on_delete=models.SET_NULL)
    test_time = models.DurationField(null=True, blank=True)
    shifts = models.ManyToManyField('Shift', blank=True)
    first_year = models.BooleanField(null=True, blank=True)

    class Meta:
        permissions = rest_permissions('runner') + [
            ('rest_top_runners_runner', 'Can view top runners in REST'),
            ('rest_most_active_runner', 'Can view most active runners in REST')
        ]

    def save(self, *args, **kwargs):
        self.identification = self.identification.lower()
        if not self.id:
            self.registration_time = timezone.now()
        return super(Runner, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.identification})"


class QueueTicketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete(*args, **kwargs)
        return super().delete(*args, **kwargs)


class QueueTicket(models.Model):
    objects = QueueTicketQuerySet.as_manager()
    runner = models.ForeignKey('Runner', blank=False, on_delete=models.PROTECT)
    registration_time = models.DateTimeField(blank=True)
    deleted = models.BooleanField(default=False)
    ran = models.BooleanField(default=False)

    class Meta:
        permissions = rest_permissions('queueticket') + [
            ('rest_move_queueticket', 'Can move a ticket in REST')
        ]

    def save(self, *args, **kwargs):
        self.__sse__ = kwargs.pop('__sse__', True)
        if not self.id:
            self.registration_time = timezone.now()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.__sse__ = kwargs.pop('__sse__', True)
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.runner.first_name} {self.runner.last_name} ({self.id})'


class LapQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete(*args, **kwargs)
        return super().delete(*args, **kwargs)


class Lap(models.Model):
    objects = LapQuerySet.as_manager()
    runner = models.ForeignKey('Runner', blank=False, on_delete=models.PROTECT, related_name='laps')
    ticket = models.OneToOneField('QueueTicket', blank=True, on_delete=models.PROTECT)
    start_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    raining = models.BooleanField(default=False)

    class Meta:
        permissions = rest_permissions('lap') + [
            ('rest_advance_lap', 'Can advance a lap in REST'),
            ('rest_reverse_lap', 'Can reverse a lap in REST'),
            ('rest_lap_count_lap', 'Can retrieve lap count in REST')
        ]

    def save(self, *args, **kwargs):
        self.__sse__ = kwargs.pop('__sse__', True)
        if not self.id:
            self.raining = RainStatus.objects.first().is_raining
        if self.ticket and self.ticket.ran is False:
            self.ticket.ran = True
            self.ticket.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.__sse__ = kwargs.pop('__sse__', True)
        if self.ticket and self.ticket.ran is True:
            self.ticket.ran = False
            self.ticket.save()
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.runner.first_name} {self.runner.last_name} ({self.duration})"


class Group(models.Model):
    name = models.CharField(max_length=30)
    happy_hours = models.ManyToManyField('HappyHour', blank=True)
    score = models.IntegerField(default=0, blank=False)

    class Meta:
        permissions = rest_permissions('group') + [
            ('rest_top_groups_group', 'Can view top groups in REST')
        ]

    def save(self, *args, **kwargs):
        self.meta = kwargs.pop('meta', None)
        self.__sse__ = kwargs.pop('__sse__', True)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.meta = kwargs.pop('meta', None)
        self.__sse__ = kwargs.pop('__sse__', True)
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.score})'


class HappyHour(models.Model):
    name = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    multiplier = models.IntegerField(default=1)
    base = models.BooleanField(default=False)

    class Meta:
        permissions = rest_permissions('happyhour')

    def __str__(self):
        return self.name


class Criterium(models.Model):
    upper_limit = models.DurationField()
    score = models.IntegerField()
    base = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Criteria'
        permissions = rest_permissions('criterium')

    def __str__(self):
        if self.base:
            return f'Base score is {self.score} points'
        else:
            return f"Under {self.upper_limit}s is {self.score} points"


class Shift(models.Model):
    name = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        permissions = rest_permissions('shift') + [
            ('rest_no_shift_after_shift', 'Can list all runners who have no shifter after specific time'),
            ('rest_list_runners_shift', 'Can list all runners in a specific shift')
        ]

    def __str__(self):
        return f'{self.name}'

class Counter(models.Model):
    name = models.CharField(max_length=20)
    count = models.IntegerField()

    class Meta:
        permissions = rest_permissions('counter')

    def __str__(self):
        return f'{self.name} ({self.count})'

class RainStatus(models.Model):
    is_raining = models.BooleanField(default=False)

    # Prevent pluralization
    class Meta:
        verbose_name = "Rain status"
        verbose_name_plural = "Rain status"