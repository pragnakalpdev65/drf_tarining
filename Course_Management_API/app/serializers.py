from rest_framework import serializers
from .models import CustomUser, Course, Lesson, Enrollment


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "role"]

        role=serializers.ChoiceField(choices=[
            ('instructor', 'Instructor'),
            ('student', 'Students'),
        ])


    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
                

class PublicCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title']  


class CourseSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    lessons_count = serializers.SerializerMethodField()
    enrolled_students_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "created_by", "created_at", "lessons_count","enrolled_students_count"
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_enrolled_students_count(self, obj):
        return obj.enrollments.count()

    
class StudentCourseSerializer(serializers.ModelSerializer):
    total_lessons = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "total_lessons", "total_students"
        ]

    def get_total_lessons(self, obj):
        return obj.lessons.count()

    def get_total_students(self, obj):
        return obj.enrollments.count()



class LessonSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source="course.title")
    title=serializers.CharField(allow_blank=False )
    id = serializers.IntegerField(label='ID', read_only=True)
    video_url = serializers.URLField()
    class Meta:
        model = Lesson

        fields = [
             "id","course", "course_title","title", "content", "video_url","created_at"
        ]
    
    def create(self,validated_data):
        lesson=Lesson.objects.create(**validated_data)
        return lesson
    
    def update(self,instance,validated_data):

        instance.title=validated_data.get('title',instance.title)
        instance.content=validated_data.get('content',instance.content)
        instance.video_url=validated_data.get('video_url',instance.video_url)
        
        return instance

class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    course_title = serializers.ReadOnlyField(source="course.title")

    class Meta:
        model = Enrollment
        fields = ["id", "user", "course", "course_title", "enrolled_at"]

    def validate(self, data):
        user = self.context['request'].user
        if Enrollment.objects.filter(user=user, course=data['course']).exists():
            raise serializers.ValidationError("Already enrolled in this course.")
        return data
    
 
    
    