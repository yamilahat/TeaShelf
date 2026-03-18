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

export type CreateTeaInput = {
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

export function createTea(input: CreateTeaInput) {
    return apiFetch<Tea>("/teas", {
        method: "POST",
        body: JSON.stringify(input)
    })
}