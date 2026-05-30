from datetime import datetime, time, timedelta

from django.core.management.color import no_style
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from scheduling.models import Clinic, Doctor, Slot


class Command(BaseCommand):
    def handle(self, *args, **options):
        clinics = [
            (1, "Central Clinic"),
            (2, "North Clinic"),
        ]
        doctors = {
            1: [
                ("Анна Миронова", "Кардиолог"),
                ("Илья Сафин", "Терапевт"),
                ("Мария Волкова", "Невролог"),
            ],
            2: [
                ("Олег Петров", "Ортопед"),
                ("Елена Ким", "Эндокринолог"),
            ],
        }
        slot_times = [time(9, 0), time(9, 30), time(10, 0), time(11, 0), time(14, 0), time(15, 30)]
        today = timezone.localdate()

        for clinic_id, clinic_name in clinics:
            clinic, _ = Clinic.objects.update_or_create(id=clinic_id, defaults={"name": clinic_name})
            for name, specialization in doctors[clinic_id]:
                doctor, _ = Doctor.objects.update_or_create(
                    clinic=clinic,
                    name=name,
                    specialization=specialization,
                    defaults={},
                )
                for day_offset in range(7):
                    current_date = today + timedelta(days=day_offset)
                    for slot_time in slot_times:
                        start_at = timezone.make_aware(datetime.combine(current_date, slot_time))
                        Slot.objects.get_or_create(
                            clinic=clinic,
                            doctor=doctor,
                            start_at=start_at,
                            defaults={"duration_minutes": 30, "status": Slot.Status.FREE},
                        )

        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Clinic])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS("Seed data is ready."))
