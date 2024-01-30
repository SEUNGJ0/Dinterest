from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from App_Auth.Auth_views import check_users_token
from ..models import Pins, Comment
from ..serializers import CommentSerializer

class CommentListView(APIView):
    serializer_class = CommentSerializer

    def get(self, request, pin_id):
        comments = Comment.objects.filter(pin = pin_id)
        comment_serializer = CommentSerializer(comments, many = True)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, pin_id):
        serializer = self.serializer_class(data = request.data)
        user = check_users_token(request)
        pin = Pins.objects.get(id=pin_id)
        
        if serializer.is_valid(raise_exception=False):
            serializer.save(user=user, pin=pin)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentAllListView(APIView):
    def get(self, request):
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many = True)
        return Response(serializer.data)


class CommentDetailView(APIView):

    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except:
            return Response({'error_message': '해당 댓글은 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, comment_id):
        try:
            user = check_users_token(request)
            comment = Comment.objects.get(id=comment_id)
        
            # 권한 체크: 해당 댓글의 작성자 또는 관리자만 수정 가능
            if user == comment.user or user.is_admin:
                # partial=True는 Django REST framework의 Serializer에서 사용되는 옵션 중 하나
                # 이 옵션을 사용하면 부분 업데이트(partial update)가 가능해진다.
                serializer = CommentSerializer(comment, data=request.data, partial=True)
 
                if serializer.is_valid():
                    serializer.save(user=user, pin=comment.pin)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': '권한이 없습니다.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Comment.DoesNotExist:
            return Response({'error_message': '수정할 댓글이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, comment_id):
        try:
            user = check_users_token(request)
            comment = Comment.objects.get(id=comment_id)

            # 권한 체크: 해당 댓글의 작성자 또는 관리자만 삭제 가능
            if user == comment.user or user.is_admin:
                comment.delete()
                return Response({'message': '댓글이 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error_message': '권한이 없습니다.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except :
            return Response({'error_message': '삭제할 댓글이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
