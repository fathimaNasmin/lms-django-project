from django.contrib import admin


from . import models
from student.models import SaveForLater, Cart, Order, OrderItems
from instructor.models import Category,Level,Requirement,WhatYouWillLearn,Lesson


# Register your models here.
class WhatYouWillLearnTabularInline(admin.TabularInline):
    model = WhatYouWillLearn


class RequirementTabularInline(admin.TabularInline):
    model = Requirement


class CourseAdmin(admin.ModelAdmin):
    inlines = (WhatYouWillLearnTabularInline,
               RequirementTabularInline
               )


admin.site.register(Category)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Level)
admin.site.register(Lesson)
admin.site.register(models.Video)
admin.site.register(Requirement)
admin.site.register(WhatYouWillLearn)
admin.site.register(SaveForLater)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItems)
