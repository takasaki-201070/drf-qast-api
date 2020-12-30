from rest_framework import permissions

class ProfilePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 参照の場合は、ログインユーザに関係なく許可する
        if request.method in permissions.SAFE_METHODS:
            return True
        # 参照以外は、ログインユーザのみを許可する
        return obj.userPro.id == request.user.id
