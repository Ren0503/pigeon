from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Article, Category, Comment


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def get_articles(self, obj):
        articles = obj.article_set.all()
        serializer = ArticleSerializer(articles, many=True)
        return serializer.data