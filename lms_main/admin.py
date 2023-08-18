from django.contrib import admin


from . import models


# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.Course)
admin.site.register(models.Level)
admin.site.register(models.Requirement)
