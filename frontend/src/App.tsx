import { NavLink, Navigate, Route, Routes } from "react-router";
import { TeasPage } from "./pages/TeasPage";
import { NewTeaPage } from "./pages/NewTeaPage";

export default function App() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      <header className="border-b">
        <div className="mx-auto flex max-w-5xl items-center gap-6 p-4">
          <h1 className="text-xl font-semibold">TeaShelf</h1>

          <nav className="flex gap-4 text-sm">
            <NavLink to="/teas" className="hover:underline">
              Teas
            </NavLink>
            <NavLink to="/teas/new" className="hover:underline">
              New tea
            </NavLink>
            <NavLink to="/sessions" className="hover:underline">
              Sessions
            </NavLink>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-5xl p-6">
        <Routes>
          <Route path="/" element={<Navigate to="/teas" replace />} />
          <Route path="/teas" element={<TeasPage />} />
          <Route path="/teas/new" element={<NewTeaPage />} />
          <Route path="/sessions" element={<div>Sessions page next.</div>} />
        </Routes>
      </main>
    </div>
  );
}