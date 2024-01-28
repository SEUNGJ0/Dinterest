from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken

from App_Auth.models import User
from App_Auth.serializers import UserSerializer, UserJWTSignupSerializer, UserJWTLoginSerializer

def check_users_token(request):
    token = request.COOKIES.get('access_token')
    if token:
        try:
            untyped_token = UntypedToken(token)
            user = JWTAuthentication().get_user(untyped_token)
            return user
        except:
            raise InvalidToken({
                "detail": "토큰의 유효 기간이 지났습니다.",
                "token": token
            })
    else:
        raise InvalidToken({
            "detail": "토큰이 존재하지 않습니다.",
        })

class UserListView(APIView):
    def get(self, request):
        user = check_users_token(request)
        if user.is_staff:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error message' : '권한이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get(self, request):
        queryset = check_users_token(request)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    def patch(self, request):
        user = check_users_token(request)
        serializer = UserSerializer(user, data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class JWTSignupView(APIView):
    serializer_class = UserJWTSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid(raise_exception=False):
            # 시리얼라이저에서 유효성 검증을 성공한 경우
            user = serializer.save(request)
            # RefreshToken을 생성하여 access 및 refresh 토큰 생성
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            attrs = {
                'user_email': user.email,
                'message':'회원가입되었습니다.', 
                'jwt_token':{
                    'access_token':access_token,
                    'refresh_token':refresh_token 
                },
            }

            return Response(attrs, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JWTLoginView(APIView):
    serializer_class = UserJWTLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=False):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # 사용자 인증
            user = authenticate(request, email=email, password=password)
            # 인증 성공 시
            if user:
                access_token = serializer.validated_data['access_token']
                refresh_token = serializer.validated_data['refresh_token']
                
                # 응답에 포함될 데이터 설정
                attrs = {
                    'user_email': user.email,
                    'message':'로그인되었습니다.', 
                    'jwt_token':{
                        'access_token':access_token,
                        'refresh_token':refresh_token 
                        },
                    }
                
                # 응답 생성 
                response = Response(attrs, status=status.HTTP_200_OK)\
                # 토큰을 쿠키로 저장
                response.set_cookie("access_token", access_token, httponly=True)
                response.set_cookie("refresh_token", refresh_token, httponly=True)
                return response
            else:
                # 인증 실패 시
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)    
        else:
            # 유효성 검사 실패 시
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    def post(self, request):
        response = Response({'message': '로그아웃되었습니다.'}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response    
        
