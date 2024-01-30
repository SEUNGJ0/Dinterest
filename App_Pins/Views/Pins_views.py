from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from App_Auth.Auth_views import check_users_token
from ..models import Pins, Comment, Like
from ..serializers import PinSerializer, CommentSerializer, LikeSerializer

class PinsListView(APIView):
    serializer_class = PinSerializer
    
    def get(self, request):
        pins = Pins.objects.all()
        serializer = PinSerializer(pins, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = check_users_token(request)
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid(raise_exception=False):
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PinsDetailView(APIView):
    serializer_class = PinSerializer

    def get(self, request, pin_id):
        try:
            pin = Pins.objects.get(id = pin_id)
            comments = Comment.objects.filter(pin = pin)
            likes = Like.objects.filter(pin = pin)

            # serializer.data를 Python 사전으로 변환
            serializer = PinSerializer(pin)
            response_data = dict(serializer.data)
            
            # 댓글들을 직렬화한 후 리스트로 변환하여 추가
            comments_data = CommentSerializer(comments, many=True).data
            response_data['comments_count'] = len(comments_data)

            # 좋아요들을 직렬화한 후 리스트로 변환하여 추가
            likes_data = LikeSerializer(likes, many=True).data
            response_data['likes_count'] = len(likes_data)

            return Response(response_data, status=status.HTTP_200_OK)
        except:
            return Response({'error_message' : '잘못된 접근입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pin_id):
        try:
            user = check_users_token(request)
            pin = Pins.objects.get(id=pin_id)
        
            # 권한 체크: 해당 댓글의 작성자 또는 관리자만 수정 가능
            if user == pin.user or user.is_admin:
                # partial=True는 Django REST framework의 Serializer에서 사용되는 옵션 중 하나
                # 이 옵션을 사용하면 부분 업데이트(partial update)가 가능해진다.
                serializer = self.serializer_class(pin, data=request.data, partial=True)
 
                if serializer.is_valid():
                    serializer.save(user=user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': '권한이 없습니다.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Pins.DoesNotExist:
            return Response({'error_message': '수정할 핀이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pin_id):
        try:
            user = check_users_token(request)
            pin = Pins.objects.get(id=pin_id)

            # 권한 체크: 해당 댓글의 작성자 또는 관리자만 삭제 가능
            if user == pin.user or user.is_admin:
                pin.delete()
                return Response({'message': '핀이 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error_message': '권한이 없습니다.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({'error_message': '삭제할 핀이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        

        