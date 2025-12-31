from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register(r'course',views.CourseView,basename='course')
router.register(r'register',views.CustomUserView, basename='register')
#router.register(r'login',views.LoginViewSet,basename='login')
router.register(r'lesson',views.LessonViewSet,basename='lesson')
router.register(r'enrollment',views.EnrollmentViewSet, basename='enrollment')





urlpatterns = [
    path('', include(router.urls)),
    # path('register/',views.CustomUserView.as_view({'get': 'list'}),name='register'),
    # path('course/',views.CourseView.as_view({'get': 'list'}),name='course'),
    path('login/',views.LoginView.as_view(),name='login')
]