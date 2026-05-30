from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, time

from django.db import close_old_connections, connection
from django.test import Client, TestCase, TransactionTestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from scheduling.models import Appointment, Clinic, Doctor, Slot


def create_slot(*, clinic_name="Clinic", doctor_name="Doctor", start_time=time(9, 0)):
    clinic = Clinic.objects.create(name=clinic_name)
    doctor = Doctor.objects.create(clinic=clinic, name=doctor_name, specialization="Therapist")
    slot = Slot.objects.create(
        clinic=clinic,
        doctor=doctor,
        start_at=timezone.make_aware(datetime.combine(timezone.localdate(), start_time)),
        duration_minutes=30,
    )
    return clinic, doctor, slot


@override_settings(ALLOWED_HOSTS=["testserver"])
class AppointmentApiTests(TestCase):
    def setUp(self):
        self.clinic, self.doctor, self.slot = create_slot()
        self.client = Client(HTTP_CLINIC_ID=str(self.clinic.id))

    def test_book_free_slot(self):
        response = self.client.post(
            reverse("appointment-create"),
            data={"slot_id": self.slot.id, "patient_name": "Ivan Petrov", "patient_phone": "+77001234567"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.status, Slot.Status.BOOKED)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_reject_repeated_booking(self):
        payload = {"slot_id": self.slot.id, "patient_name": "Ivan Petrov", "patient_phone": "+77001234567"}

        first_response = self.client.post(reverse("appointment-create"), data=payload, content_type="application/json")
        second_response = self.client.post(reverse("appointment-create"), data=payload, content_type="application/json")

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 400)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_slot_from_another_clinic_is_not_available(self):
        another_clinic, _, another_slot = create_slot(clinic_name="Another clinic", doctor_name="Another doctor")
        response = self.client.post(
            reverse("appointment-create"),
            data={"slot_id": another_slot.id, "patient_name": "Ivan Petrov", "patient_phone": "+77001234567"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Appointment.objects.filter(clinic=another_clinic).count(), 0)

    def test_reject_invalid_patient_name(self):
        response = self.client.post(
            reverse("appointment-create"),
            data={"slot_id": self.slot.id, "patient_name": "A", "patient_phone": "+77001234567"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_reject_invalid_patient_phone(self):
        response = self.client.post(
            reverse("appointment-create"),
            data={"slot_id": self.slot.id, "patient_name": "Ivan Petrov", "patient_phone": "abc"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Appointment.objects.count(), 0)


@override_settings(ALLOWED_HOSTS=["testserver"])
class ConcurrentBookingTests(TransactionTestCase):
    reset_sequences = True

    def test_only_one_concurrent_request_books_slot(self):
        if connection.vendor != "postgresql":
            self.skipTest("Row-level locking is validated against PostgreSQL.")

        clinic, _, slot = create_slot()
        payloads = [
            {"slot_id": slot.id, "patient_name": "First Patient", "patient_phone": "+77001111111"},
            {"slot_id": slot.id, "patient_name": "Second Patient", "patient_phone": "+77002222222"},
        ]

        def send(payload):
            close_old_connections()
            client = Client(HTTP_CLINIC_ID=str(clinic.id))
            response = client.post(reverse("appointment-create"), data=payload, content_type="application/json")
            close_old_connections()
            return response.status_code

        with ThreadPoolExecutor(max_workers=2) as executor:
            statuses = list(executor.map(send, payloads))

        self.assertEqual(sorted(statuses), [201, 400])
        self.assertEqual(Appointment.objects.count(), 1)
