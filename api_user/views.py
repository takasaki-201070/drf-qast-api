from rest_framework import generics, authentication, permissions
from rest_framework.permissions import AllowAny
from api_user import serializers
from core.models import Profile
from rest_framework import viewsets
from core import custompermissions


# ************************
# プロフィール
#　検索：全ユーザを取得する
# ************************
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, custompermissions.ProfilePermission)

    # プロフィールの新規作成時（ログインユーザのプロフィールとする）
    def perform_create(self, serializer):
        serializer.save(userPro=self.request.user)

# ************************
# ログインユーザのプロフィール取得
# ************************
class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    # プロフィールの検索時（ログインユーザのプロフィールを検索する）
    def get_queryset(self):
        return self.queryset.filter(userPro=self.request.user)

