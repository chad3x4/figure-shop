from django.urls import path, re_path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('lessons', views.LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    path('test/', views.TestView.as_view()),
    re_path(r'^(?P<course_id>[0-9]{1})/$', views.course_detail)
]
