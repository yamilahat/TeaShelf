import { useState } from "react";
import type { FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, useNavigate, useParams } from "react-router";
import { deleteTeaware, getTeaware, updateTeaware } from "../features/teaware/api";
import { TeawareForm } from "../features/teaware/TeawareForm";
import { teaTypeLabel } from "../features/tea-types/api";
import {
  type TeawareFormState,
  toTeawareFormState,
  toTeawarePayload,
} from "../features/teaware/formState";

export function TeawareDetailPage() {
  const params = useParams();
  const teawareId = Number(params.teawareId);

  const teawareQuery = useQuery({
    queryKey: ["teaware", teawareId],
    queryFn: () => getTeaware(teawareId),
    enabled: Number.isInteger(teawareId) && teawareId > 0,
  });

  if (!Number.isInteger(teawareId) || teawareId <= 0) {
    return (
      <section className="panel">
        <p className="feedback feedback--error">Invalid teaware id.</p>
      </section>
    );
  }

  if (teawareQuery.isPending) {
    return (
      <section className="panel">
        <p className="muted">Loading teaware...</p>
      </section>
    );
  }

  if (teawareQuery.isError) {
    return (
      <section className="panel stack">
        <p className="feedback feedback--error">
          {(teawareQuery.error as Error).message}
        </p>
        <Link to="/teaware" className="button button--secondary">
          Back to teaware
        </Link>
      </section>
    );
  }

  if (!teawareQuery.data) {
    return (
      <section className="panel">
        <p className="feedback feedback--error">Teaware not found.</p>
      </section>
    );
  }

  return (
    <TeawareEditor
      key={teawareQuery.data.id}
      teawareId={teawareId}
      initialForm={toTeawareFormState(teawareQuery.data)}
      name={teawareQuery.data.name}
      type={teawareQuery.data.type}
      material={teawareQuery.data.material}
      preferredTeaTypes={teawareQuery.data.preferred_tea_types}
    />
  );
}

type TeawareEditorProps = {
  teawareId: number;
  initialForm: TeawareFormState;
  name: string;
  type: string | null;
  material: string | null;
  preferredTeaTypes: string[];
};

function TeawareEditor({
  teawareId,
  initialForm,
  name,
  type,
  material,
  preferredTeaTypes,
}: TeawareEditorProps) {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [form, setForm] = useState<TeawareFormState>(initialForm);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  const updateMutation = useMutation({
    mutationFn: () => updateTeaware(teawareId, toTeawarePayload(form)),
    onSuccess: async (updatedTeaware) => {
      setSaveMessage("Teaware updated.");
      setForm(toTeawareFormState(updatedTeaware));
      await queryClient.invalidateQueries({ queryKey: ["teaware"] });
      await queryClient.invalidateQueries({ queryKey: ["teaware", teawareId] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => deleteTeaware(teawareId),
    onSuccess: async () => {
      queryClient.removeQueries({ queryKey: ["teaware", teawareId], exact: true });
      navigate("/teaware", { replace: true });
      await queryClient.invalidateQueries({ queryKey: ["teaware"], exact: true });
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
        <span className="pill">Teaware #{teawareId}</span>
        {type ? <span className="pill">{type}</span> : null}
        {material ? <span className="pill">{material}</span> : null}
        {preferredTeaTypes.map((t) => (
          <span key={t} className="pill">{teaTypeLabel(t)}</span>
        ))}
      </div>

      {saveMessage ? <p className="feedback feedback--success">{saveMessage}</p> : null}

      <TeawareForm
        form={form}
        onChange={setForm}
        onSubmit={handleSubmit}
        submitLabel="Save changes"
        isSubmitting={updateMutation.isPending}
        errorMessage={updateMutation.isError ? (updateMutation.error as Error).message : null}
        secondaryAction={
          <>
            <Link to="/teaware" className="button button--secondary">
              Back
            </Link>
            <button
              type="button"
              onClick={handleDelete}
              disabled={deleteMutation.isPending}
              className="button button--danger"
            >
              {deleteMutation.isPending ? "Deleting..." : "Delete teaware"}
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
