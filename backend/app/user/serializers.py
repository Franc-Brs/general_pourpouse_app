"""
Serilizers for the users API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializers for the user object.
    Serializers are a way to covnerto objects to and from py objects
    task jSON input and it validates it and it converts it into a model
    or a py object. This one convert JSON into data of a model."""

    class Meta:
        model = get_user_model()
        # u dont put is_staff or so coz u don't want to normal user to set it
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and returna user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user.
        If we don't write this method when we update the pwd is stored
        in cleared text,
        Instance is the instance that is being updated,
        validated_data is data already passed in the serilizers validation
        (email, pwd, name)"""
        # retrieve pwd and remove it, we don't want to force the user
        # to have a pwd in this request
        password = validated_data.pop('password', None)
        # overriding the modelserializers
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'inpput_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
