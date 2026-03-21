import { useEffect, useRef, useState } from "react";

type Option = { value: string; label: string };

type SearchableSelectProps = {
  options: readonly Option[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
};

export function SearchableSelect({
  options,
  value,
  onChange,
  placeholder = "Select…",
}: SearchableSelectProps) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const selectedLabel = options.find((o) => o.value === value)?.label ?? "";

  const filtered = query
    ? options.filter((o) => o.label.toLowerCase().includes(query.toLowerCase()))
    : options;

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
        setQuery("");
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  function handleSelect(optionValue: string) {
    onChange(optionValue);
    setOpen(false);
    setQuery("");
  }

  function handleClear() {
    onChange("");
    setQuery("");
    setOpen(false);
  }

  function handleInputFocus() {
    setOpen(true);
    setQuery("");
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Escape") {
      setOpen(false);
      setQuery("");
      inputRef.current?.blur();
    }
    if (e.key === "Enter" && filtered.length === 1) {
      e.preventDefault();
      handleSelect(filtered[0].value);
    }
  }

  return (
    <div className="searchable-select" ref={containerRef}>
      <input
        ref={inputRef}
        className="field__input"
        placeholder={placeholder}
        value={open ? query : selectedLabel}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={handleInputFocus}
        onKeyDown={handleKeyDown}
      />
      {value && !open && (
        <button
          type="button"
          className="searchable-select__clear"
          onClick={handleClear}
          aria-label="Clear selection"
        >
          ×
        </button>
      )}
      {open && (
        <ul className="searchable-select__dropdown">
          <li>
            <button
              type="button"
              className={`searchable-select__option${value === "" ? " searchable-select__option--active" : ""}`}
              onMouseDown={(e) => e.preventDefault()}
              onClick={() => handleSelect("")}
            >
              {placeholder}
            </button>
          </li>
          {filtered.map((o) => (
            <li key={o.value}>
              <button
                type="button"
                className={`searchable-select__option${o.value === value ? " searchable-select__option--active" : ""}`}
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => handleSelect(o.value)}
              >
                {o.label}
              </button>
            </li>
          ))}
          {filtered.length === 0 && (
            <li className="searchable-select__empty">No matches</li>
          )}
        </ul>
      )}
    </div>
  );
}
