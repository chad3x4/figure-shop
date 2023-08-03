from rest_framework.serializers import ModelSerializer
from .models import Course, Lesson, Tag


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "subject", "image", "created_date", "category"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'content', 'created_date', 'course', 'tags']
