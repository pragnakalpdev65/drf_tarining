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

class CourseSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    enrolled_students_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "title", "description", "created_by", "created_at","lessons_count"
        ]

    def create(self, validated_data):
        request=self.context.get('request')

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required to create course")
        course=Course.objects.create(created_by=request.user, **validated_data)
        course.save()

        return course 
    
    def update(self,instance,validated_data):
        assigned_to_ids=validated_data.pop('assigned_to_ids',None)

        instance.title=validated_data.get('title', instance.title)
        instance.description=validated_data.get('description',instance.description)
        instance.lesson_count=validated_data.get('lesson_count',instance.lesson_count)

        instance.save()

        if assigned_to_ids is not None:
            instance.assigned_to.set(assigned_to_ids)

        return instance
    
    def get_enrollment_count(self,obj):
        return obj.enrolled_students_count()
    


class LessonSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source="course.title")
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id", "course", "course_title","title", "content", "video_url","created_at","lesson_count"
        ]
    
    def create(self,validated_data):
        lesson=Lesson.objects.create(**validated_data)
        

        return lesson
    
    def update(self,instance,validated_data):

        instance.title=validated_data.pop('title',instance.title)
        instance.content=validated_data.get('content',instance.content)
        instance.video_url=validated_data.get('video_url',instance.video_url)
        
        return instance


class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    course_title = serializers.ReadOnlyField(source="course.title")

    class Meta:
        model = Enrollment
        fields = ["id", "user", "course", "course_title", "enrolled_at","enroll_students_count"]
    
 
    
    