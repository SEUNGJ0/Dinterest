from .models import Pins, Like, Comment
from rest_framework import serializers

class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pins
        fields = ['id','user','image', 'source_url', 'title', 'description']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'