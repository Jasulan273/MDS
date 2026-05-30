import type { UseQueryResult } from "@tanstack/react-query";
import { formatSlotTime } from "../lib/date";
import { getQueryErrorText } from "../lib/errors";
import type { Doctor, Slot } from "../types";

type SlotScheduleProps = {
  selectedDoctor: Doctor | null;
  selectedSlot: Slot | null;
  slotsQuery: UseQueryResult<Slot[]>;
  onSlotSelect: (slot: Slot) => void;
};

export function SlotSchedule({ selectedDoctor, selectedSlot, slotsQuery, onSlotSelect }: SlotScheduleProps) {
  return (
    <section className="panel schedule-panel">
      <div className="schedule-head">
        <div>
          <div className="section-title">Слоты</div>
          <h2>{selectedDoctor ? selectedDoctor.name : "Выберите врача"}</h2>
        </div>
        <div className="legend">
          <span>
            <i className="free-dot" /> Свободен
          </span>
          <span>
            <i className="booked-dot" /> Занят
          </span>
        </div>
      </div>

      {slotsQuery.isLoading && <div className="muted">Загрузка расписания</div>}
      {slotsQuery.isError && <div className="error-text">{getQueryErrorText(slotsQuery.error)}</div>}
      {!slotsQuery.isLoading && slotsQuery.data?.length === 0 && <div className="empty-state">На эту дату слотов нет</div>}

      <div className="slots-grid">
        {slotsQuery.data?.map((slot) => {
          const isFree = slot.status === "free";
          const isSelected = selectedSlot?.id === slot.id;

          return (
            <button
              key={slot.id}
              type="button"
              className={isSelected ? "slot selected" : `slot ${slot.status}`}
              disabled={!isFree}
              onClick={() => onSlotSelect(slot)}
            >
              <strong>{formatSlotTime(slot.start_at)}</strong>
              <span>{isFree ? "Свободен" : "Занят"}</span>
            </button>
          );
        })}
      </div>
    </section>
  );
}
