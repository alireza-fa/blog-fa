from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from .utils.jwt import get_token_for_user
from django.contrib.auth import get_user_model
from .utils.otp import send_otp_code, check_otp_code, send_otp_code_forget_password
from .tasks import send_mail_task
from random import randint


class TokenJWTSerializer(serializers.Serializer):
    username = serializers.CharField(label=_('Email or Username'))
    password = serializers.CharField(max_length=32, min_length=8)

    def validate(self, data):
        if data.get('username') and data.get('password'):
            user = authenticate(username=data['username'], password=data['password'])
            if not user:
                raise serializers.ValidationError(_('Not found user this information.'))
            token = get_token_for_user(user)
            data['token'] = token
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=32)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')

    def validate(self, data):
        user = get_user_model().objects.filter(username=data['username'])
        if user.exists():
            raise serializers.ValidationError(_('This username already exists.'))
        user = get_user_model().objects.filter(email=data['email'])
        if user.exists():
            raise serializers.ValidationError(_('This email already exists.'))
        send_otp_code(email=data['email'], username=data['username'], password=data['password'])
        return data


class VerifyAccountSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=4, max_length=4)

    def validate(self, data):
        if data.get('code'):
            info = check_otp_code(data['code'])
            if not info:
                raise serializers.ValidationError(_('Invalid code.'))
            user = get_user_model().objects.create_user(info['username'], info['email'], info['password'])
            token = get_token_for_user(user)
            data['token'] = token
        return data


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=32)
    new_password = serializers.CharField(min_length=8, max_length=32)
    confirm_password = serializers.CharField(min_length=8, max_length=32)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(_('new password and confirm password must be match.'))
        user = self.context.get('request').user
        check_password = user.check_password(data['password'])
        if not check_password:
            raise serializers.ValidationError(_('The old password is wrong.'))
        user.set_password(data['new_password'])
        user.save()
        return data


class PasswordForgetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=120)

    def validate_email(self, value):
        user = get_user_model().objects.filter(email=value)
        if not user.exists():
            raise serializers.ValidationError(_('No account found with email.'))
        send_otp_code_forget_password(value)
        return value


class PasswordForgetConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=5, max_length=5)

    def validate_code(self, value):
        info = check_otp_code(value)
        if not info:
            raise serializers.ValidationError(_('Invalid code.'))
        user = get_user_model().objects.get(email=info['email'])
        new_password = str(randint(10000000, 99999999))
        user.set_password(new_password)
        user.save()
        send_mail_task.delay(info['email'], _('new password'), _(f'your new password is: {new_password}'))
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        exclude = ('created', 'modified', 'is_superuser', 'password', 'is_admin')
        read_only_fields = ('is_star', 'is_active', 'email')
