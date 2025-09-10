from rest_framework import serializers
from .models import Post, Comment, Like

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    author = serializers.CharField(source='author.user.username', read_only=True)
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'comment_count', 'like_count']
        read_only_fields = ['author']

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_like_count(self, obj):
        return obj.likes.count()


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    author = serializers.CharField(source='author.user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'post']


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    """
    author = serializers.CharField(source='author.user.username', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'post', 'author', 'created_at']
        read_only_fields = ['author', 'post']
