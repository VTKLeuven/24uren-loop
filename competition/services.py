from django.db import transaction
from django.db.models import OuterRef, Subquery, Q, Sum
from django.db.models.functions import TruncTime
from django.utils.timezone import localtime
from django.core.exceptions import ObjectDoesNotExist

from django_eventstream import send_event

from datetime import time

from .models import *
from .serializers import QueueTicketSerializer, GroupSerializer


class LapService:
    __model__ = Lap

    def __init__(self):
        pass

    @classmethod
    @transaction.atomic
    def advance(cls, *args, now=None, **kwargs):
        # Get object locks
        current_lap = Lap.objects.select_for_update().filter(duration__isnull=True).first()
        ticket = QueueTicket.objects.select_for_update().filter(deleted=False, ran=False).first()

        # Retrieve the current time in utc timezone
        now = now or timezone.now()

        # Check if there is a current lap
        if current_lap is not None:
            current_lap.duration = (now - current_lap.start_time)
            current_lap.save(*args, **kwargs)

        # Turn the first ticket into a lap
        if ticket is not None:
            new_lap = Lap(runner=ticket.runner, ticket=ticket, start_time=now)
            new_lap.save(*args, **kwargs)

    @classmethod
    @transaction.atomic
    def reverse(cls, *args, **kwargs):
        # Get object locks
        current_lap = Lap.objects.select_for_update().filter(duration__isnull=True).first()
        prev_lap = Lap.objects.select_for_update().filter(duration__isnull=False).order_by('-start_time').first()

        # Delete the lap
        current_lap.delete(*args, **kwargs)

        # Set last completed lap to current lap
        if prev_lap is not None:
            prev_lap.duration = None
            prev_lap.save(*args, **kwargs)

    @classmethod
    def get_polkadot_scoreboard(cls, *args, **kwargs):
        scoreboard = []
        runners = Runner.objects.all()
        for runner in runners:
            score = 0
            laps = Lap.objects.filter(runner=runner)
            for lap in laps:
                start_time = localtime(lap.start_time).time()

                if (start_time >= time(20, 0)) or (start_time < time(2, 0)):
                    score += 1
                elif (start_time >= time(2, 0)) and (start_time < time(4, 0)):
                    score += 3
                elif (start_time >= time(4, 0)) and (start_time < time(9, 0)):
                    score += 10
                elif (start_time >= time(9, 0)) and (start_time < time(12, 0)):
                    score += 5
                elif (start_time >= time(12, 0)) and (start_time < time(18, 0)):
                    score += 1
                elif (start_time >= time(18, 0)) and (start_time < time(20, 0)):
                    score += 3

                if lap.raining:
                    score += 5
            scoreboard.append(runner.first_name + ' ' + runner.last_name + " - " + str(score))

        sorted_scoreboard = sorted(scoreboard, key=lambda x: int(x.split(' - ')[1]), reverse=True)
        return sorted_scoreboard


class QueueTicketService:
    __model__ = QueueTicket

    def __init__(self):
        pass

    @classmethod
    def __copy_ticket__(cls, from_ticket, to_ticket):
        to_ticket.runner = from_ticket.runner
        to_ticket.registration_time = from_ticket.registration_time

    @classmethod
    def __swap_ticket__(cls, from_ticket, to_ticket, swap_ticket):
        cls.__copy_ticket__(from_ticket, swap_ticket)
        cls.__copy_ticket__(to_ticket, from_ticket)
        cls.__copy_ticket__(swap_ticket, to_ticket)

    @classmethod
    @transaction.atomic
    def insert_at_pos(cls, ticket, pos, *args, **kwargs):
        __sse__ = kwargs.get('__sse__', True)
        kwargs['__sse__'] = False

        ticket.save(*args, **kwargs)
        cls.move_to_pos(ticket.id, pos, *args, **kwargs)

        if __sse__:
            count = CounterService.get_and_increment('queue_op')
            send_event('competition', 'queue_insert', {
                'data': {
                    'ticket': QueueTicketSerializer(ticket).data,
                    'pos': pos,
                },
                'id': count,
            })

    @classmethod
    @transaction.atomic
    def move_to_pos(cls, id_move, pos, *args, **kwargs):
        pos_move = cls.__model__.objects.select_for_update().order_by('id').filter(id__lt=id_move).count()
        cls.move_pos_to_pos(pos_move, pos, *args, **kwargs)

    @classmethod
    @transaction.atomic
    def move_pos_to_pos(cls, pos_move, pos_target, *args, **kwargs):
        tickets = cls.__model__.objects.select_for_update().filter(deleted=False, ran=False)
        if pos_move > pos_target:
            tickets = tickets.order_by('id')[pos_target:pos_move+1]
        else:
            tickets = tickets.order_by('-id')
            length = tickets.count()
            tickets = tickets[length-pos_target-1:length-pos_move]

        __sse__ = kwargs.get('__sse__', True)
        kwargs['__sse__'] = False

        swap_ticket = QueueTicket()
        first_ticket = tickets.first()
        for ticket in tickets[1:]:
            cls.__swap_ticket__(first_ticket, ticket, swap_ticket)
            ticket.save(*args, **kwargs)
        first_ticket.save(*args, **kwargs)

        if __sse__:
            count = CounterService.get_and_increment('queue_op')
            send_event('competition', 'queue_move', {
                'data': {
                    'pos_move': pos_move,
                    'pos_target': pos_target,
                },
                'id': count,
            })

    @classmethod
    @transaction.atomic
    def swap(cls, id0, id1, *args, **kwargs):
        ticket0 = cls.__model__.objects.select_for_update().get(id=id0)
        ticket1 = cls.__model__.objects.select_for_update().get(id=id1)
        cls.__swap_ticket__(ticket0, ticket1, QueueTicket())
        ticket0.save(*args, **kwargs)
        ticket1.save(*args, **kwargs)

    @classmethod
    @transaction.atomic
    def swap_pos(cls, pos0, pos1, *args, **kwargs):
        tickets = cls.__model__.objects.select_for_update().order_by('id')[:max(pos0, pos1)]
        cls.swap(tickets[pos0], tickets[pos1], *args, **kwargs)

    @classmethod
    @transaction.atomic
    def soft_delete(cls, ticket_id, *args, **kwargs):
        ticket = QueueTicket.objects.select_for_update().get(pk=ticket_id)
        ticket.deleted = True
        ticket.save(*args, **kwargs)


class GroupService:
    __model__ = Group

    def __init__(self):
        pass

    @classmethod
    def update_score(cls, group, *args, **kwargs):
        members = Runner.objects.filter(group=group)
        total_score = 0

        for member in members:
            score = 0
            laps = Lap.objects.filter(runner=member)
            for lap in laps:
                start_time = localtime(lap.start_time).time()

                if (start_time >= time(20, 0)) or (start_time < time(2, 0)):
                    score += 1
                elif (start_time >= time(2, 0)) and (start_time < time(4, 0)):
                    score += 3
                elif (start_time >= time(4, 0)) and (start_time < time(9, 0)):
                    score += 10
                elif (start_time >= time(9, 0)) and (start_time < time(12, 0)):
                    score += 5
                elif (start_time >= time(12, 0)) and (start_time < time(18, 0)):
                    score += 1
                elif (start_time >= time(18, 0)) and (start_time < time(20, 0)):
                    score += 3

                if lap.raining:
                    score += 5

            total_score += score

        __sse__ = kwargs.get('__sse__', True)
        kwargs['__sse__'] = False

        group.score = total_score
        group.save(*args, **kwargs)

        if __sse__:
            send_event('competition', 'group_score_update', {
                'group': GroupSerializer(group).data
            })


class CounterService:
    __model__ = Counter

    def __init__(self):
        pass

    @classmethod
    @transaction.atomic
    def get_and_increment(cls, name):
        move_counter = Counter.objects.select_for_update().get(name=name)
        count = move_counter.count
        move_counter.count += 1
        move_counter.save()
        return count
