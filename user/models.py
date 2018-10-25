import datetime
import logging
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

from supplier.models import Supplier
from geo.models import Region

# Custom user class

class User(AbstractUser):
    '''Зарегистрированный пользователь'''
    logger = logging.getLogger('advert.user')

    email = models.EmailField(null=True, blank=True, default='')
    phone = models.CharField(null=True, blank=True, default='')
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/')
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey('geo.Region', on_delete=models.SET_NULL, null=True, blank=True)
    register_date = models.DateField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @staticmethod
    def add_user(cleaned_data):
        with transaction.atomic():
            new_user = User(
                username=cleaned_data['login'],
                password=make_password(cleaned_data['password']),
                email=cleaned_data['email'],
                avatar=cleaned_data['avatar'],
            )
            new_user.save()
            return new_user

    def update_user(self, user, cleaned_data):
        try:
            with transaction.atomic():
                supplier = Supplier.objects.get(id=cleaned_data['supplier'])
                region = Region.objects.get(id=cleaned_data['region'])
                upd_user = User(
                    id=user.id,
                    email=cleaned_data['email'],
                    phone=cleaned_data['phone'],
                    supplier=supplier,
                    region=region,
                    avatar=cleaned_data['avatar']
                )
                upd_user.save(update_fields=['email', 'phone', 'supplier', 'region', 'avatar'])
                return upd_user
        except Exception as err:
            self.logger.error(err)
        #return True

