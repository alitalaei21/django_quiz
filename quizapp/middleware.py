# quizapp/middleware.py

from django.utils.deprecation import MiddlewareMixin
from quizapp.models import Tenant  # مدلی که tenant رو نگه می‌داره، باید درست باشه

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().split(':')[0]  # localhost:8000 → localhost
        subdomain = host.split('.')[0]           # tenant1.example.com → tenant1

        try:
            tenant = Tenant.objects.get(subdomain=subdomain)
            request.tenant = Tenant.objects.first()

        except Tenant.DoesNotExist:
            request.tenant = None
