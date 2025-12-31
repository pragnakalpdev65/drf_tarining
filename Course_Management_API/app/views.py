from rest_framework import viewsets, status, filters
from .models import CustomUser, Course, Lesson, Enrollment
from .serializers import CustomUserSerializer, CourseSerializer, LessonSerializer, EnrollmentSerializer, PublicCourseSerializer,StudentCourseSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permissions import IsInstructor,IsCourseOwner,IsLessonOwner,IsStudent
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class CustomUserView(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
    permission_classes=[]

    def create (self,request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        
        return Response({
            'user': serializer.data,
             
        })
    
class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class CourseView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_by']
    search_fields = ['title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.role == 'instructor':
            return Course.objects.filter(created_by=user)

 
        return Course.objects.all()
    
    def get_serializer_class(self):
        user = self.request.user

        if not user.is_authenticated:
            return PublicCourseSerializer


        if user.role == 'student':
            return StudentCourseSerializer
        return CourseSerializer


    def get_permissions(self):
        if self.action == 'create':
            return [IsInstructor()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsInstructor(), IsCourseOwner()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "message": "Course deleted successfully"
        })

class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    throttle_classes = [AnonRateThrottle,UserRateThrottle]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsInstructor()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsLessonOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'student':
            return Lesson.objects.filter(
                course__enrollments__user=user
            )
        return Lesson.objects.filter(
            course__created_by=user
        )

    def perform_create(self, serializer):
        course = serializer.validated_data.get("course")

        if course.created_by != self.request.user:
            raise PermissionDenied(
                "You are not allowed to add lessons to this course."
            )

        serializer.save()

    def perform_update(self, serializer):
        lesson = self.get_object()

        # if lesson.course.created_by != self.request.user:
        #     raise PermissionDenied(
        #         "You are not allowed to update this lesson."
        #     )
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "message": "Lesson deleted successfully"
        })


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "success": True,
            "message": "You are enrolled in the course",
            "data": serializer.data
        })
    

