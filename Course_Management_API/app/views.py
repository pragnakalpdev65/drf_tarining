from rest_framework import viewsets, status,generics,filters
from django.shortcuts import render
from .models import CustomUser, Course, Lesson, Enrollment
from .serializers import CustomUserSerializer, CourseSerializer, LessonSerializer, EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

# Create your views here.
class CustomUserView(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
    permission_classes=[]

    def create (self,request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        
        refresh=RefreshToken.for_user(user)

        return Response({
            'user': serializer.data,
            'refresh':str(refresh),
            'access':str(refresh.access_token),
        })
    
class CourseViewSet(generics.CreateAPIView):
    queryset=Course.objects.all()
    serializer_class=CourseSerializer
    permission_classes=[IsAuthenticated]
    filter_backends=[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields=['created_by']
    search_fields=['title']

    def create(self,request,*args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exceptions=True)
        self.perform_craete(serializer)

        return Response({
            'success':True,
            'message':'course is added.',
            'data':serializer.data,
        })
    
    def list(self,request,*args, **kwargs):
        queryset=self.filter_queryset(self.get_queryset())
        serializer=self.get_serializer(queryset,many=True)

        return Response({
            'count':queryset.count(),
            'result':serializer.data
        })
        


class LessonViewSet(viewsets.ModelViewSet):
    queryset=Lesson.objects.all()
    serializer_class=LessonSerializer
    permission_classes=[IsAuthenticated]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset=Enrollment.objects.all()
    swrializer_class=EnrollmentSerializer
    permission_classes=[IsAuthenticated]


