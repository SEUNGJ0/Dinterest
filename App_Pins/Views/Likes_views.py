from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from App_Auth.Auth_views import check_users_token
from ..models import Pins, Like
from ..serializers import LikeSerializer

class LikeListView(APIView):
    serializer_class = LikeSerializer

    def get(self, request, pin_id):
        queryset = Like.objects.filter(pin = pin_id)
        serializer = LikeSerializer(queryset, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pin_id):
        serializer = self.serializer_class(data = request.data)
        user = check_users_token(request)
        pin = Pins.objects.get(id=pin_id)
        
        if serializer.is_valid(raise_exception=False):
            serializer.save(user=user, pin=pin)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pin_id):
        try:
            user = check_users_token(request)
            like = Like.objects.get(pin=pin_id)

            # 권한 체크: 해당 댓글의 작성자 또는 관리자만 삭제 가능
            if user == like.user or user.is_admin:
                like.delete()
                return Response({'message': '좋아요 취소가 완료되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error_message': '권한이 없습니다.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except :
            return Response({'error_message': '잘못된 접근입니다.'}, status=status.HTTP_404_NOT_FOUND)

class LikeAllListView(APIView):
    def get(self, request):
        queryset = Like.objects.all()
        serializer = LikeSerializer(queryset, many = True)
        return Response(serializer.data)

class LikeDetailView(APIView):

    def get(self, request, like_id):
        try:
            like = Like.objects.get(id=like_id)
            serializer = LikeSerializer(like)
            return Response(serializer.data)
        except:
            return Response({'error_message': '잘못된 접근입니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, like_id):
        try:
            user = check_users_token(request)
            like = Like.objects.get(id=like_id)

            # 권한 체크: 해당 댓글의 작성자 또는 관리자만 삭제 가능
            if user == like.user or user.is_admin:
                like.delete()
                return Response({'message': '좋아요 취소가 완료되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error_message': '권한이 없습니다.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except :
            return Response({'error_message': '잘못된 접근입니다.'}, status=status.HTTP_404_NOT_FOUND)
