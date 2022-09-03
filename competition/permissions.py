from rest_framework.permissions import BasePermission


VUE_VIEWS = {
    'index': {
        'open': True,
        'perms': ['list_lap', 'most_active_runner', 'top_runners_runner', 'top_groups_group'],
    },
    'queueUp': {
        'open': False,
        'perms': [],
    },
    'queue': {
        'open': True,
        'perms': ['list_queueticket', 'list_counter'],
    },
    'fullscreen': {
        'open': True,
        'perms': ['list_lap', 'list_queueticket', 'list_counter'],
    },
    'control': {
        'open': False,
        'perms': ['advance_lap', 'reverse_lap', 'list_lap'],
    },
}

OPEN_PERMISSIONS = {}


class BaseOperandPermission(BasePermission):
    def __or__(self, other):
        return OrPermission(self, other)


class OrPermission(BaseOperandPermission):
    def __init__(self, left, right):
        self.__left__ = left
        self.__right__ = right

    def has_permission(self, request, view):
        return self.__left__.has_permission(request, view) or self.__right__.has_permission(request, view)


class RestBasePermission(BaseOperandPermission):
    def __init__(self, model, action):
        self.__perm__ = f'competition.rest_{action}_{model}'

    def has_permission(self, request, view):
        return request.user.has_perm(self.__perm__)


class IsOpen(BaseOperandPermission):
    open_permissions = {perm for view in VUE_VIEWS.values() if view['open'] for perm in view['perms']}.union(OPEN_PERMISSIONS)

    def __init__(self, model, action):
        self.__perm__ = f'{str(action)}_{str(model)}'

    def has_permission(self, request, view):
        return self.__perm__ in self.open_permissions



