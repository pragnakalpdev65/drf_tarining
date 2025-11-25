from rest_framework import viewsets,status , generics 
from .models import Book,Task, CustomUser ,UserProfile
from .serializers import BookSerializer,TaskSerializer, AuthorSerializer, ProductSerializer, UserProfileSerializer
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from .filters import BookFilter, TaskFilter
from .permissions import IsOwnerOrReadOnly
from .throttles import BookCreateThrottle


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'desc']
    ordering_fields = ['title', 'completed', 'created_at']
    ordering = ['-created_at']



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Custom response
        return Response({
            'success': True,
            'message': 'Task created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
     
    def get_queryset(self):
        # Users can only see their own tasks
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['completed', 'created_at', 'priority'] 

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'desc']
  
    filter_backends = [filters.OrderingFilter]  
    ordering_fields = ['title', 'completed', 'created_at', 'updated_at', 'priority']
    ordering = ['priority'] 


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': 'An error occurred',
                'details': response.data
            }
        }
        response.data = custom_response_data

    return response


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = AuthorSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = ProductSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class BookViewSets(viewsets.ModelViewSet):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['title', 'author', 'published_date', 'created_at']
    ordering = ['-created_at']
     
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'published_date']  

class UseProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookViewSet(viewsets.ModelViewSet):
    throttle_classes = [BookCreateThrottle]