from App_Auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserJWTSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','password','birth','gender','country','language']
    
    def save(self, request):
        user = super().save()
        user.email = self.validated_data.get('email', '')
        user.birth = self.validated_data.get('birth', None)
        user.gender = self.validated_data.get('gender', None)
        user.country = self.validated_data.get('country', None)
        user.language = self.validated_data.get('language', None)

        user.set_password(self.validated_data['password'])
        user.save()

        return user

    def validate(self, attrs):
        # 전달받은 attrs에서 이메일 추출
        email = attrs.get('email', None)
        # 이메일이 존재하는지 확인
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError('해당 이메일은 이미 사용 중 입니다.')
        
        return attrs
    

class UserJWTLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        write_only=True,
        )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id','email', 'password']

    def validate(self, attrs):
        # 전달받은 attrs에서 이메일과 패스워드 추출
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        # 이메일이 존재하는지 확인
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('해당 이메일을 사용하는 유저가 존재하지 않습니다.')

        # 패스워드 일치 여부 확인
        if not user.check_password(password):
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')

        # 유효한 경우에는 RefreshToken을 이용하여 토큰 생성
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        # 결과를 attrs에 업데이트하여 반환
        attrs = {
            'email': user,
            'password':password,
            'refresh_token': refresh_token,
            'access_token': access_token,
        }
        
        return attrs
