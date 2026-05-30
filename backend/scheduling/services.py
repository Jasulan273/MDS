from django.db import IntegrityError, transaction

from scheduling.models import Appointment, Slot


class SlotAlreadyBooked(Exception):
    ...


def book_slot(*, clinic, slot_id, patient_name, patient_phone):
    with transaction.atomic():
        slot = Slot.objects.select_for_update().select_related("doctor").get(id=slot_id, clinic=clinic)

        if slot.status == Slot.Status.BOOKED or hasattr(slot, "appointment"):
            raise SlotAlreadyBooked

        try:
            appointment = Appointment.objects.create(
                clinic=clinic,
                slot=slot,
                patient_name=patient_name,
                patient_phone=patient_phone,
            )
        except IntegrityError as exc:
            raise SlotAlreadyBooked from exc

        slot.status = Slot.Status.BOOKED
        slot.save(update_fields=["status"])
        return appointment
