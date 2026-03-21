import { apiFetch } from "../../lib/api";

export type Teaware = {
  id: number;
  name: string;
  nickname: string | null;
  type: string | null;
  volume_ml: number | null;
  material: string | null;
  vendor: string | null;
  preferred_tea_types: string[];
  acquired_date: string | null;
  notes: string | null;
};

export type TeawareInput = {
  name: string;
  nickname?: string | null;
  type?: string | null;
  volume_ml?: number | null;
  material?: string | null;
  vendor?: string | null;
  preferred_tea_types?: string[];
  acquired_date?: string | null;
  notes?: string | null;
};

export function listTeaware() {
  return apiFetch<Teaware[]>("/teaware");
}

export function getTeaware(teawareId: number) {
  return apiFetch<Teaware>(`/teaware/${teawareId}`);
}

export function createTeaware(input: TeawareInput) {
  return apiFetch<Teaware>("/teaware", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function updateTeaware(teawareId: number, input: TeawareInput) {
  return apiFetch<Teaware>(`/teaware/${teawareId}`, {
    method: "PUT",
    body: JSON.stringify(input),
  });
}

export function deleteTeaware(teawareId: number) {
  return apiFetch<void>(`/teaware/${teawareId}`, {
    method: "DELETE",
  });
}
