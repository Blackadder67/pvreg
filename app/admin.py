from django.contrib import admin
from .models import Person, Product, INN, PhTherGroup

admin.site.register(Person)
admin.site.register(Product)
admin.site.register(INN)
admin.site.register(PhTherGroup)


# Register your models here.
