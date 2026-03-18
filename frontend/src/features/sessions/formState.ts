import type { TeaSession, TeaSessionInput } from "./api";

export type TeaSessionFormState = {
  tea_id: string;
  session_date: string;
  steeps_count: string;
  rating: string;
  notes: string;
};

export const initialTeaSessionFormState: TeaSessionFormState = {
  tea_id: "",
  session_date: "",
  steeps_count: "",
  rating: "",
  notes: "",
};

function toDateTimeLocalInput(value: string): string {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  const timezoneOffsetMs = date.getTimezoneOffset() * 60_000;
  return new Date(date.getTime() - timezoneOffsetMs).toISOString().slice(0, 16);
}

export function toTeaSessionFormState(session?: TeaSession): TeaSessionFormState {
  if (!session) {
    return initialTeaSessionFormState;
  }

  return {
    tea_id: session.tea_id.toString(),
    session_date: toDateTimeLocalInput(session.session_date),
    steeps_count: session.steeps_count?.toString() ?? "",
    rating: session.rating?.toString() ?? "",
    notes: session.notes ?? "",
  };
}

export function toTeaSessionPayload(
  form: TeaSessionFormState,
): TeaSessionInput {
  return {
    tea_id: Number(form.tea_id),
    session_date: new Date(form.session_date).toISOString(),
    steeps_count: form.steeps_count ? Number(form.steeps_count) : null,
    rating: form.rating ? Number(form.rating) : null,
    notes: form.notes.trim() || null,
  };
}
