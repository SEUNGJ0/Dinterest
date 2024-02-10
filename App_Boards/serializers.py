from .models import Board, Ideas
from rest_framework import serializers

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','name', 'user']


class IdeasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ideas
        fields = ['id', 'pin','board', 'user']