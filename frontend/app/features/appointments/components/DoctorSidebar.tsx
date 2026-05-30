import type { UseQueryResult } from "@tanstack/react-query";
import { getDateInputValue } from "../lib/date";
import { getQueryErrorText } from "../lib/errors";
import type { Doctor } from "../types";

type DoctorSidebarProps = {
  date: string;
  doctorId: number | null;
  doctorsQuery: UseQueryResult<Doctor[]>;
  onDateChange: (date: string) => void;
  onDoctorChange: (doctorId: number) => void;
};

export function DoctorSidebar({ date, doctorId, doctorsQuery, onDateChange, onDoctorChange }: DoctorSidebarProps) {
  return (
    <aside className="panel">
      <div className="field">
        <label htmlFor="date">Дата</label>
        <input
          id="date"
          type="date"
          value={date}
          min={getDateInputValue()}
          onChange={(event) => onDateChange(event.target.value)}
        />
      </div>

      <div className="doctor-list">
        <div className="section-title">Врачи</div>
        {doctorsQuery.isLoading && <div className="muted">Загрузка врачей</div>}
        {doctorsQuery.isError && <div className="error-text">{getQueryErrorText(doctorsQuery.error)}</div>}
        {doctorsQuery.data?.map((doctor) => (
          <button
            key={doctor.id}
            className={doctor.id === doctorId ? "doctor active" : "doctor"}
            type="button"
            onClick={() => onDoctorChange(doctor.id)}
          >
            <span>{doctor.name}</span>
            <small>{doctor.specialization}</small>
          </button>
        ))}
      </div>
    </aside>
  );
}
