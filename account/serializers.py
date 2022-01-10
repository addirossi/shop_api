from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


def normalize_phone(phone):
    import re
    phone = re.sub('[^0-9]', '', phone)
    if phone.startswith('0'):
        phone = f'996{phone[1:]}'
    phone = f'+{phone}'
    return phone


class RegistrationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20,
                                  required=True)
    name = serializers.CharField(max_length=50,
                                 required=True)
    password = serializers.CharField(min_length=6,
                                     required=True)
    password_confirm = serializers.CharField(min_length=6,
                                             required=True)

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Неверный формат номера')
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Номер телефона занят')
        return phone

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self):
        user = User.objects.create_user(**self.validated_data)
        user.create_activation_code()
        user.send_activation_sms()


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6,
                                 min_length=6,
                                 required=True)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def activate(self):
        code = self.validated_data.get('code')
        user = User.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13 or not phone.startswith('+996'):
            raise serializers.ValidationError('Неверный формат номера')
        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return phone

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        user = User.objects.get(phone=phone)
        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')
        if not user.is_active:
            raise serializers.ValidationError('Аккаунт не активен')
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6)
    new_pass = serializers.CharField(min_length=6)
    new_pass_confirm = serializers.CharField(min_length=6)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Укажите верный текущий пароль')
        return old_password

    def validate(self, validated_data):
        new_pass = validated_data.get('new_pass')
        new_pass_confirm = validated_data.get('new_pass_confirm')
        if new_pass != new_pass_confirm:
            raise serializers.ValidationError('Неверный пароль или его подтверждение')
        return validated_data

    def set_new_pass(self):
        new_pass = self.validated_data.get('new_pass')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13 or not phone.startswith('+996'):
            raise serializers.ValidationError('Неверный формат номера')
        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Пользователь с данным номером не зарегистрирован')
        return phone

    def send_code(self):
        phone = self.validated_data.get('phone')
        user = User.objects.get(phone=phone)
        user.create_activation_code()
        user.send_activation_sms()


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)
    new_pass = serializers.CharField(min_length=6)
    new_pass_confirm = serializers.CharField(min_length=6)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def validate(self, validated_data):
        new_pass = validated_data.get('new_pass')
        new_pass_confirm = validated_data.get('new_pass_confirm')
        if new_pass != new_pass_confirm:
            raise serializers.ValidationError('Неверный пароль или его подтверждение')
        return validated_data

    def set_new_pass(self):
        code = self.validated_data.get('code')
        new_pass = self.validated_data.get('new_pass')
        user = User.objects.get(activation_code=code)
        user.set_password(new_pass)
        user.save()