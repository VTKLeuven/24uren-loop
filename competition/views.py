from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Group
from .serializers import GroupSerializer


@api_view(['POST'])
def create_group(request):
    group_name = request.data.get('name', 'New Group')
    group = Group.objects.create(name=group_name)
    serializer = GroupSerializer(group)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserInfo(APIView):
    def get(self, request, format=None):
        return Response(UserSerializer(request.user).data)


