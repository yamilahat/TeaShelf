import { ddmmyyyyToISO, todayISO } from "../../lib/dateUtils";
import type { TeaSession, TeaSessionInput } from "./api";

export type TeaSessionFormState = {
  tea_id: string;
  teaware_id: string;
  session_date: string; // YYYY-MM-DD for <input type="date">
  steeps_count: string;
  rating: string;
  notes: string;
};

export const initialTeaSessionFormState: TeaSessionFormState = {
  tea_id: "",
  teaware_id: "",
  session_date: todayISO(),
  steeps_count: "",
  rating: "",
  notes: "",
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
    rating: session.rating?.toString() ?? "",
    notes: session.notes ?? "",
  };
}

export function toTeaSessionPayload(form: TeaSessionFormState): TeaSessionInput {
  return {
    tea_id: Number(form.tea_id),
    teaware_id: form.teaware_id ? Number(form.teaware_id) : null,
    session_date: form.session_date, // YYYY-MM-DD, backend accepts it
    steeps_count: form.steeps_count ? Number(form.steeps_count) : null,
    rating: form.rating ? Number(form.rating) : null,
    notes: form.notes.trim() || null,
  };
}
