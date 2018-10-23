from django.db import models

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=80)
    fednum = models.CharField(max_length=5)
    kladr_code = models.CharField(max_length=15)
    okato = models.CharField(max_length=12)
    aoguid = models.CharField(max_length=40)
    aoid = models.CharField(max_length=40)
    active = models.BooleanField('Активность', default=False, null=True, blank=True)

