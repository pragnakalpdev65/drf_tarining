from rest_framework import serializers
from .models import Book, Task, Author, Product,CustomUser, UserProfile
from django.contrib.auth.models import User

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
        model=Author
        fields=['name','bio','email']

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