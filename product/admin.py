from django.contrib import admin
from .models import Product, Group, Category

# Register your models here.

admin.site.register(Product)
admin.site.register(Group)
admin.site.register(Category)
