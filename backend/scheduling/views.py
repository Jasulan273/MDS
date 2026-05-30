from datetime import datetime, time, timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from scheduling.models import Doctor, Slot
from scheduling.serializers import AppointmentCreateSerializer, AppointmentSerializer, DoctorSerializer, SlotSerializer


class DoctorListView(APIView):
    def get(self, request):
        doctors = Doctor.objects.filter(clinic=request.clinic).order_by("name")
        return Response(DoctorSerializer(doctors, many=True).data)


class DoctorSlotsView(APIView):
    def get(self, request, doctor_id):
        selected_date = parse_date(request.query_params.get("date", ""))
        if selected_date is None:
            return Response({"date": "Expected date in YYYY-MM-DD format."}, status=status.HTTP_400_BAD_REQUEST)

        doctor = get_object_or_404(Doctor, id=doctor_id, clinic=request.clinic)
        start = timezone.make_aware(datetime.combine(selected_date, time.min))
        end = start + timedelta(days=1)

        slots = Slot.objects.filter(
            clinic=request.clinic,
            doctor=doctor,
            start_at__gte=start,
            start_at__lt=end,
        ).order_by("start_at")

        return Response(SlotSerializer(slots, many=True).data)


class AppointmentCreateView(APIView):
    def post(self, request):
        serializer = AppointmentCreateSerializer(data=request.data, context={"clinic": request.clinic})
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)
