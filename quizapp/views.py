from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from quizapp.models import Post, Book, Survey, Company, Customer, Tag, Photo
from quizapp.serializers import PostSerializer, RegisterSerializer, BookSerializer, DynamicSurveyResponseSerializer, \
    CompanySerializer, CustomerSerializer, TagSerializer, PhotoSerializer


class Published(generics.ListAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class BookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    def get_queryset(self):
        return Book.objects.select_related('author')



class SubmitSurveyResponseAPIView(APIView):
    def get(self, request, survey_id):
        survey = get_object_or_404(Survey, id=survey_id)
        serializer = DynamicSurveyResponseSerializer(survey=survey)
        return Response(serializer.data)

    def post(self, request, survey_id):
        survey = get_object_or_404(Survey, id=survey_id)
        serializer = DynamicSurveyResponseSerializer(data=request.data, survey=survey)
        if serializer.is_valid():
            return Response({"message": "Response received", "data": serializer.validated_data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.prefetch_related('employees')
    serializer_class = CompanySerializer


class TenantCustomerListAPIView(generics.ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(tenant=self.request.tenant)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PhotoDetailAPIView(generics.RetrieveAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        tags = instance.tags.values('id', 'name')
        data = {
            "photo": instance.title,
            "tags": list(tags)
        }
        return Response(data)