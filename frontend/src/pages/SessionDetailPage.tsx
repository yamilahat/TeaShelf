import { useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, useNavigate, useParams } from "react-router";
import { listTeas } from "../features/teas/api";
import { listTeaware } from "../features/teaware/api";
import {
  deleteSession,
  getSession,
  updateSession,
} from "../features/sessions/api";
import { SessionForm } from "../features/sessions/SessionForm";
import {
  type TeaSessionFormState,
  toTeaSessionFormState,
  toTeaSessionPayload,
} from "../features/sessions/formState";

/** Parse DD/MM/YYYY from API into a Date for display */
function parseSessionDate(value: string): Date {
  const [day, month, year] = value.split("/").map(Number);
  return new Date(year, month - 1, day);
}

export function SessionDetailPage() {
  const params = useParams();
  const sessionId = Number(params.sessionId);

  const sessionQuery = useQuery({
    queryKey: ["sessions", sessionId],
    queryFn: () => getSession(sessionId),
    enabled: Number.isInteger(sessionId) && sessionId > 0,
  });

  const teasQuery = useQuery({
    queryKey: ["teas"],
    queryFn: listTeas,
    enabled: Number.isInteger(sessionId) && sessionId > 0,
  });

  const teawareQuery = useQuery({
    queryKey: ["teaware"],
    queryFn: listTeaware,
    enabled: Number.isInteger(sessionId) && sessionId > 0,
  });

  if (!Number.isInteger(sessionId) || sessionId <= 0) {
    return (
      <section className="panel">
        <p className="feedback feedback--error">Invalid session id.</p>
      </section>
    );
  }

  if (sessionQuery.isPending || teasQuery.isPending || teawareQuery.isPending) {
    return (
      <section className="panel">
        <p className="muted">Loading session...</p>
      </section>
    );
  }

  if (sessionQuery.isError || teasQuery.isError) {
    return (
      <section className="panel stack">
        <p className="feedback feedback--error">
          {sessionQuery.isError
            ? (sessionQuery.error as Error).message
            : (teasQuery.error as Error).message}
        </p>
        <Link to="/sessions" className="button button--secondary">
          Back to sessions
        </Link>
      </section>
    );
  }

  if (!sessionQuery.data) {
    return (
      <section className="panel">
        <p className="feedback feedback--error">Tea session not found.</p>
      </section>
    );
  }

  return (
    <SessionEditor
      key={sessionQuery.data.id}
      sessionId={sessionId}
      initialForm={toTeaSessionFormState(sessionQuery.data)}
      teas={teasQuery.data ?? []}
      teaware={teawareQuery.data ?? []}
      teaId={sessionQuery.data.tea_id}
      sessionDate={sessionQuery.data.session_date}
    />
  );
}

type SessionEditorProps = {
  sessionId: number;
  initialForm: TeaSessionFormState;
  teaId: number;
  sessionDate: string;
  teas: Awaited<ReturnType<typeof listTeas>>;
  teaware: Awaited<ReturnType<typeof listTeaware>>;
};

function SessionEditor({ sessionId, initialForm, teaId, sessionDate, teas, teaware }: SessionEditorProps) {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [form, setForm] = useState<TeaSessionFormState>(initialForm);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  const selectedTeaName = useMemo(
    () => teas.find((tea) => tea.id === Number(form.tea_id))?.name,
    [form.tea_id, teas],
  );

  const updateMutation = useMutation({
    mutationFn: () => updateSession(sessionId, toTeaSessionPayload(form)),
    onSuccess: async (updatedSession) => {
      setSaveMessage(`Session #${updatedSession.id} updated.`);
      setForm(toTeaSessionFormState(updatedSession));
      await queryClient.invalidateQueries({ queryKey: ["sessions"] });
      await queryClient.invalidateQueries({ queryKey: ["sessions", sessionId] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => deleteSession(sessionId),
    onSuccess: async () => {
      queryClient.removeQueries({ queryKey: ["sessions", sessionId], exact: true });
      navigate("/sessions", { replace: true });
      await queryClient.invalidateQueries({ queryKey: ["sessions"], exact: true });
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

  const formattedDate = new Intl.DateTimeFormat(undefined, { dateStyle: "medium" }).format(
    parseSessionDate(sessionDate),
  );

  return (
    <section className="panel panel--form stack">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Edit</p>
          <h2>{selectedTeaName ?? `Session #${sessionId}`}</h2>
        </div>
        <p className="muted">Review the stored session, update it, or remove it.</p>
      </div>

      <div className="metadata-row">
        <span className="pill">Session #{sessionId}</span>
        <Link to={`/teas/${teaId}`} className="pill pill--link">
          Tea #{teaId}
        </Link>
        <span className="pill">{formattedDate}</span>
      </div>

      {saveMessage ? <p className="feedback feedback--success">{saveMessage}</p> : null}

      <SessionForm
        form={form}
        teas={teas}
        teaware={teaware}
        onChange={setForm}
        onSubmit={handleSubmit}
        submitLabel="Save changes"
        isSubmitting={updateMutation.isPending}
        errorMessage={updateMutation.isError ? (updateMutation.error as Error).message : null}
        secondaryAction={
          <>
            <Link to="/sessions" className="button button--secondary">
              Back
            </Link>
            <button
              type="button"
              onClick={handleDelete}
              disabled={deleteMutation.isPending}
              className="button button--danger"
            >
              {deleteMutation.isPending ? "Deleting..." : "Delete session"}
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
