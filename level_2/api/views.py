from rest_framework import viewsets,status , generics 
from .models import Book,Task
from .serializers import BookSerializer,TaskSerializer, AuthorSerializer, ProductSerializer
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

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
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

