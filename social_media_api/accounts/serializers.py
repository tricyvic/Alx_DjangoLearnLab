from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()

# Implement views and serializers in the accounts app for user registration, login, and token retrieval
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'bio', 'profile_picture')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):        
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Invalid credentials")

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    bio = serializers.CharField(allow_blank=True, required=False)
    profile_picture = serializers.ImageField(allow_null=True, required=False)
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    followers = serializers.ListField(child=serializers.CharField(), required=False)
    following = serializers.ListField(child=serializers.CharField(), required=False)

class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count', 'followers', 'following')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers(self, obj):
        return [follower.username for follower in obj.followers.all()]

    def get_following(self, obj):
        return [followed.username for followed in obj.following.all()]


