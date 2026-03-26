import { ddmmyyyyToISO, todayISO } from "../../lib/dateUtils";
import type { TeaSession, TeaSessionInput } from "./api";

export type SteepInfusionFormRow = {
  steep_number: string;
  steep_time_seconds: string;
};

export type TeaSessionFormState = {
  tea_id: string;
  teaware_id: string;
  session_date: string; // YYYY-MM-DD for <input type="date">
  steeps_count: string;
  water_temp_c: string;
  leaf_weight_g: string;
  water_volume_ml: string;
  brew_method: string;
  rating: string;
  notes: string;
  steep_infusions: SteepInfusionFormRow[];
};

export const initialTeaSessionFormState: TeaSessionFormState = {
  tea_id: "",
  teaware_id: "",
  session_date: todayISO(),
  steeps_count: "",
  water_temp_c: "",
  leaf_weight_g: "",
  water_volume_ml: "",
  brew_method: "",
  rating: "",
  notes: "",
  steep_infusions: [],
};

export function toTeaSessionFormState(session?: TeaSession): TeaSessionFormState {
  if (!session) {
    return initialTeaSessionFormState;
  }

  return {
    tea_id: session.tea_id.toString(),
    teaware_id: session.teaware_id?.toString() ?? "",
    session_date: ddmmyyyyToISO(session.session_date), // API returns DD/MM/YYYY → convert for date input
    steeps_count: session.steeps_count?.toString() ?? "",
    water_temp_c: session.water_temp_c?.toString() ?? "",
    leaf_weight_g: session.leaf_weight_g?.toString() ?? "",
    water_volume_ml: session.water_volume_ml?.toString() ?? "",
    brew_method: session.brew_method ?? "",
    rating: session.rating?.toString() ?? "",
    notes: session.notes ?? "",
    steep_infusions: session.steep_infusions.map((inf) => ({
      steep_number: inf.steep_number.toString(),
      steep_time_seconds: inf.steep_time_seconds.toString(),
    })),
  };
}

export function toTeaSessionPayload(form: TeaSessionFormState): TeaSessionInput {
  return {
    tea_id: Number(form.tea_id),
    teaware_id: form.teaware_id ? Number(form.teaware_id) : null,
    session_date: form.session_date, // YYYY-MM-DD, backend accepts it
    steeps_count: form.steeps_count ? Number(form.steeps_count) : null,
    water_temp_c: form.water_temp_c ? Number(form.water_temp_c) : null,
    leaf_weight_g: form.leaf_weight_g ? Number(form.leaf_weight_g) : null,
    water_volume_ml: form.water_volume_ml ? Number(form.water_volume_ml) : null,
    brew_method: form.brew_method.trim() || null,
    rating: form.rating ? Number(form.rating) : null,
    notes: form.notes.trim() || null,
    steep_infusions: form.steep_infusions
      .filter((row) => row.steep_time_seconds !== "")
      .map((row) => ({
        steep_number: Number(row.steep_number),
        steep_time_seconds: Number(row.steep_time_seconds),
      })),
  };
}
