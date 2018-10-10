from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user class

class User(AbstractUser):
    '''Зарегистрированный пользователь'''
    email = models.EmailField(null=True, blank=True, default='')
    phone = models.EmailField(null=True, blank=True, default='')
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/')
    reg_date = models.DateField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


