from django.contrib import admin
from .models import *
# Register your models here.

class LectureAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "video_duration")

class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "title")



admin.site.register(User)
admin.site.register(Student)
admin.site.register(Language)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Instructor)
admin.site.register(Review)
admin.site.register(Level)
admin.site.register(Filter)
admin.site.register(Section, SectionAdmin)
admin.site.register(Payment)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Coupon)
admin.site.register(Lecture, LectureAdmin)
