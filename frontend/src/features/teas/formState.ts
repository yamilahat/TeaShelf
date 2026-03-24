import type { Tea, TeaInput } from "./api";

export type TeaFormState = {
  name: string;
  vendor: string;
  origin: string;
  tea_type: string;
  initial_quantity_g: string;
  current_quantity_g: string;
  harvest_year: string;
  notes: string;
};

export const initialTeaFormState: TeaFormState = {
  name: "",
  vendor: "",
  origin: "",
  tea_type: "",
  initial_quantity_g: "",
  current_quantity_g: "",
  harvest_year: "",
  notes: "",
};

export function toTeaFormState(tea?: Tea): TeaFormState {
  if (!tea) {
    return initialTeaFormState;
  }

  return {
    name: tea.name,
    vendor: tea.vendor ?? "",
    origin: tea.origin ?? "",
    tea_type: tea.tea_type ?? "",
    initial_quantity_g: tea.initial_quantity_g?.toString() ?? "",
    current_quantity_g: tea.current_quantity_g?.toString() ?? "",
    harvest_year: tea.harvest_year?.toString() ?? "",
    notes: tea.notes ?? "",
  };
}

export function toTeaPayload(form: TeaFormState): TeaInput {
  return {
    name: form.name.trim(),
    vendor: form.vendor.trim() || null,
    origin: form.origin.trim() || null,
    tea_type: form.tea_type.trim() || null,
    initial_quantity_g: form.initial_quantity_g ? Number(form.initial_quantity_g) : null,
    current_quantity_g: form.current_quantity_g ? Number(form.current_quantity_g) : null,
    harvest_year: form.harvest_year ? Number(form.harvest_year) : null,
    notes: form.notes.trim() || null,
  };
}
