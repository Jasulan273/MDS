import re

from rest_framework import serializers

from scheduling.models import Appointment, Doctor, Slot
from scheduling.services import SlotAlreadyBooked, book_slot


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name", "specialization"]


class SlotSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(source="doctor.id", read_only=True)

    class Meta:
        model = Slot
        fields = ["id", "doctor_id", "start_at", "duration_minutes", "status"]


class AppointmentSerializer(serializers.ModelSerializer):
    slot_id = serializers.IntegerField(source="slot.id", read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "slot_id", "patient_name", "patient_phone", "created_at"]


class AppointmentCreateSerializer(serializers.Serializer):
    slot_id = serializers.IntegerField()
    patient_name = serializers.CharField(max_length=120, trim_whitespace=True)
    patient_phone = serializers.CharField(max_length=32, trim_whitespace=True)

    def validate_patient_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Patient name is too short.")
        return value.strip()

    def validate_patient_phone(self, value):
        phone = value.strip()
        if not re.match(r"^\+?[\d\s().-]{7,32}$", phone):
            raise serializers.ValidationError("Patient phone is invalid.")
        return phone

    def create(self, validated_data):
        clinic = self.context["clinic"]
        try:
            return book_slot(
                clinic=clinic,
                slot_id=validated_data["slot_id"],
                patient_name=validated_data["patient_name"],
                patient_phone=validated_data["patient_phone"],
            )
        except Slot.DoesNotExist as exc:
            raise serializers.ValidationError({"slot_id": "Slot not found."}) from exc
        except SlotAlreadyBooked as exc:
            raise serializers.ValidationError({"slot_id": "Slot is already booked."}) from exc
