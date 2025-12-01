from rest_framework import serializers
from .models import User, Course, Lesson, Enrollment


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]

class CourseSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    lessons_count = serializers.IntegerField(read_only=True)
    enrolled_students_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "title", "description", "created_by", "created_at","lessons_count", "enrolled_students_count"
        ]


class LessonSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source="course.title")

    class Meta:
        model = Lesson
        fields = [
            "id", "course", "course_title","title", "content", "video_url","created_at"
        ]

class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    course_title = serializers.ReadOnlyField(source="course.title")

    class Meta:
        model = Enrollment
        fields = ["id", "user", "course", "course_title", "enrolled_at"]
