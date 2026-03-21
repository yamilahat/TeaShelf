/** Returns today's date as YYYY-MM-DD — the format used by <input type="date">. */
export function todayISO(): string {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const dd = String(now.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

/**
 * Converts a DD/MM/YYYY string (as returned by the API) to YYYY-MM-DD
 * so it can be used as the value of an <input type="date">.
 */
export function ddmmyyyyToISO(ddmmyyyy: string): string {
  const [dd, mm, yyyy] = ddmmyyyy.split("/");
  return `${yyyy}-${mm}-${dd}`;
}
