import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { createAppointment, getDoctors, getSlots } from "../api";
import { getDateInputValue } from "../lib/date";
import { getBookingErrorText } from "../lib/errors";
import type { Slot } from "../types";

const phonePattern = /^\+?[\d\s().-]{7,32}$/;

export function useAppointmentBooking() {
  const queryClient = useQueryClient();
  const [clinicId, setClinicId] = useState("1");
  const [date, setDate] = useState(getDateInputValue());
  const [doctorId, setDoctorId] = useState<number | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<Slot | null>(null);
  const [patientName, setPatientName] = useState("");
  const [patientPhone, setPatientPhone] = useState("");
  const [formError, setFormError] = useState("");

  const doctorsQuery = useQuery({
    queryKey: ["doctors", clinicId],
    queryFn: () => getDoctors(clinicId),
  });

  const activeDoctorId = useMemo(() => {
    const doctors = doctorsQuery.data ?? [];
    if (doctors.length === 0) {
      return null;
    }
    if (doctorId && doctors.some((doctor) => doctor.id === doctorId)) {
      return doctorId;
    }
    return doctors[0].id;
  }, [doctorId, doctorsQuery.data]);

  const selectedDoctor = useMemo(
    () => doctorsQuery.data?.find((doctor) => doctor.id === activeDoctorId) ?? null,
    [activeDoctorId, doctorsQuery.data],
  );

  const slotsQuery = useQuery({
    queryKey: ["slots", clinicId, activeDoctorId, date],
    queryFn: () => getSlots(clinicId, activeDoctorId as number, date),
    enabled: activeDoctorId !== null,
  });

  const appointmentMutation = useMutation({
    mutationFn: () =>
      createAppointment(clinicId, {
        slot_id: selectedSlot?.id ?? 0,
        patient_name: patientName.trim(),
        patient_phone: patientPhone.trim(),
      }),
    onSuccess: async () => {
      setPatientName("");
      setPatientPhone("");
      setSelectedSlot(null);
      setFormError("");
      await queryClient.invalidateQueries({ queryKey: ["slots", clinicId, activeDoctorId, date] });
    },
    onError: (error) => {
      setFormError(getBookingErrorText(error));
    },
  });

  function resetFeedback() {
    setFormError("");
    appointmentMutation.reset();
  }

  function changeClinic(nextClinicId: string) {
    setClinicId(nextClinicId);
    setDoctorId(null);
    setSelectedSlot(null);
    resetFeedback();
  }

  function changeDate(nextDate: string) {
    setDate(nextDate);
    setSelectedSlot(null);
    resetFeedback();
  }

  function changeDoctor(nextDoctorId: number) {
    setDoctorId(nextDoctorId);
    setSelectedSlot(null);
    resetFeedback();
  }

  function chooseSlot(slot: Slot) {
    setSelectedSlot(slot);
    resetFeedback();
  }

  function changePatientName(value: string) {
    setPatientName(value);
    resetFeedback();
  }

  function changePatientPhone(value: string) {
    setPatientPhone(value);
    resetFeedback();
  }

  function submitBooking() {
    const trimmedName = patientName.trim();
    const trimmedPhone = patientPhone.trim();

    if (!selectedSlot) {
      setFormError("Выберите свободный слот");
      return;
    }
    if (trimmedName.length < 2) {
      setFormError("Введите имя пациента");
      return;
    }
    if (!phonePattern.test(trimmedPhone)) {
      setFormError("Введите корректный телефон");
      return;
    }

    setFormError("");
    appointmentMutation.mutate();
  }

  return {
    clinicId,
    date,
    doctorId: activeDoctorId,
    selectedDoctor,
    selectedSlot,
    patientName,
    patientPhone,
    formError,
    doctorsQuery,
    slotsQuery,
    appointmentMutation,
    changeClinic,
    changeDate,
    changeDoctor,
    chooseSlot,
    changePatientName,
    changePatientPhone,
    submitBooking,
  };
}
