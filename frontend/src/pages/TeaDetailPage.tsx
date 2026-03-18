import { useState } from "react";
import type { FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, useNavigate, useParams } from "react-router";
import { deleteTea, getTea, updateTea } from "../features/teas/api";
import { TeaForm } from "../features/teas/TeaForm";
import {
  type TeaFormState,
  toTeaFormState,
  toTeaPayload,
} from "../features/teas/formState";

export function TeaDetailPage() {
  const params = useParams();
  const teaId = Number(params.teaId);

  const teaQuery = useQuery({
    queryKey: ["teas", teaId],
    queryFn: () => getTea(teaId),
    enabled: Number.isInteger(teaId) && teaId > 0,
  });

  if (!Number.isInteger(teaId) || teaId <= 0) {
    return (
      <section className="panel">
        <p className="feedback feedback--error">Invalid tea id.</p>
      </section>
    );
  }

  if (teaQuery.isPending) {
    return (
      <section className="panel">
        <p className="muted">Loading tea...</p>
      </section>
    );
  }

  if (teaQuery.isError) {
    return (
      <section className="panel stack">
        <p className="feedback feedback--error">
          {(teaQuery.error as Error).message}
        </p>
        <Link to="/teas" className="button button--secondary">
          Back to teas
        </Link>
      </section>
    );
  }

  if (!teaQuery.data) {
    return (
      <section className="panel">
        <p className="feedback feedback--error">Tea not found.</p>
      </section>
    );
  }

  return <TeaEditor key={teaQuery.data.id} teaId={teaId} initialForm={toTeaFormState(teaQuery.data)} name={teaQuery.data.name} teaType={teaQuery.data.tea_type} origin={teaQuery.data.origin} />;
}

type TeaEditorProps = {
  teaId: number;
  initialForm: TeaFormState;
  name: string;
  teaType: string | null;
  origin: string | null;
};

function TeaEditor({
  teaId,
  initialForm,
  name,
  teaType,
  origin,
}: TeaEditorProps) {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [form, setForm] = useState<TeaFormState>(initialForm);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  const updateMutation = useMutation({
    mutationFn: () => updateTea(teaId, toTeaPayload(form)),
    onSuccess: async (updatedTea) => {
      setSaveMessage("Tea updated.");
      setForm(toTeaFormState(updatedTea));
      await queryClient.invalidateQueries({ queryKey: ["teas"] });
      await queryClient.invalidateQueries({ queryKey: ["teas", teaId] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => deleteTea(teaId),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["teas"] });
      navigate("/teas");
    },
  });

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaveMessage(null);
    updateMutation.mutate();
  }

  function handleDelete() {
    setSaveMessage(null);
    deleteMutation.mutate();
  }

  return (
    <section className="panel panel--form">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Edit</p>
          <h2>{name}</h2>
        </div>
        <p className="muted">Review the stored record, update fields, or remove it.</p>
      </div>

      <div className="metadata-row">
        <span className="pill">Tea #{teaId}</span>
        {teaType ? <span className="pill">{teaType}</span> : null}
        {origin ? <span className="pill">{origin}</span> : null}
      </div>

      {saveMessage ? <p className="feedback feedback--success">{saveMessage}</p> : null}

      <TeaForm
        form={form}
        onChange={setForm}
        onSubmit={handleSubmit}
        submitLabel="Save changes"
        isSubmitting={updateMutation.isPending}
        errorMessage={updateMutation.isError ? (updateMutation.error as Error).message : null}
        secondaryAction={
          <>
            <Link to="/teas" className="button button--secondary">
              Back
            </Link>
            <button
              type="button"
              onClick={handleDelete}
              disabled={deleteMutation.isPending}
              className="button button--danger"
            >
              {deleteMutation.isPending ? "Deleting..." : "Delete tea"}
            </button>
          </>
        }
      />

      {deleteMutation.isError ? (
        <p className="feedback feedback--error">
          {(deleteMutation.error as Error).message}
        </p>
      ) : null}
    </section>
  );
}
