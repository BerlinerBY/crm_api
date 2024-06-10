from rest_framework import permissions
from rest_framework_simplejwt.tokens import AccessToken
from .views import User

def get_user_obj(request):
      token_str = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
      token = AccessToken(token_str)
      user_id = token['user_id']
      req_user = User.objects.get(id=user_id)

      return req_user

class IsSuperuser(permissions.BasePermission):
        def has_permission(self, request, view):
            if get_user_obj(request).is_superuser:
                  return True
            return False
        
        def has_object_permission(self, request, view, obj):
            if get_user_obj(request).is_superuser:
                  return True
            return False

class IsStaff(permissions.BasePermission):
        def has_permission(self, request, view):
            if get_user_obj(request).is_staff:
                  return True
            return False
        
        def has_object_permission(self, request, view, obj):
            if get_user_obj(request).is_staff:
                  return True
            return False