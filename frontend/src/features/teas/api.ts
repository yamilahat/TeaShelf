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

export type TeaFilters = {
  tea_type?: string;
  vendor?: string;
  name?: string;
};

export function listTeas(filters?: TeaFilters) {
  const params = new URLSearchParams();
  if (filters?.tea_type) params.set("tea_type", filters.tea_type);
  if (filters?.vendor) params.set("vendor", filters.vendor);
  if (filters?.name) params.set("name", filters.name);
  const qs = params.toString();
  return apiFetch<Tea[]>(qs ? `/teas?${qs}` : "/teas");
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
