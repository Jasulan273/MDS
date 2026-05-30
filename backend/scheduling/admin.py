from django.contrib import admin

from scheduling.models import Appointment, Clinic, Doctor, Slot


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialization", "clinic")
    list_filter = ("clinic", "specialization")
    search_fields = ("name", "specialization")


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("id", "doctor", "clinic", "start_at", "duration_minutes", "status")
    list_filter = ("clinic", "doctor", "status", "start_at")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "slot", "clinic", "patient_name", "patient_phone", "created_at")
    list_filter = ("clinic", "created_at")
    search_fields = ("patient_name", "patient_phone")
