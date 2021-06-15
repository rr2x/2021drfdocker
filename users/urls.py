from django.urls.conf import path
from .views import (
    PermissionAPIView,
    RoleViewSet,
    AuthenticatedUser,
    UserGenericAPIView,
    ProfileInfoAPIView,
    ProfilePasswordAPIView,
    register,
    # users,
    login,
    logout
)

urlpatterns = [
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('user/', AuthenticatedUser.as_view()),
    path('permissions', PermissionAPIView.as_view()),
    path('roles', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create',

    })),
    path('roles/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('users/info', ProfileInfoAPIView.as_view()),
    path('users/password', ProfilePasswordAPIView.as_view()),
    path('users', UserGenericAPIView.as_view()),
    path('users/<str:pk>', UserGenericAPIView.as_view()),

]

# users/... needs to be in correct order like above, because the last part might get mistaken as <str:pk>
