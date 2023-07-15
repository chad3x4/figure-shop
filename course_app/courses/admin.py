from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.urls import path
from django.utils.html import mark_safe
from .models import Category, Course, Lesson, Tag


class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    fk_name = 'course'  # Find out which Foreign Key


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInlineAdmin, ]


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'  # attribute __all__ return list contains all fields in model
        # fields defines which fields can be edited

    content = forms.CharField(widget=CKEditorUploadingWidget)  # Override default CharField


class LessonTagInline(admin.TabularInline):
    model = Lesson.tags.through


class LessonAdmin(admin.ModelAdmin):
    form = LessonForm  # Replace forms.ModelForm by LessonForm
    list_display = ["id", "subject", "created_date", "active", "course"]  # Define which fields is displayed
    search_fields = ["subject", "created_date", "course__subject"]  # Define which fields is used to searched
    list_filter = ["subject", "course__subject"]
    inlines = [LessonTagInline, ]
    readonly_fields = ["avatar"]  # Add a ReadOnlyField to show the image

    def avatar(self, lesson):  # Define what ReadOnlyField "avatar" shows
        if lesson:
            return mark_safe("<img src='/static/{img_urls}' alt='{alt}' width='120'/>"
                             .format(img_urls=lesson.image.name, alt=lesson.subject))


class CourseAppAdminSite(admin.AdminSite):
    site_header = 'HỆ THỐNG QUẢN LÝ KHÓA HỌC'

    def get_urls(self):
        return [
            path('course-stats/', self.course_stats)
        ] + super().get_urls()

    def course_stats(self, request):
        return "Thống kê"


admin_site = CourseAppAdminSite('mycourse')

# Register your models here (to enable editing)
# admin.site.register(Category)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Lesson, LessonAdmin)
admin_site.register(Category)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
