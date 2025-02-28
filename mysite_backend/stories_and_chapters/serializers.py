from rest_framework import serializers
from .models import Story, Chapter
from users_and_auth.serializers import UserSerializer

class StorySerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'title', 'is_complete', 'created_at', 'updated_at', 'author']
        read_only_fields = ['author']


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']


class ChapterDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'story']
        read_only_fields = ['story']


class StoryDetailSerializer(serializers.ModelSerializer):

    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'title', 'is_complete', 'created_at', 'updated_at', 'chapters']