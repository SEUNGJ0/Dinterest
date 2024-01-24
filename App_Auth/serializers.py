from rest_framework import serializers
from App_Auth.models import User

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
