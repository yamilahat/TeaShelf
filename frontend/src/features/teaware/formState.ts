import type { Teaware, TeawareInput } from "./api";

export type TeawareFormState = {
  name: string;
  nickname: string;
  type: string;
  volume_ml: string;
  material: string;
  vendor: string;
  preferred_tea_types: string[];
  acquired_date: string;
  notes: string;
};

export const initialTeawareFormState: TeawareFormState = {
  name: "",
  nickname: "",
  type: "",
  volume_ml: "",
  material: "",
  vendor: "",
  preferred_tea_types: [],
  acquired_date: "",
  notes: "",
};

export function toTeawareFormState(teaware?: Teaware): TeawareFormState {
  if (!teaware) {
    return initialTeawareFormState;
  }

  return {
    name: teaware.name,
    nickname: teaware.nickname ?? "",
    type: teaware.type ?? "",
    volume_ml: teaware.volume_ml?.toString() ?? "",
    material: teaware.material ?? "",
    vendor: teaware.vendor ?? "",
    preferred_tea_types: teaware.preferred_tea_types ?? [],
    acquired_date: teaware.acquired_date ?? "",
    notes: teaware.notes ?? "",
  };
}

export function toTeawarePayload(form: TeawareFormState): TeawareInput {
  return {
    name: form.name.trim(),
    nickname: form.nickname.trim() || null,
    type: form.type.trim() || null,
    volume_ml: form.volume_ml ? Number(form.volume_ml) : null,
    material: form.material.trim() || null,
    vendor: form.vendor.trim() || null,
    preferred_tea_types: form.preferred_tea_types,
    acquired_date: form.acquired_date || null,
    notes: form.notes.trim() || null,
  };
}
