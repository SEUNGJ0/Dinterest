from django.db import models
from App_Auth.models import User
from App_Pins.models import Pins


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Ideas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pins, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True)
