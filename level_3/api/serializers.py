from rest_framework import serializers
from .models import Book, Task, Author, Product,CustomUser, UserProfile, Post, Comment, Tag
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class BookSerializer(serializers.ModelSerializer):

    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'description', 'owner', 'owner_username', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'desc', 'completed', 'owner',  'created_at', 'updated_at', 'priority']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

        priority = serializers.ChoiceField(choices=[
             ('high', 'High'),
             ('medium', 'Medium'),
             ('low', 'Low'),
         ])

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','first_name', 'last_name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        field=['name', 'description', 'price', 'stock', 'is_available', 'created_at','updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username', read_only=True)
    email=serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model=UserProfile
        fields=['id','username','email','bio','phone_number', 
                  'avatar', 'website', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=['id','name']

class CommentSerializer(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    author_id=serializers.IntegerField(write_only=True)

    class Meta:
        model=Comment
        fields=['id', 'content', 'author', 'author_id', 'created_at']
        read_only_fields=['id','created_at']


class PostSerializer(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    tags=TagSerializer(many=True, required=False)
    comments=CommentSerializer(many=True, read_only=True)
    comment_count=serializers.SerializerMethodField()

    class Meta:
        model=Post
        fields=['id','title', 'content', 'author', 'tags', 'comments', 'comment_count', 'published', 'created_at', 'updated_at']
        read_only_fields=['id','author','created_at','updated_at']

    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def create(self,validated_data):
        tags_data=validated_data.pop('tags',[])
        request= self.context.get('request')
        post=Post.objects.create(author=request.user, **validated_data)

        for tag_data in tags_data:
            tag,created=Tag.objects.get_or_create(name=tag_data['name'])
            post.tags.add(tag)

        return post
    
    def update(self,instance,validated_data):
        tags_data=validated_data.pop('tags',None)

        instance.title=validated_data.pop('title',instance.title)
        instance.content=validated_data.get('content', instance.content)
        instance.published=validated_data.get('published',instance.published)
        instance.save()

        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag,created=Tag.objects.get_or_create(name=tag_data['name'])
                instance.tags.add(tag)

        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token
    
