from typing import Any, Dict
from django.db import models
from django.core.validators import (MinLengthValidator,MaxLengthValidator,MinValueValidator,MaxValueValidator)

class UserModel(models.Model):

    username: str = models.CharField(max_length=40,unique=True,editable=True,
	                validators=[ MaxLengthValidator(20,message='Username is too long'),
                    MinLengthValidator(8,message='Username is too short..')])
    emailAddr: str = models.EmailField(max_length=60, unique=True)
    updatesFrequency: str = models.CharField(max_length=100, editable=True)

    def __str__(self):
        return self.username

class FeedBack(models.Model):

    user: Any = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    review: str = models.TextField(max_length=500, editable=True)
    rating: int = models.IntegerField(editable=True, validators=[ MaxValueValidator(5,message='Not Available'),
                                                   MinValueValidator(1,message='Not available')])

    def __str__(self) -> str:
        return self.user.username


