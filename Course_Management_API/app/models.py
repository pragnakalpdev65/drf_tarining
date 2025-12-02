from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):

    USER_TYPE=(
        ('istructor','Instructor'),
        ('studednt','Student'),
        )
    
    username=models.CharField(max_length=15, blank=True,unique=True)
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=30,choices=USER_TYPE, default='student')



    def __str__(self):
        return f"{self.username} ({self.role})"

class Course(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    created_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='instructor')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=100)
    content=models.TextField(null=True,blank=True)
    video_url=models.URLField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class Enrollment(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, related_name='student')
    course=models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    enrolled_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'course') 

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"