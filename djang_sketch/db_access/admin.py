import inspect

from django.contrib import admin

# Register your models here.
import db_access.models as models

for name,value in inspect.getmembers(models, inspect.isclass):
    if issubclass(value, models.models.Model):
        if name not in ["Game", "Privilege"]:
            admin.site.register(value)
