from django.urls.conf import path
from .views import register, users, login, AuthenticatedUser

urlpatterns = [
    path('users/', users),
    path('register/', register),
    path('login/', login),
    path('user/', AuthenticatedUser.as_view()),
]
