import { useQuery } from "@tanstack/react-query";
import { listTeas } from "../features/teas/api";

export function TeasPage() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ["teas"],
    queryFn: listTeas,
  });

  if (isPending) {
    return <p>Loading teas...</p>;
  }

  if (isError) {
    return <p className="text-red-600">{(error as Error).message}</p>;
  }

  if (!data || data.length === 0) {
    return <p>No teas yet.</p>;
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Teas</h2>

      <div className="grid gap-4">
        {data.map((tea) => (
          <article key={tea.id} className="rounded-xl border p-4">
            <h3 className="text-lg font-medium">{tea.name}</h3>
            <p className="text-sm text-slate-600">
              {tea.vendor ?? "Unknown vendor"} · {tea.tea_type ?? "Unknown type"}
            </p>
            <p className="text-sm text-slate-500">
              {tea.origin ?? "Unknown origin"}
            </p>
          </article>
        ))}
      </div>
    </div>
  );
}