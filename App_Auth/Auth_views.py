from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from App_Auth.models import User
from App_Auth.serializers import UsersSerializer

class UserList(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UsersSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
