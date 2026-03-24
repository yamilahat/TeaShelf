import { useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, useNavigate, useParams } from "react-router";
import { deleteTea, getTea, updateTea, updateTeaQuantity } from "../features/teas/api";
import { listSessions } from "../features/sessions/api";
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

  return <TeaEditor key={teaQuery.data.id} teaId={teaId} initialForm={toTeaFormState(teaQuery.data)} name={teaQuery.data.name} teaType={teaQuery.data.tea_type} origin={teaQuery.data.origin} initialQuantityG={teaQuery.data.initial_quantity_g} currentQuantityG={teaQuery.data.current_quantity_g} />;
}

type TeaEditorProps = {
  teaId: number;
  initialForm: TeaFormState;
  name: string;
  teaType: string | null;
  origin: string | null;
  initialQuantityG: number | null;
  currentQuantityG: number | null;
};

function TeaEditor({
  teaId,
  initialForm,
  name,
  teaType,
  origin,
  initialQuantityG,
  currentQuantityG,
}: TeaEditorProps) {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [form, setForm] = useState<TeaFormState>(initialForm);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);
  const [quantityInput, setQuantityInput] = useState(currentQuantityG?.toString() ?? "");
  const [quantityMessage, setQuantityMessage] = useState<string | null>(null);

  const sessionsQuery = useQuery({
    queryKey: ["sessions"],
    queryFn: listSessions,
  });

  const relatedSessions = useMemo(
    () => (sessionsQuery.data ?? []).filter((session) => session.tea_id === teaId),
    [sessionsQuery.data, teaId],
  );

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
      queryClient.removeQueries({ queryKey: ["teas", teaId], exact: true });
      navigate("/teas", { replace: true });
      await queryClient.invalidateQueries({ queryKey: ["teas"], exact: true });
    },
  });

  const quantityMutation = useMutation({
    mutationFn: (qty: number) => updateTeaQuantity(teaId, qty),
    onSuccess: async () => {
      setQuantityMessage("Quantity updated.");
      await queryClient.invalidateQueries({ queryKey: ["teas"] });
      await queryClient.invalidateQueries({ queryKey: ["teas", teaId] });
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
        {initialQuantityG != null || currentQuantityG != null ? (
          <span className="pill pill--stock">
            {initialQuantityG != null ? `Initial: ${initialQuantityG} g` : null}
            {initialQuantityG != null && currentQuantityG != null ? " / " : null}
            {currentQuantityG != null ? `Remaining: ${currentQuantityG} g` : null}
          </span>
        ) : null}
      </div>

      {(initialQuantityG != null || currentQuantityG != null) && (
        <div className="quantity-update">
          <label className="field">
            <span className="field__label">Update quantity (g)</span>
            <input
              className="field__input"
              type="number"
              inputMode="decimal"
              min="0"
              step="any"
              value={quantityInput}
              onChange={(e) => {
                setQuantityInput(e.target.value);
                setQuantityMessage(null);
              }}
            />
          </label>
          <button
            type="button"
            className="button button--secondary"
            disabled={quantityMutation.isPending || quantityInput === ""}
            onClick={() => {
              setQuantityMessage(null);
              quantityMutation.mutate(Number(quantityInput));
            }}
          >
            {quantityMutation.isPending ? "Saving..." : "Save"}
          </button>
        </div>
      )}

      {quantityMessage ? <p className="feedback feedback--success">{quantityMessage}</p> : null}
      {quantityMutation.isError ? (
        <p className="feedback feedback--error">{(quantityMutation.error as Error).message}</p>
      ) : null}

      {saveMessage ? <p className="feedback feedback--success">{saveMessage}</p> : null}

      <div className="panel panel--nested stack">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Sessions</p>
            <h3>Linked sessions</h3>
          </div>
          <Link to="/sessions" className="button button--secondary">
            Open sessions
          </Link>
        </div>

        {sessionsQuery.isPending ? <p className="muted">Loading linked sessions...</p> : null}
        {sessionsQuery.isError ? (
          <p className="feedback feedback--error">{(sessionsQuery.error as Error).message}</p>
        ) : null}
        {!sessionsQuery.isPending && !sessionsQuery.isError && relatedSessions.length === 0 ? (
          <p className="muted">No sessions are linked to this tea yet.</p>
        ) : null}
        {!sessionsQuery.isPending && !sessionsQuery.isError && relatedSessions.length > 0 ? (
          <div className="linked-list">
            {relatedSessions.map((session) => (
              <Link key={session.id} to={`/sessions/${session.id}`} className="linked-list__item">
                <strong>Session #{session.id}</strong>
                <span>
                  {new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(new Date(session.session_date))}
                </span>
              </Link>
            ))}
          </div>
        ) : null}
      </div>

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
