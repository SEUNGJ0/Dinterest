from django.db import models
from App_Auth.models import User

class Pins(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    source_url = models.URLField(null=True)
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_data = models.DateTimeField(auto_now=True)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pins, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_data = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pins, on_delete=models.CASCADE)
    
    # 좋아요 중복 방지
    class Meta:
        unique_together = ['user', 'pin']
