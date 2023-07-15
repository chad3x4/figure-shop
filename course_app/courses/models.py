from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')


class ItemBase(models.Model):
    class Meta:
        abstract = True  # Make this model abstract (migrate won't create a table)

    subject = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)


class Course (ItemBase):
    class Meta:
        unique_together = ('subject', 'category')  # This Meta Option check if the combination of them is unique
        ordering = ["subject", "created_date"]  # Sort rows in order

    description = models.TextField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, db_index=True, null=True)

    def __str__(self):
        return self.subject


class Lesson(ItemBase):
    class Meta:
        unique_together = ('subject', 'course')

    content = RichTextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', db_index=True)
    tags = models.ManyToManyField('Tag', related_name='lessons', blank=True, null=True)

    def __str__(self):
        return self.subject


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
