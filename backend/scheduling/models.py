from django.core.validators import MinValueValidator
from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Doctor(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="doctors")
    name = models.CharField(max_length=120)
    specialization = models.CharField(max_length=120)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["clinic", "name", "specialization"], name="unique_doctor_per_clinic")
        ]
        indexes = [
            models.Index(fields=["clinic", "name"], name="doctor_clinic_name_idx"),
        ]

    def __str__(self):
        return f"{self.name}, {self.specialization}"


class Slot(models.Model):
    class Status(models.TextChoices):
        FREE = "free", "Free"
        BOOKED = "booked", "Booked"

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="slots")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="slots")
    start_at = models.DateTimeField()
    duration_minutes = models.PositiveSmallIntegerField(default=30, validators=[MinValueValidator(5)])
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.FREE)

    class Meta:
        ordering = ["start_at"]
        constraints = [
            models.UniqueConstraint(fields=["clinic", "doctor", "start_at"], name="unique_slot_start_per_doctor"),
        ]
        indexes = [
            models.Index(fields=["clinic", "doctor", "start_at"], name="slot_clinic_doctor_start_idx"),
            models.Index(fields=["clinic", "status"], name="slot_clinic_status_idx"),
        ]

    def save(self, *args, **kwargs):
        if self.doctor_id:
            doctor_clinic_id = self.doctor.clinic_id
            if not self.clinic_id:
                self.clinic_id = doctor_clinic_id
            elif self.clinic_id != doctor_clinic_id:
                raise ValueError("Slot clinic must match doctor clinic.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doctor} at {self.start_at}"


class Appointment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="appointments")
    slot = models.OneToOneField(Slot, on_delete=models.PROTECT, related_name="appointment")
    patient_name = models.CharField(max_length=120)
    patient_phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["clinic", "created_at"], name="appointment_clinic_created_idx"),
        ]

    def __str__(self):
        return f"{self.patient_name} for {self.slot}"

    def save(self, *args, **kwargs):
        if self.slot_id:
            slot_clinic_id = self.slot.clinic_id
            if not self.clinic_id:
                self.clinic_id = slot_clinic_id
            elif self.clinic_id != slot_clinic_id:
                raise ValueError("Appointment clinic must match slot clinic.")
        super().save(*args, **kwargs)
