from django.contrib import admin
from django.urls import path

from scheduling.views import AppointmentCreateView, DoctorListView, DoctorSlotsView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/doctors/", DoctorListView.as_view(), name="doctor-list"),
    path("api/doctors/<int:doctor_id>/slots/", DoctorSlotsView.as_view(), name="doctor-slots"),
    path("api/appointments/", AppointmentCreateView.as_view(), name="appointment-create"),
]
