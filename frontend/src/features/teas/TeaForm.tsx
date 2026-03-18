import type { FormEvent, ReactNode } from "react";
import type { TeaFormState } from "./formState";

type TeaFormProps = {
  form: TeaFormState;
  onChange: (nextForm: TeaFormState) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  submitLabel: string;
  isSubmitting?: boolean;
  errorMessage?: string | null;
  secondaryAction?: ReactNode;
};

export function TeaForm({
  form,
  onChange,
  onSubmit,
  submitLabel,
  isSubmitting = false,
  errorMessage,
  secondaryAction,
}: TeaFormProps) {
  function updateField<K extends keyof TeaFormState>(
    field: K,
    value: TeaFormState[K],
  ) {
    onChange({ ...form, [field]: value });
  }

  return (
    <form onSubmit={onSubmit} className="stack">
      <label className="field">
        <span className="field__label">Name</span>
        <input
          className="field__input"
          placeholder="Da Hong Pao"
          value={form.name}
          onChange={(event) => updateField("name", event.target.value)}
          required
        />
      </label>

      <div className="field-grid">
        <label className="field">
          <span className="field__label">Vendor</span>
          <input
            className="field__input"
            placeholder="Tea house or shop"
            value={form.vendor}
            onChange={(event) => updateField("vendor", event.target.value)}
          />
        </label>

        <label className="field">
          <span className="field__label">Origin</span>
          <input
            className="field__input"
            placeholder="Region or country"
            value={form.origin}
            onChange={(event) => updateField("origin", event.target.value)}
          />
        </label>
      </div>

      <div className="field-grid">
        <label className="field">
          <span className="field__label">Tea type</span>
          <input
            className="field__input"
            placeholder="green, oolong, white..."
            value={form.tea_type}
            onChange={(event) => updateField("tea_type", event.target.value)}
          />
        </label>

        <label className="field">
          <span className="field__label">Harvest year</span>
          <input
            className="field__input"
            placeholder="2024"
            type="number"
            inputMode="numeric"
            min="1900"
            max="2100"
            value={form.harvest_year}
            onChange={(event) => updateField("harvest_year", event.target.value)}
          />
        </label>
      </div>

      <label className="field">
        <span className="field__label">Notes</span>
        <textarea
          className="field__input field__input--textarea"
          placeholder="Anything worth remembering about this tea"
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
