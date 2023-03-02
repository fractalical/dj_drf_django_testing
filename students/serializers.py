from django_testing.settings import MAX_STUDENTS_PER_COURSE
from rest_framework import serializers
from rest_framework.validators import ValidationError

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):

        if len(value) > MAX_STUDENTS_PER_COURSE:
            raise ValidationError

        return value
