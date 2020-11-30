from django.urls import path, include
from . import views
from rest_framework import routers

app_name = "user"

router = routers.DefaultRouter()
router.register("profile", views.ProfileViewSet)
router.register("approval", views.FriendRequestViewSet)
router.register("message", views.MessageViewSet, basename="message")
router.register("inbox", views.InboxListView, basename="inbox")
router.register("wheel", views.WheelBrandViewSet)
router.register("frame", views.FrameBrandViewSet)
urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("myprofile/", views.MyProfileListView.as_view(), name="myprofile"),
    path("", include(router.urls)),
]