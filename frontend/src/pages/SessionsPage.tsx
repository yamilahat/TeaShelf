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
import { listTeaware } from "../features/teaware/api";
import { SessionForm } from "../features/sessions/SessionForm";
import {
  initialTeaSessionFormState,
  type TeaSessionFormState,
  toTeaSessionPayload,
} from "../features/sessions/formState";

/** Parse DD/MM/YYYY from API into a Date for display */
function parseSessionDate(value: string): Date {
  const [day, month, year] = value.split("/").map(Number);
  return new Date(year, month - 1, day);
}

function formatSessionDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, { dateStyle: "medium" }).format(
    parseSessionDate(value),
  );
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

  const teawareQuery = useQuery({
    queryKey: ["teaware"],
    queryFn: listTeaware,
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

  const teawareNameById = useMemo(() => {
    const items = teawareQuery.data ?? [];
    return new Map(items.map((t) => [t.id, t.nickname ?? t.name]));
  }, [teawareQuery.data]);

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
              void teawareQuery.refetch();
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
              teaware={teawareQuery.data ?? []}
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
          <p className="muted">No sessions yet. Log one above.</p>
        </div>
      ) : null}

      {!isLoading && !isError && sessionsQuery.data && sessionsQuery.data.length > 0 ? (
        <div className="tea-grid">
          {sessionsQuery.data.map((session) => (
            <SessionCard
              key={session.id}
              session={session}
              teaName={teaNameById.get(session.tea_id) ?? `Tea #${session.tea_id}`}
              teawareName={session.teaware_id ? teawareNameById.get(session.teaware_id) : undefined}
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
  teawareName,
}: {
  session: TeaSession;
  teaName: string;
  teawareName?: string;
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
                {teaName}
              </Link>
            </dd>
          </div>
          {teawareName ? (
            <div>
              <dt>Teaware</dt>
              <dd>{teawareName}</dd>
            </div>
          ) : null}
          <div>
            <dt>Rating</dt>
            <dd>{session.rating ?? "Not set"}</dd>
          </div>
          <div>
            <dt>Steeps</dt>
            <dd>
              {session.steep_infusions.length > 0
                ? session.steep_infusions.length
                : session.steeps_count ?? "Not set"}
            </dd>
          </div>
          {session.water_temp_c != null ? (
            <div>
              <dt>Water temp</dt>
              <dd>{session.water_temp_c}&deg;C</dd>
            </div>
          ) : null}
          {session.leaf_weight_g != null ? (
            <div>
              <dt>Leaf weight</dt>
              <dd>{session.leaf_weight_g}g</dd>
            </div>
          ) : null}
          {session.water_volume_ml != null ? (
            <div>
              <dt>Water vol</dt>
              <dd>{session.water_volume_ml}ml</dd>
            </div>
          ) : null}
          {session.brew_method ? (
            <div>
              <dt>Brew method</dt>
              <dd>{session.brew_method}</dd>
            </div>
          ) : null}
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
