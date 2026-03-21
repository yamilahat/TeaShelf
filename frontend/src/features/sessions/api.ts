import { apiFetch } from "../../lib/api";

export type TeaSession = {
  id: number;
  tea_id: number;
  teaware_id: number | null;
  session_date: string; // DD/MM/YYYY from API
  steeps_count: number | null;
  rating: number | null;
  notes: string | null;
};

export type TeaSessionInput = {
  tea_id: number;
  teaware_id?: number | null;
  session_date: string; // YYYY-MM-DD
  steeps_count?: number | null;
  rating?: number | null;
  notes?: string | null;
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
