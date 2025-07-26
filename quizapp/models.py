from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
class PublisheManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)

    objects = models.Manager()
    published = PublisheManager()
    def __str__(self):
        return self.title
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username


class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
class Survey(models.Model):
    questions_json = models.JSONField()


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='employees')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    subdomain = models.SlugField(unique=True)

    def __str__(self):
        return self.name
class Customer(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.title
class Tag(models.Model):
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name