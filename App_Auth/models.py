from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# 사용자 생성 및 관리 기능을 구현
class UserManager(BaseUserManager):    
    use_in_migrations = True    
    # 파라미터를 받아서 새로운 사용자를 생성하고 저장
    def create_user(self, email, password, **extra_fields):        
        if not email:            
            raise ValueError('이메일은 필수입니다.')
        if not password:            
            raise ValueError('비밀번호는 필수입니다.')
 
        email=self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)        
        user.save(using=self._db)        
        return user

    # create_user를 호출하여 관리자 권한을 추가로 설정
    def create_superuser(self, email, password):        
        user = self.create_user(            
            email = self.normalize_email(email),             
            password = password,        
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 

LANGUAGE_CHOICES = (
    ('EN', "English"),
    ('KR', 'Korean')
)
GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)
COUNTRY_CHOICES = (
    ('US', 'United States'),
    ('KR', 'Korea')
)

class User(AbstractBaseUser, PermissionsMixin):    
    objects = UserManager()
    email = models.EmailField(max_length=255, unique=True, verbose_name='이메일')
    birth = models.DateField(default=None, null=True, blank=True, verbose_name='생일')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=None, null=True, blank=True, verbose_name='성별')
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, default=None, null=True, blank=True, verbose_name='국가')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default=None, null=True, blank=True, verbose_name='언어')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
 
    USERNAME_FIELD = 'email'    # -> 사용자 고유 식별 필드 설정
    REQUIRED_FIELDS = [] # -> 슈퍼유저를 생성할때 필요한 필드 설정
 
    def __str__(self):
        return self.email
 
    @property
    def is_staff(self):
        return self.is_admin
    