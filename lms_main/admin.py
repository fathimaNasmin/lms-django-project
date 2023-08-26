from django.contrib import admin


from . import models


# Register your models here.
class WhatYouWillLearnTabularInline(admin.TabularInline):
    model = models.WhatYouWillLearn


class RequirementTabularInline(admin.TabularInline):
    model = models.Requirement


class CourseAdmin(admin.ModelAdmin):
    inlines = (WhatYouWillLearnTabularInline,
               RequirementTabularInline
               )


admin.site.register(models.Category)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Level)
admin.site.register(models.Lesson)
admin.site.register(models.Video)
admin.site.register(models.Requirement)
admin.site.register(models.WhatYouWillLearn)
admin.site.register(models.SaveForLater)
admin.site.register(models.Cart)
admin.site.register(models.Order)
admin.site.register(models.OrderItems)
