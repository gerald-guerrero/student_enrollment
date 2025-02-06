from django.core.exceptions import PermissionDenied

def is_owner_or_staff(instance):
    is_staff = instance.request.user.is_staff
    is_owner = instance.request.user == instance.get_object().user
    
    return is_owner | is_staff

def user_is_staff(user):
    if not user.is_staff:
        raise PermissionDenied
    return True

def user_is_student(user):
    if not hasattr(user, 'student'):
        raise PermissionDenied
    return True