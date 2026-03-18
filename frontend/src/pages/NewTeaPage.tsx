import { FormEvent, useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { createTea } from "../features/teas/api";

type TeaFormState = {
  name: string;
  vendor: string;
  origin: string;
  tea_type: string;
  harvest_year: string;
  notes: string;
};

const initialState: TeaFormState = {
  name: "",
  vendor: "",
  origin: "",
  tea_type: "",
  harvest_year: "",
  notes: "",
};

export function NewTeaPage() {
  const [form, setForm] = useState<TeaFormState>(initialState);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: createTea,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["teas"] });
      navigate("/teas");
    },
  });

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    mutation.mutate({
      name: form.name,
      vendor: form.vendor || null,
      origin: form.origin || null,
      tea_type: form.tea_type || null,
      harvest_year: form.harvest_year ? Number(form.harvest_year) : null,
      notes: form.notes || null,
    });
  }

  return (
    <div className="max-w-2xl space-y-4">
      <h2 className="text-2xl font-semibold">New tea</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          className="w-full rounded-lg border p-3"
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />

        <input
          className="w-full rounded-lg border p-3"
          placeholder="Vendor"
          value={form.vendor}
          onChange={(e) => setForm({ ...form, vendor: e.target.value })}
        />

        <input
          className="w-full rounded-lg border p-3"
          placeholder="Origin"
          value={form.origin}
          onChange={(e) => setForm({ ...form, origin: e.target.value })}
        />

        <input
          className="w-full rounded-lg border p-3"
          placeholder="Tea type"
          value={form.tea_type}
          onChange={(e) => setForm({ ...form, tea_type: e.target.value })}
        />

        <input
          className="w-full rounded-lg border p-3"
          placeholder="Harvest year"
          type="number"
          value={form.harvest_year}
          onChange={(e) => setForm({ ...form, harvest_year: e.target.value })}
        />

        <textarea
          className="min-h-32 w-full rounded-lg border p-3"
          placeholder="Notes"
          value={form.notes}
          onChange={(e) => setForm({ ...form, notes: e.target.value })}
        />

        <button
          type="submit"
          disabled={mutation.isPending}
          className="rounded-lg border px-4 py-2"
        >
          {mutation.isPending ? "Saving..." : "Create tea"}
        </button>

        {mutation.isError && (
          <p className="text-red-600">{(mutation.error as Error).message}</p>
        )}
      </form>
    </div>
  );
}