from core.utils.serializers import Base64ImageField
from rest_framework import serializers
from users.models import UserBase


class RegisterUserBaseSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = UserBase
        fields = ('email', 'password', 'first_name', 'last_name',
                  'phone_number', 'profile_image', 'gender', 'dob', 'address',
                  'zip_code', 'city', 'country', 'blood_group', 'indexes',
                  'preferred_size', 'designation')

        extra_kwargs = {
            'is_verified': {
                'read_only': True
            },
            'last_login': {
                'read_only': True
            },
            'is_staff': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance


class UserBaseSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = UserBase
        fields = ('email', 'password', 'first_name', 'last_name',
                  'phone_number', 'profile_image', 'gender', 'dob', 'address',
                  'zip_code', 'city', 'country', 'blood_group', 'indexes',
                  'preferred_size', 'is_verified', 'last_login', 'is_staff',
                  'id', 'distance_ran', 'event_participated_in_count', 'uuid',
                  'created_at', 'is_active', 'designation')

        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'uuid': {
                'read_only': True
            },
            'email': {
                'read_only': True
            },
            'is_verified': {
                'read_only': True
            },
            'last_login': {
                'read_only': True
            },
            'is_staff': {
                'read_only': True
            },
            'password': {
                'write_only': True
            }
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return super(UserBaseSerializer, self).update(instance, validated_data)
