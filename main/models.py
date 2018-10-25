from django.db import models

from product.models import Category, Group

# Create your models here.



class Tag(models.Model):
    name = models.CharField(max_length=60)

