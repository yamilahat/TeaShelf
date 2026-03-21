import { useState } from "react";
import type { FormEvent } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { createTeaware } from "../features/teaware/api";
import { TeawareForm } from "../features/teaware/TeawareForm";
import {
  initialTeawareFormState,
  type TeawareFormState,
  toTeawarePayload,
} from "../features/teaware/formState";

export function NewTeawarePage() {
  const [form, setForm] = useState<TeawareFormState>(initialTeawareFormState);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: createTeaware,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["teaware"] });
      navigate("/teaware");
    },
  });

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    mutation.mutate(toTeawarePayload(form));
  }

  return (
    <section className="panel panel--form">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Create</p>
          <h2>New teaware</h2>
        </div>
        <p className="muted">Add a piece of brewing equipment to your collection.</p>
      </div>

      <TeawareForm
        form={form}
        onChange={setForm}
        onSubmit={handleSubmit}
        submitLabel="Create teaware"
        isSubmitting={mutation.isPending}
        errorMessage={mutation.isError ? (mutation.error as Error).message : null}
      />
    </section>
  );
}
