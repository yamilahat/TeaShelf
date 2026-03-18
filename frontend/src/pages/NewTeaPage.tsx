import { useState } from "react";
import type { FormEvent } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { createTea } from "../features/teas/api";
import { TeaForm } from "../features/teas/TeaForm";
import {
  initialTeaFormState,
  type TeaFormState,
  toTeaPayload,
} from "../features/teas/formState";

export function NewTeaPage() {
  const [form, setForm] = useState<TeaFormState>(initialTeaFormState);
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
    mutation.mutate(toTeaPayload(form));
  }

  return (
    <section className="panel panel--form">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Create</p>
          <h2>New tea</h2>
        </div>
        <p className="muted">Add a tea you want to keep track of.</p>
      </div>

      <TeaForm
        form={form}
        onChange={setForm}
        onSubmit={handleSubmit}
        submitLabel="Create tea"
        isSubmitting={mutation.isPending}
        errorMessage={mutation.isError ? (mutation.error as Error).message : null}
      />
    </section>
  );
}
