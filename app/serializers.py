from rest_framework import serializers
from .models import users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['username', 'description']
