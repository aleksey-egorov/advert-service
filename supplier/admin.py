from django.contrib import admin
from .models import Supplier, SupplierOrg

# Register your models here.

admin.site.register(Supplier)
admin.site.register(SupplierOrg)