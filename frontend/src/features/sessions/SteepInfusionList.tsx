import type { SteepInfusionFormRow } from "./formState";

type SteepInfusionListProps = {
  infusions: SteepInfusionFormRow[];
  onChange: (infusions: SteepInfusionFormRow[]) => void;
};

export function SteepInfusionList({ infusions, onChange }: SteepInfusionListProps) {
  function addRow() {
    onChange([
      ...infusions,
      { steep_number: String(infusions.length + 1), steep_time_seconds: "" },
    ]);
  }

  function removeRow(index: number) {
    const next = infusions
      .filter((_, i) => i !== index)
      .map((row, i) => ({ ...row, steep_number: String(i + 1) }));
    onChange(next);
  }

  function updateRow(index: number, value: string) {
    const next = infusions.map((row, i) =>
      i === index ? { ...row, steep_time_seconds: value } : row,
    );
    onChange(next);
  }

  return (
    <div className="stack stack--tight">
      <span className="field__label">Steep infusions</span>
      {infusions.length > 0 ? (
        <div className="linked-list">
          {infusions.map((row, index) => (
            <div key={index} className="linked-list__item">
              <span>Steep {row.steep_number}</span>
              <input
                className="field__input"
                type="number"
                min="1"
                inputMode="numeric"
                placeholder="seconds"
                value={row.steep_time_seconds}
                onChange={(e) => updateRow(index, e.target.value)}
                style={{ maxWidth: "8rem" }}
              />
              <button
                type="button"
                className="button button--secondary"
                onClick={() => removeRow(index)}
              >
                Remove
              </button>
            </div>
          ))}
        </div>
      ) : (
        <p className="muted">No steep infusions added.</p>
      )}
      <div>
        <button type="button" className="button button--secondary" onClick={addRow}>
          Add steep
        </button>
      </div>
    </div>
  );
}
