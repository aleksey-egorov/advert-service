from django.contrib import admin
from .models import Lot, LotGallery, Currency

# Register your models here.

admin.site.register(Lot)
admin.site.register(LotGallery)
admin.site.register(Currency)