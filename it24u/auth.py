
from rest_framework.authentication import BasicAuthentication


class XBasicAuth(BasicAuthentication):
    def authenticate_header(self, request):
        return 'XXXBasic'
