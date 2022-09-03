from django.contrib import admin
from django.http import HttpResponse, StreamingHttpResponse
import itertools

from .models import *
import csv

admin.site.register(Group)
admin.site.register(University)
admin.site.register(Shift)
admin.site.register(Counter)


class Echo:
    def write(self, value):
        return value


@admin.register(Runner)
class RunnerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'identification']


@admin.register(Lap)
class LapAdmin(admin.ModelAdmin):
    search_fields = ['runner__first_name', 'runner__last_name', 'runner__identification']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        writer = csv.writer(Echo())
        response = StreamingHttpResponse(
            itertools.chain((writer.writerow(field_names),), 
            (writer.writerow([getattr(obj, field) for field in field_names]) for obj in queryset)),
            content_type='text/csv', 
        )
        response['Content-Disposition'] = 'attachment; filename="laps.csv"'

        return response

    export_as_csv.short_description = "Export Selected"

    actions = ["export_as_csv"]
    list_per_page = 1000

@admin.register(QueueTicket)
class QueueTicketAdmin(admin.ModelAdmin):
    list_filter = [
        "deleted", "ran"
    ]


@admin.register(Criterium)
class CriteriumAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(base=False)


@admin.register(HappyHour)
class HappyHourAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(base=False)
