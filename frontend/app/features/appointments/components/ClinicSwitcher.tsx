import type { Clinic } from "../types";

type ClinicSwitcherProps = {
  clinics: Clinic[];
  selectedClinicId: string;
  onChange: (clinicId: string) => void;
};

export function ClinicSwitcher({ clinics, selectedClinicId, onChange }: ClinicSwitcherProps) {
  return (
    <div className="clinic-switcher" aria-label="Клиника">
      {clinics.map((clinic) => (
        <button
          key={clinic.id}
          className={selectedClinicId === clinic.id ? "active" : ""}
          type="button"
          onClick={() => onChange(clinic.id)}
        >
          {clinic.name}
        </button>
      ))}
    </div>
  );
}
