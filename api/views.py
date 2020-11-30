from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets
from . import serializers, custompermissions
from .models import FrameBrand, WheelBrand, Profile, FriendRequest, Message
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import FrameBrandSerializer, WheelBrandSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = serializers.FriendRequestSerializer

    def get_queryset(self):
        return self.queryset.filter(Q(askTo=self.request.user) | Q(askFrom=self.request.user))

    def perform_create(self, serializer):
        try:
            serializer.save(askFrom=self.request.user)
        except:
            raise ValidationError("User can have only unique request")

    def destroy(self, request, *args, **kwargs):
        response = {"message": "Delete is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {"message": "Patch is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, custompermissions.ProfilePermission)

    def perform_create(self, serializer):
        serializer.save(userPro=self.request.user)


class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(userPro=self.request.user)


class FrameBrandViewSet(viewsets.ModelViewSet):
    queryset = FrameBrand.objects.all()
    serializer_class = FrameBrandSerializer

    def destroy(self, request, *args, **kwargs):
        response = {"message": "Delete is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {"message": "Put is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {"message": "Patch is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class WheelBrandViewSet(viewsets.ModelViewSet):
    queryset = WheelBrand.objects.all()
    serializer_class = WheelBrandSerializer

    def destroy(self, request, *args, **kwargs):
        response = {"message": "Delete is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {"message": "Put is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {"message": "Patch is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Delete DM is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Update DM is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'Patch DM is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class InboxListView(viewsets.ReadOnlyModelViewSet):

    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)