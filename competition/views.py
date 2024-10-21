from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer


class UserInfo(APIView):
    def get(self, request, format=None):
        return Response(UserSerializer(request.user).data)
