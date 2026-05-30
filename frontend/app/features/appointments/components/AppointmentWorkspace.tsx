import { clinics } from "../model/clinics";
import { useAppointmentBooking } from "../hooks/useAppointmentBooking";
import { BookingPanel } from "./BookingPanel";
import { ClinicSwitcher } from "./ClinicSwitcher";
import { DoctorSidebar } from "./DoctorSidebar";
import { SlotSchedule } from "./SlotSchedule";

export function AppointmentWorkspace() {
  const booking = useAppointmentBooking();

  return (
    <main className="page-shell">
      <section className="workspace">
        <div className="topbar">
          <div>
            <p className="eyebrow">Запись пациента</p>
            <h1>Расписание врачей</h1>
          </div>
          <ClinicSwitcher clinics={clinics} selectedClinicId={booking.clinicId} onChange={booking.changeClinic} />
        </div>

        <div className="layout-grid">
          <DoctorSidebar
            date={booking.date}
            doctorId={booking.doctorId}
            doctorsQuery={booking.doctorsQuery}
            onDateChange={booking.changeDate}
            onDoctorChange={booking.changeDoctor}
          />
          <SlotSchedule
            selectedDoctor={booking.selectedDoctor}
            selectedSlot={booking.selectedSlot}
            slotsQuery={booking.slotsQuery}
            onSlotSelect={booking.chooseSlot}
          />
          <BookingPanel
            selectedSlot={booking.selectedSlot}
            patientName={booking.patientName}
            patientPhone={booking.patientPhone}
            formError={booking.formError}
            appointmentMutation={booking.appointmentMutation}
            onPatientNameChange={booking.changePatientName}
            onPatientPhoneChange={booking.changePatientPhone}
            onSubmit={booking.submitBooking}
          />
        </div>
      </section>
    </main>
  );
}
