from django.urls import path, include
from rest_framework.routers import DefaultRouter

from quizapp.views import Published, RegisterAPIView, BookListAPIView, SubmitSurveyResponseAPIView, CompanyListAPIView, \
    TenantCustomerListAPIView, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet)
urlpatterns = [
    path('api/Published/', Published.as_view(), name='published'),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/books/', BookListAPIView.as_view(), name='book_list'),
    path('api/survey/<int:survey_id>/submit/', SubmitSurveyResponseAPIView.as_view(), name='submit-survey'),
    path('api/companies/', CompanyListAPIView.as_view(), name='company_list'),
    path('api/customers/', TenantCustomerListAPIView.as_view(), name='tenant-customers'),
    path('api/tag/', include(router.urls)),
]