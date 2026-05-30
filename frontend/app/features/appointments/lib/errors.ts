import { ApiError } from "../api";

type ErrorDetails = {
  detail?: string;
  slot_id?: string | string[];
  patient_name?: string | string[];
  patient_phone?: string | string[];
};

function firstMessage(value: unknown) {
  if (Array.isArray(value)) {
    return String(value[0] ?? "");
  }
  if (typeof value === "string") {
    return value;
  }
  return "";
}

export function getQueryErrorText(error: unknown) {
  if (error instanceof ApiError) {
    return "Не удалось получить данные";
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "Не удалось выполнить запрос";
}

export function getBookingErrorText(error: unknown) {
  if (error instanceof ApiError && error.details && typeof error.details === "object") {
    const details = error.details as ErrorDetails;
    return (
      firstMessage(details.slot_id) ||
      firstMessage(details.patient_name) ||
      firstMessage(details.patient_phone) ||
      details.detail ||
      "Не удалось создать запись"
    );
  }
  return "Не удалось создать запись";
}
