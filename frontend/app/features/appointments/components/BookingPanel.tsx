import type { FormEvent } from "react";
import type { UseMutationResult } from "@tanstack/react-query";
import { formatSlotTime } from "../lib/date";
import type { Appointment, Slot } from "../types";

type BookingPanelProps = {
  selectedSlot: Slot | null;
  patientName: string;
  patientPhone: string;
  formError: string;
  appointmentMutation: UseMutationResult<Appointment, Error, void, unknown>;
  onPatientNameChange: (value: string) => void;
  onPatientPhoneChange: (value: string) => void;
  onSubmit: () => void;
};

export function BookingPanel({
  selectedSlot,
  patientName,
  patientPhone,
  formError,
  appointmentMutation,
  onPatientNameChange,
  onPatientPhoneChange,
  onSubmit,
}: BookingPanelProps) {
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <aside className="panel booking-panel">
      <div className="section-title">Бронирование</div>
      <div className="selected-slot">
        {selectedSlot ? (
          <>
            <span>Выбранное время</span>
            <strong>{formatSlotTime(selectedSlot.start_at)}</strong>
          </>
        ) : (
          <span>Выберите свободный слот в расписании</span>
        )}
      </div>

      <form onSubmit={submit} className="booking-form">
        <div className="field">
          <label htmlFor="patientName">Имя пациента</label>
          <input
            id="patientName"
            value={patientName}
            onChange={(event) => onPatientNameChange(event.target.value)}
            placeholder="Иван Петров"
            minLength={2}
            required
          />
        </div>
        <div className="field">
          <label htmlFor="patientPhone">Телефон</label>
          <input
            id="patientPhone"
            value={patientPhone}
            onChange={(event) => onPatientPhoneChange(event.target.value)}
            placeholder="+7 700 123 45 67"
            autoComplete="tel"
            inputMode="tel"
            pattern="^\+?[\d\s().-]{7,32}$"
            required
          />
        </div>
        {formError && <div className="error-text">{formError}</div>}
        {appointmentMutation.isSuccess && <div className="success-text">Запись создана</div>}
        <button className="primary-action" type="submit" disabled={!selectedSlot || appointmentMutation.isPending}>
          {appointmentMutation.isPending ? "Бронируем" : "Забронировать"}
        </button>
      </form>
    </aside>
  );
}
