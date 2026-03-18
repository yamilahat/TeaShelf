import { useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router";
import { listTeas } from "../features/teas/api";
import {
  createSession,
  listSessions,
  type TeaSession,
} from "../features/sessions/api";
import { SessionForm } from "../features/sessions/SessionForm";
import {
  initialTeaSessionFormState,
  type TeaSessionFormState,
  toTeaSessionPayload,
} from "../features/sessions/formState";

function formatSessionDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export function SessionsPage() {
  const queryClient = useQueryClient();
  const [form, setForm] = useState<TeaSessionFormState>(initialTeaSessionFormState);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  const teasQuery = useQuery({
    queryKey: ["teas"],
    queryFn: listTeas,
  });

  const sessionsQuery = useQuery({
    queryKey: ["sessions"],
    queryFn: listSessions,
  });

  const createMutation = useMutation({
    mutationFn: createSession,
    onSuccess: async (createdSession) => {
      setForm(initialTeaSessionFormState);
      setSaveMessage(`Session #${createdSession.id} created.`);
      await queryClient.invalidateQueries({ queryKey: ["sessions"] });
    },
  });

  const teaNameById = useMemo(() => {
    const teas = teasQuery.data ?? [];
    return new Map(teas.map((tea) => [tea.id, tea.name]));
  }, [teasQuery.data]);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaveMessage(null);
    createMutation.mutate(toTeaSessionPayload(form));
  }

  const isLoading = teasQuery.isPending || sessionsQuery.isPending;
  const isError = teasQuery.isError || sessionsQuery.isError;
  const errorMessage = teasQuery.isError
    ? (teasQuery.error as Error).message
    : sessionsQuery.isError
      ? (sessionsQuery.error as Error).message
      : null;

  return (
    <section className="stack">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Sessions</p>
          <h2>Tasting sessions</h2>
        </div>
        <div className="button-row">
          <button
            type="button"
            onClick={() => {
              void teasQuery.refetch();
              void sessionsQuery.refetch();
            }}
            disabled={teasQuery.isFetching || sessionsQuery.isFetching}
            className="button button--secondary"
          >
            {teasQuery.isFetching || sessionsQuery.isFetching ? "Refreshing..." : "Refresh"}
          </button>
        </div>
      </div>

      <section className="panel panel--form stack">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Create</p>
            <h3>Log a session</h3>
          </div>
          <p className="muted">Use a real tea record and save brewing notes directly to the backend.</p>
        </div>

        {teasQuery.isSuccess && teasQuery.data.length === 0 ? (
          <div className="stack">
            <p className="muted">Create a tea before logging sessions.</p>
            <div>
              <Link to="/teas/new" className="button button--primary">
                Add tea first
              </Link>
            </div>
          </div>
        ) : (
          <>
            {saveMessage ? <p className="feedback feedback--success">{saveMessage}</p> : null}
            <SessionForm
              form={form}
              teas={teasQuery.data ?? []}
              onChange={setForm}
              onSubmit={handleSubmit}
              submitLabel="Create session"
              isSubmitting={createMutation.isPending}
              errorMessage={createMutation.isError ? (createMutation.error as Error).message : null}
              secondaryAction={
                <button
                  type="button"
                  className="button button--secondary"
                  onClick={() => {
                    setSaveMessage(null);
                    setForm(initialTeaSessionFormState);
                  }}
                >
                  Clear
                </button>
              }
            />
          </>
        )}
      </section>

      {isLoading ? <p className="panel muted">Loading sessions...</p> : null}
      {isError && errorMessage ? <p className="panel feedback feedback--error">{errorMessage}</p> : null}

      {!isLoading && !isError && sessionsQuery.data?.length === 0 ? (
        <div className="panel stack">
          <p className="muted">No sessions yet. Log one to verify the new session endpoints.</p>
        </div>
      ) : null}

      {!isLoading && !isError && sessionsQuery.data && sessionsQuery.data.length > 0 ? (
        <div className="tea-grid">
          {sessionsQuery.data.map((session) => (
            <SessionCard
              key={session.id}
              session={session}
              teaName={teaNameById.get(session.tea_id) ?? `Tea #${session.tea_id}`}
            />
          ))}
        </div>
      ) : null}
    </section>
  );
}

function SessionCard({
  session,
  teaName,
}: {
  session: TeaSession;
  teaName: string;
}) {
  return (
    <article className="tea-card">
      <div className="stack stack--tight">
        <div className="tea-card__header">
          <div>
            <h3>{teaName}</h3>
            <p className="muted">{formatSessionDate(session.session_date)}</p>
          </div>
          <span className="pill">Session #{session.id}</span>
        </div>

        <dl className="tea-card__meta tea-card__meta--two-up">
          <div>
            <dt>Tea</dt>
            <dd>
              <Link to={`/teas/${session.tea_id}`} className="inline-link">
                #{session.tea_id}
              </Link>
            </dd>
          </div>
          <div>
            <dt>Rating</dt>
            <dd>{session.rating ?? "Not set"}</dd>
          </div>
          <div>
            <dt>Steeps</dt>
            <dd>{session.steeps_count ?? "Not set"}</dd>
          </div>
        </dl>

        {session.notes ? <p className="tea-card__notes">{session.notes}</p> : null}
      </div>

      <div className="button-row">
        <Link to={`/sessions/${session.id}`} className="button button--secondary">
          View and edit
        </Link>
      </div>
    </article>
  );
}
