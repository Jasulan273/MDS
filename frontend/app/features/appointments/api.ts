import type { Appointment, AppointmentInput, Doctor, Slot } from "./types";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

type RequestOptions = {
  clinicId: string;
  method?: "GET" | "POST";
  body?: unknown;
};

export class ApiError extends Error {
  status: number;
  details: unknown;

  constructor(status: number, details: unknown) {
    super("API request failed");
    this.status = status;
    this.details = details;
  }
}

async function request<T>(path: string, options: RequestOptions): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
      "Clinic-Id": options.clinicId,
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    let details: unknown = null;
    try {
      details = await response.json();
    } catch {
      details = await response.text();
    }
    throw new ApiError(response.status, details);
  }

  return response.json() as Promise<T>;
}

export function getDoctors(clinicId: string) {
  return request<Doctor[]>("/doctors/", { clinicId });
}

export function getSlots(clinicId: string, doctorId: number, date: string) {
  return request<Slot[]>(`/doctors/${doctorId}/slots/?date=${date}`, { clinicId });
}

export function createAppointment(clinicId: string, input: AppointmentInput) {
  return request<Appointment>("/appointments/", {
    clinicId,
    method: "POST",
    body: input,
  });
}
