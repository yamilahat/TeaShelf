import type { FormEvent, ReactNode } from "react";
import type { Tea } from "../teas/api";
import type { Teaware } from "../teaware/api";
import type { TeaSessionFormState } from "./formState";
import { SteepInfusionList } from "./SteepInfusionList";

type SessionFormProps = {
  form: TeaSessionFormState;
  teas: Tea[];
  teaware: Teaware[];
  onChange: (nextForm: TeaSessionFormState) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  submitLabel: string;
  isSubmitting?: boolean;
  errorMessage?: string | null;
  secondaryAction?: ReactNode;
};

export function SessionForm({
  form,
  teas,
  teaware,
  onChange,
  onSubmit,
  submitLabel,
  isSubmitting = false,
  errorMessage,
  secondaryAction,
}: SessionFormProps) {
  function updateField<K extends keyof TeaSessionFormState>(
    field: K,
    value: TeaSessionFormState[K],
  ) {
    onChange({ ...form, [field]: value });
  }

  return (
    <form onSubmit={onSubmit} className="stack">
      <div className="field-grid">
        <label className="field">
          <span className="field__label">Tea</span>
          <select
            className="field__input"
            value={form.tea_id}
            onChange={(event) => updateField("tea_id", event.target.value)}
            required
          >
            <option value="">Select a tea</option>
            {teas.map((tea) => (
              <option key={tea.id} value={tea.id}>
                {tea.name}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span className="field__label">Session date</span>
          <input
            className="field__input"
            type="date"
            value={form.session_date}
            onChange={(event) => updateField("session_date", event.target.value)}
            required
          />
        </label>
      </div>

      <div className="field-grid">
        <label className="field">
          <span className="field__label">Teaware</span>
          <select
            className="field__input"
            value={form.teaware_id}
            onChange={(event) => updateField("teaware_id", event.target.value)}
          >
            <option value="">None</option>
            {teaware.map((item) => (
              <option key={item.id} value={item.id}>
                {item.nickname ?? item.name}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span className="field__label">Steeps</span>
          <input
            className="field__input"
            type="number"
            min="0"
            inputMode="numeric"
            placeholder="3"
            value={form.steeps_count}
            onChange={(event) => updateField("steeps_count", event.target.value)}
          />
        </label>
      </div>

      <div className="field-grid">
        <label className="field">
          <span className="field__label">Rating</span>
          <input
            className="field__input"
            type="number"
            min="0"
            max="100"
            inputMode="numeric"
            placeholder="85"
            value={form.rating}
            onChange={(event) => updateField("rating", event.target.value)}
          />
        </label>
      </div>

      <div className="field-grid">
        <label className="field">
          <span className="field__label">Water temp (&deg;C)</span>
          <input
            className="field__input"
            type="number"
            min="0"
            max="100"
            step="any"
            inputMode="decimal"
            placeholder="95"
            value={form.water_temp_c}
            onChange={(event) => updateField("water_temp_c", event.target.value)}
          />
        </label>

        <label className="field">
          <span className="field__label">Leaf weight (g)</span>
          <input
            className="field__input"
            type="number"
            min="0"
            step="any"
            inputMode="decimal"
            placeholder="5"
            value={form.leaf_weight_g}
            onChange={(event) => updateField("leaf_weight_g", event.target.value)}
          />
        </label>
      </div>

      <div className="field-grid">
        <label className="field">
          <span className="field__label">Water volume (ml)</span>
          <input
            className="field__input"
            type="number"
            min="0"
            step="any"
            inputMode="decimal"
            placeholder="150"
            value={form.water_volume_ml}
            onChange={(event) => updateField("water_volume_ml", event.target.value)}
          />
        </label>

        <label className="field">
          <span className="field__label">Brew method</span>
          <input
            className="field__input"
            type="text"
            maxLength={60}
            placeholder="Gongfu, Western, etc."
            value={form.brew_method}
            onChange={(event) => updateField("brew_method", event.target.value)}
          />
        </label>
      </div>

      <SteepInfusionList
        infusions={form.steep_infusions}
        onChange={(infusions) => onChange({ ...form, steep_infusions: infusions })}
      />

      <label className="field">
        <span className="field__label">Notes</span>
        <textarea
          className="field__input field__input--textarea"
          placeholder="Brewing notes, aromas, or quick impressions"
          value={form.notes}
          onChange={(event) => updateField("notes", event.target.value)}
        />
      </label>

      {errorMessage ? <p className="feedback feedback--error">{errorMessage}</p> : null}

      <div className="button-row">
        <button
          type="submit"
          disabled={isSubmitting || teas.length === 0}
          className="button button--primary"
        >
          {isSubmitting ? "Saving..." : submitLabel}
        </button>
        {secondaryAction}
      </div>
    </form>
  );
}
