from rest_framework import viewsets, filters, serializers, status
from rest_framework.decorators import action, parser_classes

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models import Subquery, Min, Count, F, OuterRef, Prefetch
from django.utils.dateparse import parse_datetime

from .models import *
from .serializers import *
from .services import *
from .filters import *
from .permissions import *


def apply_query_limit(request, queryset):
    limit = request.query_params.get('limit', None)
    if limit is not None:
        try:
            limit = int(limit)
            if limit <= 0:
                raise ValueError()
            return queryset[:limit]
        except ValueError:
            raise ValidationError({'limit': 'The limit should be a non-negative integer'})
    return queryset


def parse_boolean(b):
    if isinstance(b, str):
        return bool(b) and b.lower() != 'false'
    elif isinstance(b, bool):
        return b
    else:
        raise ValueError()


class RunnerViewSet(viewsets.ModelViewSet):
    queryset = Runner.objects.all()
    serializer_class = RunnerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, LimitFilter, OffsetFilter]
    ordering_fields = '__all__'
    filter_fields = {
        'identification': ['exact'],
        'first_name': ['exact'],
        'last_name': ['exact'],
        'university': ['exact'],
        'group': ['exact'],
        'registration_time': ['gte', 'lte', 'gt', 'lt'],
    }

    @action(detail=False, methods=['get'])
    def top_runners(self, request):
        runners = Runner.objects.annotate(fastest=Min('laps__duration')).order_by('fastest')
        runners = apply_query_limit(request, runners)
        for runner in runners:
            runner.fastest_lap = runner.laps.order_by('duration').first()
        return Response(RunnerSerializer(runners, many=True, extra_fields={'fastest_lap': LapSerializer(rm_fields={'runner'})}).data)


    @action(detail=False, methods=['get'])
    def most_active(self, request):
        runners = Runner.objects.filter(laps__duration__isnull=False).annotate(lapcount=Count('laps')).order_by('-lapcount')
        runners = apply_query_limit(request, runners)
        return Response(RunnerSerializer(runners, many=True, extra_fields={'lapcount': serializers.IntegerField()}).data)

    @action(detail=False, methods=['get'])
    def most_active_first_year(self, request):
        runners = Runner.objects.filter(first_year=True, laps__duration__isnull=False).annotate(
            lapcount=Count('laps')).order_by('-lapcount')
        runners = apply_query_limit(request, runners)
        return Response(
            RunnerSerializer(runners, many=True, extra_fields={'lapcount': serializers.IntegerField()}).data)

    def get_permissions(self):
        return [RestBasePermission('runner', self.action) | IsOpen('runner', self.action)]


class LapViewSet(viewsets.ModelViewSet):
    queryset = Lap.objects.all()
    serializer_class = LapSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, LimitFilter, OffsetFilter]
    ordering_fields = '__all__'
    filter_fields = {
        'duration': ['gte', 'lte', 'gt', 'lt', 'isnull'],
        'start_time': ['gte', 'lte', 'gt', 'lt'],
        'runner': ['exact'],
        'ticket': ['exact'],
        'id': ['exact', 'gte', 'lte', 'gt', 'lt'],
    }

    @action(detail=False, methods=['post'])
    def advance(self, request):
        now = request.data.get('now', None)
        if now is not None:
            now = parse_datetime(now)

        # Advance a lap
        LapService.advance(now=now)

        # Return the response
        return Response({'success': True})

    @action(detail=False, methods=['post'])
    def reverse(self, request):
        # Reverse a lap
        LapService.reverse()

        return Response({'success': True})

    @action(detail=False, methods=['get'])
    def lap_count(self, request):
        id = request.query_params.get('id')
        lapcount = Lap.objects.filter(runner__id=id, duration__isnull=False).count()
        return Response({'lap_count': lapcount})

    @action(detail=False, methods=['get'])
    def polkadot_scoreboard(self, request):
        scoreboard = LapService.get_polkadot_scoreboard()
        scoreboard = apply_query_limit(request, scoreboard)
        return Response(scoreboard)

    def get_permissions(self):
        return [RestBasePermission('lap', self.action) | IsOpen('lap', self.action)]


class QueueTicketViewSet(viewsets.ModelViewSet):
    queryset = QueueTicket.objects.all().order_by('id')
    serializer_class = QueueTicketSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, LimitFilter, OffsetFilter]
    ordering_fields = '__all__'
    filter_fields = {
        'runner': ['exact'],
        'registration_time': ['gte', 'lte', 'gt', 'lt'],
        'id': ['exact', 'gte', 'lte', 'gt', 'lt'],
        'deleted': ['exact'],
        'ran': ['exact']
    }

    def destroy(self, request, pk=None):
        count = Counter.objects.filter(name='queue_op').first().count
        if request.data.get('id') == count:
            QueueTicketService.soft_delete(pk)
            return Response({'success': True})
        else:
            return Response({'success': False})

    @action(detail=False, methods=['post'])
    @parser_classes([JSONParser])
    def move(self, request):
        data = request.data.get('data')
        pos_move = data.get('pos_move')
        pos_target = data.get('pos_target')

        count = Counter.objects.filter(name='queue_op').first().count
        if request.data.get('id') == count:
            QueueTicketService.move_pos_to_pos(pos_move, pos_target)
            return Response({'success': True})
        else:
            return Response({'success': False})

    def get_permissions(self):
        return [RestBasePermission('queueticket', self.action) | IsOpen('queueticket', self.action)]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def top_groups(self, request):
        groups = Group.objects.order_by('-score')
        groups = apply_query_limit(request, groups)
        return Response(GroupSerializer(groups, many=True).data)

    def get_permissions(self):
        return [RestBasePermission('group', self.action) | IsOpen('group', self.action)]


class HappyHourViewSet(viewsets.ModelViewSet):
    queryset = HappyHour.objects.all()
    serializer_class = HappyHourSerializer

    def get_permissions(self):
        return [RestBasePermission('happyhour', self.action) | IsOpen('happyhour', self.action)]


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

    def get_permissions(self):
        return [RestBasePermission('university', self.action) | IsOpen('university', self.action)]


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

    @action(detail=False, methods=['get'])
    def no_shift_after(self, request):
        date = request.query_params.get('datetime')
        if date is None:
            date = datetime.datetime.now(datetime.timezone.utc)
        else:
            date = parse_datetime(date.replace(' ', '+'))
        runners = Runner.objects.filter(shifts__isnull=False).exclude(shifts__end_time__gte=date)
        return Response(RunnerSerializer(runners, many=True).data)

    @action(detail=False, methods=['get'])
    def list_runners(self, request):
        shift_id = request.query_params.get('id')
        filter_queue = parse_boolean(request.query_params.get('filter_queue', False))

        runners = Runner.objects.filter(shifts__id=shift_id)
        if filter_queue:
            runners = runners.exclude(id__in=QueueTicket.objects.all().values('runner'))
        return Response(RunnerSerializer(runners, many=True).data)

    def get_permissions(self):
        return [RestBasePermission('shift', self.action) | IsOpen('shift', self.action)]


class CounterViewSet(viewsets.ModelViewSet):
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = {
        'name': ['exact'],
    }

    def get_permissions(self):
        return [RestBasePermission('counter', self.action) | IsOpen('counter', self.action)]

class RainStatusViewSet(viewsets.ModelViewSet):
    queryset = RainStatus.objects.all()
    serializer_class = RainStatusSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    filter_fields = {
        'is_raining': ['exact'],
    }

    @action(detail=False, methods=['get'])
    def current_status(self, request):
        try:
            rain_status = RainStatus.objects.first()
            if not rain_status:
                return Response({'error': 'Rain status not found'}, status=404)
            serializer = RainStatusSerializer(rain_status)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    @action(detail=False, methods=['put'])
    def update_status(self, request):
        try:
            rain_status = RainStatus.objects.first()
            if not rain_status:
                return Response({'error': 'Rain status not found'}, status=404)
            rain_status.is_raining = request.data.get('is_raining', rain_status.is_raining)
            rain_status.save()
            serializer = RainStatusSerializer(rain_status)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def get_permissions(self):
        return [RestBasePermission('rainstatus', self.action) | IsOpen('rainstatus', self.action)]