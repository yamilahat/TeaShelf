import { apiFetch } from "../../lib/api";

export type Tea = {
  id: number;
  name: string;
  vendor: string | null;
  origin: string | null;
  tea_type: string | null;
  harvest_year: number | null;
  notes: string | null;
};

export type TeaInput = {
  name: string;
  vendor?: string | null;
  origin?: string | null;
  tea_type?: string | null;
  harvest_year?: number | null;
  notes?: string | null;
};

export function listTeas() {
  return apiFetch<Tea[]>("/teas");
}

export function getTea(teaId: number) {
  return apiFetch<Tea>(`/teas/${teaId}`);
}

export function createTea(input: TeaInput) {
  return apiFetch<Tea>("/teas", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function updateTea(teaId: number, input: TeaInput) {
  return apiFetch<Tea>(`/teas/${teaId}`, {
    method: "PUT",
    body: JSON.stringify(input),
  });
}

export function deleteTea(teaId: number) {
  return apiFetch<void>(`/teas/${teaId}`, {
    method: "DELETE",
  });
}
