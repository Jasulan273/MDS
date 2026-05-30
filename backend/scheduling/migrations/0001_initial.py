import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Clinic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("specialization", models.CharField(max_length=120)),
                (
                    "clinic",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="doctors", to="scheduling.clinic"),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Slot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_at", models.DateTimeField()),
                (
                    "duration_minutes",
                    models.PositiveSmallIntegerField(default=30, validators=[django.core.validators.MinValueValidator(5)]),
                ),
                (
                    "status",
                    models.CharField(choices=[("free", "Free"), ("booked", "Booked")], default="free", max_length=16),
                ),
                (
                    "clinic",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="slots", to="scheduling.clinic"),
                ),
                (
                    "doctor",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="slots", to="scheduling.doctor"),
                ),
            ],
            options={"ordering": ["start_at"]},
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("patient_name", models.CharField(max_length=120)),
                ("patient_phone", models.CharField(max_length=32)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "clinic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="appointments", to="scheduling.clinic"
                    ),
                ),
                (
                    "slot",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT, related_name="appointment", to="scheduling.slot"
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="doctor",
            index=models.Index(fields=["clinic", "name"], name="scheduling__clinic_7213af_idx"),
        ),
        migrations.AddConstraint(
            model_name="doctor",
            constraint=models.UniqueConstraint(fields=("clinic", "name", "specialization"), name="unique_doctor_per_clinic"),
        ),
        migrations.AddIndex(
            model_name="slot",
            index=models.Index(fields=["clinic", "doctor", "start_at"], name="scheduling__clinic_89a997_idx"),
        ),
        migrations.AddIndex(
            model_name="slot",
            index=models.Index(fields=["clinic", "status"], name="scheduling__clinic_07bf88_idx"),
        ),
        migrations.AddConstraint(
            model_name="slot",
            constraint=models.UniqueConstraint(fields=("clinic", "doctor", "start_at"), name="unique_slot_start_per_doctor"),
        ),
        migrations.AddIndex(
            model_name="appointment",
            index=models.Index(fields=["clinic", "created_at"], name="scheduling__clinic_297771_idx"),
        ),
    ]
