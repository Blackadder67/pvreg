from django.contrib import admin
from .models import Person, Product, INN, PhTherGroup, Exam

admin.site.register(Person)
admin.site.register(Product)
admin.site.register(INN)
admin.site.register(PhTherGroup)

admin.site.register(Exam)


# Register your models here.
