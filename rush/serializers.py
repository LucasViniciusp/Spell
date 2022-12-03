from rest_framework import serializers
from rush.models import User, Post, Follower


# Create serializers here.
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "birth_date",
            "picture",
            "banner",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "first_name",
            "last_name",
            "birth_date",
            "picture",
            "banner",
            "date_joined",
        )

    def get_name(self, obj):
        return obj.get_full_name()


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_follower(self, follower):
        if self.get_authenticated_user() == follower:
            raise serializers.ValidationError("You cannot follow youself!")
        return follower

    def get_authenticated_user(self):
        return self.context["request"].user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "user", "content", "created_at")
        read_only_fields = ["user"]

    def get_authenticated_user(self):
        return self.context["request"].user
