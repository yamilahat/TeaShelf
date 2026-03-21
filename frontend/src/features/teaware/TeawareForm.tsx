import type { FormEvent, ReactNode } from "react";
import { useTeaTypeOptions } from "../tea-types/api";
import type { TeawareFormState } from "./formState";

type TeawareFormProps = {
  form: TeawareFormState;
  onChange: (nextForm: TeawareFormState) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  submitLabel: string;
  isSubmitting?: boolean;
  errorMessage?: string | null;
  secondaryAction?: ReactNode;
};

export function TeawareForm({
  form,
  onChange,
  onSubmit,
  submitLabel,
  isSubmitting = false,
  errorMessage,
  secondaryAction,
}: TeawareFormProps) {
  const teaTypeOptions = useTeaTypeOptions();

  function updateField<K extends keyof TeawareFormState>(
    field: K,
    value: TeawareFormState[K],
  ) {
    onChange({ ...form, [field]: value });
  }

  function toggleTeaType(value: string) {
    const next = form.preferred_tea_types.includes(value)
      ? form.preferred_tea_types.filter((t) => t !== value)
      : [...form.preferred_tea_types, value];
    updateField("preferred_tea_types", next);
  }

  return (
    <form onSubmit={onSubmit} className="stack">
      <div className="field-grid">
        <label className="field">
          <span className="field__label">Name</span>
          <input
            className="field__input"
            placeholder="My favourite gaiwan"
            value={form.name}
            onChange={(event) => updateField("name", event.target.value)}
            required
          />
        </label>

        <label className="field">
          <span className="field__label">Nickname</span>
          <input
            className="field__input"
            placeholder="Optional friendly name"
            value={form.nickname}
            onChange={(event) => updateField("nickname", event.target.value)}
          />
        </label>
      </div>

      <div className="field-grid">
        <label className="field">
          <span className="field__label">Type</span>
          <input
            className="field__input"
            placeholder="Gaiwan, teapot, cup..."
            value={form.type}
            onChange={(event) => updateField("type", event.target.value)}
          />
        </label>

        <label className="field">
          <span className="field__label">Material</span>
          <input
            className="field__input"
            placeholder="Porcelain, clay, glass..."
            value={form.material}
            onChange={(event) => updateField("material", event.target.value)}
          />
        </label>
      </div>

      <div className="field-grid">
        <label className="field">
          <span className="field__label">Volume (ml)</span>
          <input
            className="field__input"
            type="number"
            min="0"
            inputMode="numeric"
            placeholder="150"
            value={form.volume_ml}
            onChange={(event) => updateField("volume_ml", event.target.value)}
          />
        </label>

        <label className="field">
          <span className="field__label">Vendor</span>
          <input
            className="field__input"
            placeholder="Where you got it"
            value={form.vendor}
            onChange={(event) => updateField("vendor", event.target.value)}
          />
        </label>
      </div>

      <label className="field">
        <span className="field__label">Acquired date</span>
        <input
          className="field__input"
          type="date"
          value={form.acquired_date}
          onChange={(event) => updateField("acquired_date", event.target.value)}
        />
      </label>

      <fieldset className="field">
        <legend className="field__label">Preferred tea types</legend>
        <div className="checkbox-group">
          {teaTypeOptions.map((tt) => (
            <label key={tt.value} className="checkbox-label">
              <input
                type="checkbox"
                checked={form.preferred_tea_types.includes(tt.value)}
                onChange={() => toggleTeaType(tt.value)}
              />
              {tt.label}
            </label>
          ))}
        </div>
      </fieldset>

      <label className="field">
        <span className="field__label">Notes</span>
        <textarea
          className="field__input field__input--textarea"
          placeholder="Anything worth remembering about this piece"
          value={form.notes}
          onChange={(event) => updateField("notes", event.target.value)}
        />
      </label>

      {errorMessage ? <p className="feedback feedback--error">{errorMessage}</p> : null}

      <div className="button-row">
        <button
          type="submit"
          disabled={isSubmitting}
          className="button button--primary"
        >
          {isSubmitting ? "Saving..." : submitLabel}
        </button>
        {secondaryAction}
      </div>
    </form>
  );
}
