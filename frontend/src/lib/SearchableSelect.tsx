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
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLUListElement>(null);

  const selectedLabel = options.find((o) => o.value === value)?.label ?? "";

  const filtered = query
    ? options.filter((o) => o.label.toLowerCase().includes(query.toLowerCase()))
    : options;

  // All selectable items: placeholder (index 0) + filtered options (index 1..N)
  const itemCount = filtered.length + 1;

  // Reset highlight when filter changes
  useEffect(() => {
    setHighlightedIndex(-1);
  }, [query]);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
        setQuery("");
        setHighlightedIndex(-1);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Scroll highlighted item into view
  useEffect(() => {
    if (highlightedIndex < 0 || !listRef.current) return;
    const items = listRef.current.querySelectorAll("li");
    items[highlightedIndex]?.scrollIntoView({ block: "nearest" });
  }, [highlightedIndex]);

  function handleSelect(optionValue: string) {
    onChange(optionValue);
    setOpen(false);
    setQuery("");
    setHighlightedIndex(-1);
  }

  function handleClear() {
    onChange("");
    setQuery("");
    setOpen(false);
    setHighlightedIndex(-1);
  }

  function handleInputFocus() {
    setOpen(true);
    setQuery("");
    setHighlightedIndex(-1);
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Escape") {
      setOpen(false);
      setQuery("");
      setHighlightedIndex(-1);
      inputRef.current?.blur();
      return;
    }

    if (!open) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev + 1) % itemCount);
      return;
    }

    if (e.key === "ArrowUp") {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev <= 0 ? itemCount - 1 : prev - 1));
      return;
    }

    if (e.key === "Enter") {
      e.preventDefault();
      if (highlightedIndex === 0) {
        handleSelect("");
      } else if (highlightedIndex > 0 && highlightedIndex <= filtered.length) {
        handleSelect(filtered[highlightedIndex - 1].value);
      } else if (filtered.length === 1) {
        handleSelect(filtered[0].value);
      }
      return;
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
        role="combobox"
        aria-expanded={open}
        aria-autocomplete="list"
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
        <ul className="searchable-select__dropdown" ref={listRef} role="listbox">
          <li>
            <button
              type="button"
              className={`searchable-select__option${highlightedIndex === 0 ? " searchable-select__option--highlighted" : ""}${value === "" ? " searchable-select__option--active" : ""}`}
              onMouseDown={(e) => e.preventDefault()}
              onClick={() => handleSelect("")}
              onMouseEnter={() => setHighlightedIndex(0)}
            >
              {placeholder}
            </button>
          </li>
          {filtered.map((o, i) => (
            <li key={o.value}>
              <button
                type="button"
                className={`searchable-select__option${highlightedIndex === i + 1 ? " searchable-select__option--highlighted" : ""}${o.value === value ? " searchable-select__option--active" : ""}`}
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => handleSelect(o.value)}
                onMouseEnter={() => setHighlightedIndex(i + 1)}
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
