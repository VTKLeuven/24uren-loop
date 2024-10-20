from django.conf.urls import url, include
from rest_framework import routers
from django.shortcuts import render

from .viewsets import *
from .views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'lap', LapViewSet)
router.register(r'group', GroupViewSet)
router.register(r'university', UniversityViewSet)
router.register(r'happyhour', HappyHourViewSet)
router.register(r'runner', RunnerViewSet, basename='runner-case-insensitive')
router.register(r'queue-ticket', QueueTicketViewSet)
router.register(r'shift', ShiftViewSet)
router.register(r'counter', CounterViewSet)
router.register(r'rain_status', RainStatusViewSet, basename='rain_status')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-auth/info/', UserInfo.as_view()),
    url(r'^$', lambda request: render(request, 'index.html')),
    url(r'^.*/$', lambda request: render(request, 'index.html')),
]
