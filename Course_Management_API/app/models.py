from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE = (
        ("instructor", "Instructor"),
        ("student", "Student"),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=USER_TYPE, default="student")

    def __str__(self):
        return f"{self.username} ({self.role})"

class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True,default="")
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name="courses",default="")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,related_name="lessons",default=1)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True,default="")
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="enrollments",default="")
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="enrollments",default="")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
