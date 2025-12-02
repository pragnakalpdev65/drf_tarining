from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register(r'course',views.CourseViewSet,basename='course')
router.register(r'lesson',views.LessonViewSet,basename='lessom')
router.register(r'enrollment',views.EnrollmentViewSet, basename='enrollment')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.CustomUserView.as_view(), name='register'),
]