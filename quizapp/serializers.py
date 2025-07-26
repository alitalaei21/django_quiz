from django.contrib.auth.models import User
from rest_framework import serializers

from quizapp.models import Post, Author, Book, Employee, Company, Customer, Photo, Tag


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name']
class BookSerializer(serializers.ModelSerializer):
    Author = AuthorSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ['id','title','author']


class DynamicSurveyResponseSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        survey = kwargs.pop('survey', None)
        super().__init__(*args, **kwargs)

        if survey:
            for question in survey.questions_json:
                field_name = question['name']
                label = question.get('label', field_name)
                q_type = question.get('type', 'text')

                if q_type == 'integer':
                    self.fields[field_name] = serializers.IntegerField(label=label)
                elif q_type == 'email':
                    self.fields[field_name] = serializers.EmailField(label=label)
                else:
                    self.fields[field_name] = serializers.CharField(label=label)



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True,many=True)
    class Meta:
        model = Company
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'content_type', 'object_id']
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'