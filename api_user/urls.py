from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from api_user import views

router = routers.DefaultRouter()
router.register('profile',views.ProfileViewSet)

urlpatterns = [
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('', include(router.urls)),
]
