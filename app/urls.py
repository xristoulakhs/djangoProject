from django.urls import path, include
from . import views


# URLConf
from .views import UserView


class UserAPIView:
    pass


urlpatterns = [
    path('index/', views.index),
]
