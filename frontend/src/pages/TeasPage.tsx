import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { Link } from "react-router";
import { type TeaFilters, listTeas } from "../features/teas/api";
import { useTeaTypeOptions } from "../features/tea-types/api";
import { SearchableSelect } from "../lib/SearchableSelect";

function StockBar({ current, initial }: { current: number; initial: number }) {
  const pct = Math.max(0, Math.min(100, (current / initial) * 100));
  const rounded = Math.round(pct);

  // Gradient shifts hue: green at 100%, amber at 50%, red at 0%
  const hue = Math.round((pct / 100) * 120); // 0 = red, 60 = amber, 120 = green

  return (
    <div className="stock-bar" role="meter" aria-valuenow={rounded} aria-valuemin={0} aria-valuemax={100} aria-label={`${rounded}% remaining`}>
      <div
        className="stock-bar__fill"
        style={{
          width: `${pct}%`,
          background: `linear-gradient(90deg, hsl(${hue}, 45%, 42%), hsl(${hue}, 50%, 55%))`,
        }}
      />
    </div>
  );
}

function useDebounced<T>(value: T, delay = 300): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);
  }, [value, delay]);
  return debounced;
}

export function TeasPage() {
  const teaTypeOptions = useTeaTypeOptions();
  const [filters, setFilters] = useState<TeaFilters>({});
  const debouncedFilters = useDebounced(filters);

  const { data, isPending, isError, error, refetch, isFetching } = useQuery({
    queryKey: ["teas", debouncedFilters],
    queryFn: () => listTeas(debouncedFilters),
  });

  const hasFilters = !!(filters.name || filters.vendor || filters.tea_type || filters.in_stock);

  function handleFilter(field: keyof TeaFilters, value: string) {
    setFilters((prev) => ({ ...prev, [field]: value || undefined }));
  }

  function clearFilters() {
    setFilters({});
  }

  return (
    <section className="stack">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Inventory</p>
          <h2>Teas</h2>
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
          <Link to="/teas/new" className="button button--primary">
            Add tea
          </Link>
        </div>
      </div>

      <div className="filter-bar">
        <div className="field">
          <label className="field__label">Name</label>
          <input
            className="field__input"
            type="text"
            placeholder="Search teas…"
            value={filters.name ?? ""}
            onChange={(e) => handleFilter("name", e.target.value)}
          />
        </div>
        <div className="field">
          <label className="field__label">Vendor</label>
          <input
            className="field__input"
            type="text"
            placeholder="e.g. Teavivre"
            value={filters.vendor ?? ""}
            onChange={(e) => handleFilter("vendor", e.target.value)}
          />
        </div>
        <div className="field">
          <label className="field__label">Type</label>
          <SearchableSelect
            options={teaTypeOptions}
            value={filters.tea_type ?? ""}
            onChange={(value) => handleFilter("tea_type", value)}
            placeholder="All types"
          />
        </div>
        <div className="filter-bar__actions">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={filters.in_stock === true}
              onChange={(e) =>
                setFilters((prev) => ({
                  ...prev,
                  in_stock: e.target.checked ? true : undefined,
                }))
              }
            />
            In stock only
          </label>
          {hasFilters && (
            <button type="button" className="button button--secondary" onClick={clearFilters}>
              Clear filters
            </button>
          )}
        </div>
      </div>

      {isPending ? <p className="panel muted">Loading teas...</p> : null}

      {isError ? (
        <p className="panel feedback feedback--error">{(error as Error).message}</p>
      ) : null}

      {!isPending && !isError && (!data || data.length === 0) ? (
        <div className="panel stack">
          <p className="muted">
            No teas yet. Start your shelf with a tea you want to remember.
          </p>
          <div>
            <Link to="/teas/new" className="button button--primary">
              Create the first tea
            </Link>
          </div>
        </div>
      ) : null}

      {!isPending && !isError && data?.length ? (
        <div className="tea-grid">
          {data.map((tea) => (
            <article key={tea.id} className="tea-card">
              <div className="stack stack--tight">
                <div className="tea-card__header">
                  <div>
                    <h3>{tea.name}</h3>
                    <p className="muted">{tea.vendor ?? "Unknown vendor"}</p>
                  </div>
                  <div className="metadata-row">
                    {tea.current_quantity_g != null && tea.current_quantity_g > 0 ? (
                      <span className="pill pill--stock">{tea.current_quantity_g} g</span>
                    ) : tea.current_quantity_g != null && tea.current_quantity_g <= 0 ? (
                      <span className="pill pill--out-of-stock">Out of stock</span>
                    ) : null}
                    <span className="pill">#{tea.id}</span>
                  </div>
                </div>

                <dl className="tea-card__meta">
                  <div>
                    <dt>Type</dt>
                    <dd>{tea.tea_type ?? "Not set"}</dd>
                  </div>
                  <div>
                    <dt>Origin</dt>
                    <dd>{tea.origin ?? "Not set"}</dd>
                  </div>
                  <div>
                    <dt>Harvest</dt>
                    <dd>{tea.harvest_year ?? "Not set"}</dd>
                  </div>
                </dl>

                {tea.notes ? <p className="tea-card__notes">{tea.notes}</p> : null}

                {tea.initial_quantity_g != null && tea.initial_quantity_g > 0 && tea.current_quantity_g != null ? (
                  <StockBar current={tea.current_quantity_g} initial={tea.initial_quantity_g} />
                ) : null}
              </div>

              <div className="button-row">
                <Link to={`/teas/${tea.id}`} className="button button--secondary">
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
