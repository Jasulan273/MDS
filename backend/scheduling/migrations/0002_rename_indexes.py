from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("scheduling", "0001_initial"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="appointment",
            old_name="scheduling__clinic_297771_idx",
            new_name="appointment_clinic_created_idx",
        ),
        migrations.RenameIndex(
            model_name="doctor",
            old_name="scheduling__clinic_7213af_idx",
            new_name="doctor_clinic_name_idx",
        ),
        migrations.RenameIndex(
            model_name="slot",
            old_name="scheduling__clinic_89a997_idx",
            new_name="slot_clinic_doctor_start_idx",
        ),
        migrations.RenameIndex(
            model_name="slot",
            old_name="scheduling__clinic_07bf88_idx",
            new_name="slot_clinic_status_idx",
        ),
    ]
