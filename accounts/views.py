from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .serializers import (TokenJWTSerializer, RegistrationSerializer, VerifyAccountSerializer,
                          PasswordChangeSerializer, PasswordForgetSerializer, PasswordForgetConfirmSerializer,
                          UserSerializer, LogoutSerializer)
from .models import Follow

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from permissions import IsNotAuthenticated, IsOwnerOrReadOnly, IsAuthenticatedAndNotObjectOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ApiBaseView(APIView):
    serializer_class = None
    message = None
    data_filter = None
    status = 200
    need_request_in_serializer = False

    def post(self, request):
        if self.need_request_in_serializer:
            serializer = self.serializer_class(data=request.data, context={"request": request})
        else:
            serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.message:
            return Response(data={"msg": self.message}, status=self.status)
        if self.data_filter:
            return Response(data=serializer.validated_data.get(self.data_filter), status=self.status)
        return Response(data=serializer.data)


class TokenJWTView(ApiBaseView):
    permission_classes = (IsNotAuthenticated,)
    serializer_class = TokenJWTSerializer
    data_filter = 'token'
    status = status.HTTP_200_OK


class RegistrationView(ApiBaseView):
    permission_classes = (IsNotAuthenticated,)
    serializer_class = RegistrationSerializer
    message = _('We send a otp code for you')
    status = status.HTTP_200_OK


class VerifyAccountView(ApiBaseView):
    permission_classes = (IsNotAuthenticated,)
    serializer_class = VerifyAccountSerializer
    data_filter = 'token'
    status = status.HTTP_201_CREATED


class PasswordChangeView(ApiBaseView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer
    need_request_in_serializer = True
    message = _('Your password has been successfully changed')
    status = status.HTTP_200_OK


class PasswordForgetView(ApiBaseView):
    serializer_class = PasswordForgetSerializer
    message = _('We sent a code for forgot password in your email.')
    status = status.HTTP_200_OK


class PasswordForgetConfirmView(ApiBaseView):
    serializer_class = PasswordForgetConfirmSerializer
    message = _('Your password has changed please check your email.')
    status = status.HTTP_200_OK


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_permissions(self):
        if self.action in ('list', 'create', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class UserDetailCreateView(RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (IsOwnerOrReadOnly,)


class FollowUserView(APIView):
    permission_classes = (IsAuthenticatedAndNotObjectOwner,)

    def post(self, request, user_id):
        user = get_object_or_404(get_user_model(), id=user_id)
        self.check_object_permissions(request, user)
        follow_check = request.user.following.filter(follow=request.user, user=user)
        if follow_check.exists():
            follow_check.delete()
        else:
            Follow.objects.create(user=user, follow=request.user)
        return Response(data={"msg": 'successfully'}, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
