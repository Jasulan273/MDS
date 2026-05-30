from django.http import JsonResponse

from scheduling.models import Clinic


class ClinicContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/") and request.method != "OPTIONS":
            clinic_id = request.headers.get("Clinic-Id")
            if not clinic_id:
                return JsonResponse({"detail": "Clinic-Id header is required."}, status=400)
            try:
                request.clinic = Clinic.objects.get(id=clinic_id)
            except (Clinic.DoesNotExist, ValueError):
                return JsonResponse({"detail": "Clinic not found."}, status=404)

        return self.get_response(request)
