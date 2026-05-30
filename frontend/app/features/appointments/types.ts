export type Clinic = {
  id: string;
  name: string;
};

export type Doctor = {
  id: number;
  name: string;
  specialization: string;
};

export type SlotStatus = "free" | "booked";

export type Slot = {
  id: number;
  doctor_id: number;
  start_at: string;
  duration_minutes: number;
  status: SlotStatus;
};

export type Appointment = {
  id: number;
  slot_id: number;
  patient_name: string;
  patient_phone: string;
  created_at: string;
};

export type AppointmentInput = {
  slot_id: number;
  patient_name: string;
  patient_phone: string;
};
