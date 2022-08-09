from django.contrib import admin
from .models import (UserModel, FeedBack)
# Register your models here.
admin.site.register(UserModel)
admin.site.register(FeedBack)
