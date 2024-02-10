from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Board, Ideas
from .serializers import BoardSerializer, IdeasSerializer

from App_Auth.Auth_views import check_users_token

class BoardListView(APIView):
    serializer_class = BoardSerializer

    def get(self, request):
        user = check_users_token(request)
        board = Board.objects.filter(user = user)
        if board:
            serializer = BoardSerializer(board, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error_message' : '생성한 보드가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = check_users_token(request)

        if serializer.is_valid():
            serializer.save(user = user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetailView(APIView):
    serializer_class = IdeasSerializer

    def get(self, request, board_id):
        user = check_users_token(request)
        board = Board.objects.get(id = board_id)

        if user == board.user or user.is_admin:
            ideas = Ideas.objects.filter(board = board)
            
            if ideas:
                serializer = IdeasSerializer(ideas, many = True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message' : f'{board} 보드가 비어있습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error message':'잘못된 접근입니다.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

  
    def post(self, request, board_id):
        user = check_users_token(request)
        board = Board.objects.get(id = board_id)

        print(request.data)
        ideas_data = request.data.copy()
        ideas_data['user'] = user.id
        ideas_data['board'] = board.id
        print(ideas_data)

        serializer = self.serializer_class(data = ideas_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IdeasListView(APIView):

    def get(self, request, board_id):
        pass

    def post(self, request, board_id):
        pass

class IdeasDetailView(APIView):

    def get(self, request, idea_id):
        pass

    def patch(self, request, idea_id):
        pass

    def delete(self, request, idea_id):
        pass