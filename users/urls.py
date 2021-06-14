from django.urls.conf import path
from .views import PermissionAPIView, RoleViewSet, register, users, login, logout, AuthenticatedUser

urlpatterns = [
    # path('users/', users),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('users/', users),
    path('user/', AuthenticatedUser.as_view()),
    path('permissions/', PermissionAPIView.as_view()),
    path('roles/', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create',

    })),
    path('roles/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]
