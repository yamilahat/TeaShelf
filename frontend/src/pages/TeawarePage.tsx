import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router";
import { listTeaware } from "../features/teaware/api";
import { TEA_TYPES } from "../lib/teaTypes";

function teaTypeLabel(value: string) {
  return TEA_TYPES.find((t) => t.value === value)?.label ?? value;
}

export function TeawarePage() {
  const { data, isPending, isError, error, refetch, isFetching } = useQuery({
    queryKey: ["teaware"],
    queryFn: listTeaware,
  });

  return (
    <section className="stack">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Collection</p>
          <h2>Teaware</h2>
        </div>
        <div className="button-row">
          <button
            type="button"
            onClick={() => void refetch()}
            disabled={isFetching}
            className="button button--secondary"
          >
            {isFetching ? "Refreshing..." : "Refresh"}
          </button>
          <Link to="/teaware/new" className="button button--primary">
            Add teaware
          </Link>
        </div>
      </div>

      {isPending ? <p className="panel muted">Loading teaware...</p> : null}

      {isError ? (
        <p className="panel feedback feedback--error">{(error as Error).message}</p>
      ) : null}

      {!isPending && !isError && (!data || data.length === 0) ? (
        <div className="panel stack">
          <p className="muted">
            No teaware yet. Add your first piece of brewing equipment.
          </p>
          <div>
            <Link to="/teaware/new" className="button button--primary">
              Add first teaware
            </Link>
          </div>
        </div>
      ) : null}

      {!isPending && !isError && data?.length ? (
        <div className="tea-grid">
          {data.map((tw) => (
            <article key={tw.id} className="tea-card">
              <div className="stack stack--tight">
                <div className="tea-card__header">
                  <div>
                    <h3>{tw.name}</h3>
                    <p className="muted">{tw.nickname ?? tw.type ?? "Teaware"}</p>
                  </div>
                  <span className="pill">#{tw.id}</span>
                </div>

                <dl className="tea-card__meta">
                  <div>
                    <dt>Type</dt>
                    <dd>{tw.type ?? "Not set"}</dd>
                  </div>
                  <div>
                    <dt>Material</dt>
                    <dd>{tw.material ?? "Not set"}</dd>
                  </div>
                  <div>
                    <dt>Volume</dt>
                    <dd>{tw.volume_ml ? `${tw.volume_ml} ml` : "Not set"}</dd>
                  </div>
                </dl>

                {tw.preferred_tea_types.length > 0 ? (
                  <div className="metadata-row">
                    {tw.preferred_tea_types.map((t) => (
                      <span key={t} className="pill">
                        {teaTypeLabel(t)}
                      </span>
                    ))}
                  </div>
                ) : null}

                {tw.notes ? <p className="tea-card__notes">{tw.notes}</p> : null}
              </div>

              <div className="button-row">
                <Link to={`/teaware/${tw.id}`} className="button button--secondary">
                  View and edit
                </Link>
              </div>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  );
}
