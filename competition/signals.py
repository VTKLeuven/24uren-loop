from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_eventstream import send_event

from .models import QueueTicket, Lap
from .serializers import *

from .services import GroupService, CounterService


@receiver(post_save, sender=QueueTicket)
def post_save_queue_ticket(sender, instance, **kwargs):
    if instance.__sse__:
        count = CounterService.get_and_increment('queue_op')
        send_event('competition', 'queue_update', {
            'data': QueueTicketSerializer(instance).data,
            'id': count,
        })


@receiver(post_delete, sender=QueueTicket)
def post_delete_queue_ticket(sender, instance, **kwargs):
    if instance.__sse__:
        count = CounterService.get_and_increment('queue_op')
        send_event('competition', 'queue_delete', {
            'data': QueueTicketSerializer(instance).data,
            'id': count,
        })


@receiver(post_save, sender=Lap)
def post_save_lap(sender, instance, **kwargs):
    if instance.runner.group:
        GroupService.update_score(instance.runner.group)
    if instance.__sse__:
        send_event('competition', 'lap_update', {
            'data': LapSerializer(instance).data,
        })


@receiver(post_delete, sender=Lap)
def post_delete_lap(sender, instance, **kwargs):
    if instance.runner.group:
        GroupService.update_score(instance.runner.group)
    if not hasattr(instance, '__sse__') or instance.__sse__:
        send_event('competition', 'lap_delete', {
            'data': LapSerializer(instance).data,
        })


