from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsInstructor(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'instructor'
        )


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'student'
        )

class IsCourseOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.role == 'instructor' and obj.created_by == request.user
        )


class IsLessonOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.role == 'instructor' and obj.course.created_by == request.user
        )

