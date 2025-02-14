from rest_framework import permissions

class StudentAccessPermission(permissions.BasePermission):
    message = 'You do not have permission to view'

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_staff
        elif view.action == 'retrieve':
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if (request.user == obj.user):
            print("test")
            return True
        return False
    

class StaffListOnly(permissions.BasePermission):
    message = 'Only staff members have permission to view the full requested list'

    def has_permission(self, request, view):

        if view.action == 'list':
            return request.user.is_staff
        return request.user.is_authenticated

class SelfAndStaffEnroll(permissions.BasePermission):
    message = 'You do not have permission to enroll this student'

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        
        if view.action == 'create':
            return request.user.student.id == int(request.data.get('student'))

class IsStaffOrOwner(permissions.BasePermission):
    message = 'You do not have permission to view this instance'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        print(view.action)
        if hasattr(obj, "student"):
            return request.user == obj.student.user
        elif hasattr(obj, "user"):
            return request.user == obj.user

        return False
