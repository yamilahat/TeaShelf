import { apiFetch } from "../../lib/api";

export type SteepInfusion = {
  id: number;
  session_id: number;
  steep_number: number;
  steep_time_seconds: number;
};

export type SteepInfusionInput = {
  steep_number: number;
  steep_time_seconds: number;
};

export type TeaSession = {
  id: number;
  tea_id: number;
  teaware_id: number | null;
  session_date: string; // DD/MM/YYYY from API
  steeps_count: number | null;
  water_temp_c: number | null;
  leaf_weight_g: number | null;
  water_volume_ml: number | null;
  brew_method: string | null;
  rating: number | null;
  notes: string | null;
  steep_infusions: SteepInfusion[];
};

export type TeaSessionInput = {
  tea_id: number;
  teaware_id?: number | null;
  session_date: string; // YYYY-MM-DD
  steeps_count?: number | null;
  water_temp_c?: number | null;
  leaf_weight_g?: number | null;
  water_volume_ml?: number | null;
  brew_method?: string | null;
  rating?: number | null;
  notes?: string | null;
  steep_infusions?: SteepInfusionInput[];
};

export function listSessions() {
  return apiFetch<TeaSession[]>("/sessions");
}

export function getSession(sessionId: number) {
  return apiFetch<TeaSession>(`/sessions/${sessionId}`);
}

export function createSession(input: TeaSessionInput) {
  return apiFetch<TeaSession>("/sessions", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function updateSession(sessionId: number, input: TeaSessionInput) {
  return apiFetch<TeaSession>(`/sessions/${sessionId}`, {
    method: "PUT",
    body: JSON.stringify(input),
  });
}

export function deleteSession(sessionId: number) {
  return apiFetch<void>(`/sessions/${sessionId}`, {
    method: "DELETE",
  });
}
