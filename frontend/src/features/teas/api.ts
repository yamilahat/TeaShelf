import { apiFetch } from "../../lib/api";

export type Tea = {
    id: number;
    name: string;
    vendor: string | null;
    origin: string | null;
    tea_type: string | null;
    harvest_year: number | null;
    notes: string | null;
}

export type CreateTeaInput = {}