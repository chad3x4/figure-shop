from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound
from django.template.response import TemplateResponse
from django.views import View
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Course, Lesson
from .paginator import BasePagination
from .serializers import CourseSerializer, LessonSerializer


# Create your views here.


def index(request):
    return HttpResponse("e-Course App")


def course_detail(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("<h1>Not found</h1>")

    return TemplateResponse(request, 'admin/detail.html', {'course': course})


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    pagination_class = BasePagination

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonSerializer
    pagination_class = BasePagination

    @action(methods=['post'], detail=True, url_path="hide-lesson")
    def hide_lesson(self, request, pk):
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=LessonSerializer(l).data,
                        status=status.HTTP_200_OK)


class TestView(View):
    def get(self, request):
        return HttpResponse("TESTING")

    def post(self, request):
        pass
