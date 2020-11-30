from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import FrameBrand, WheelBrand, Profile, FriendRequest, Message, User
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class FrameBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameBrand
        fields = ("id", "item")


class WheelBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = WheelBrand
        fields = ("id", "item")


class ProfileSerializer(serializers.ModelSerializer):
    frameBrand_item = serializers.ReadOnlyField(source="frameBrand.item", read_only=True)
    component_name = serializers.CharField(source="get_component_display", read_only=True)
    wheelBrand_item = serializers.ReadOnlyField(source="wheelBrand.item", read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "nickName", "frameBrand", "frameBrand_item", "frame", "component", "component_name", "compo",
                  "wheelBrand", "wheelBrand_item", "wheel", "purchase", "userPro", "created_on", "img", "liked",
                  "favCourse", "favGear", "favShop")
        extra_kwargs = {"userPro": {"read_only": True}}


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ("id", "askFrom", "askTo", "approved")
        extra_kwargs = {"askFrom": {"read_only": True}}


class FriendsFilter(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        request = self.context['request']
        friends = FriendRequest.objects.filter(Q(askTo=request.user) & Q(approved=True))

        list_friend = []
        for friend in friends:
            list_friend.append(friend.askFrom.id)

        queryset = User.objects.filter(id__in=list_friend)
        return queryset


class MessageSerializer(serializers.ModelSerializer):

    receiver = FriendsFilter()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message')
        extra_kwargs = {'sender': {'read_only': True}}
