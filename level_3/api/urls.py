from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'tags', views.TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.CustomUserView.as_view(), name='register'),
]

