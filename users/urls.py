from django.urls.conf import path
from .views import users

urlpatterns = [
    path('users/', users),
]
