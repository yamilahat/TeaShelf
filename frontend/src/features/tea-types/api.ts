import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../../lib/api";

export type TeaType = {
  id: number;
  name: string;
  category: string;
};

type TeaTypeOption = { value: string; label: string };

export function listTeaTypes() {
  return apiFetch<TeaType[]>("/tea-types");
}

export function teaTypeLabel(name: string) {
  return name.replace(/\b\w/g, (c) => c.toUpperCase());
}

function toOptions(types: TeaType[]): TeaTypeOption[] {
  return types.map((t) => ({ value: t.name, label: teaTypeLabel(t.name) }));
}

export function useTeaTypeOptions(): TeaTypeOption[] {
  const { data } = useQuery({
    queryKey: ["tea-types"],
    queryFn: listTeaTypes,
    staleTime: Infinity,
  });
  return data ? toOptions(data) : [];
}
