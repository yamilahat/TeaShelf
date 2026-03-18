import type { ReactNode } from "react";
import { Navigate, NavLink, Route, Routes } from "react-router";
import { NewTeaPage } from "./pages/NewTeaPage";
import { TeaDetailPage } from "./pages/TeaDetailPage";
import { TeasPage } from "./pages/TeasPage";

function ShellLayout({ children }: { children: ReactNode }) {
  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="site-header__inner">
          <div>
            <h1>TeaShelf</h1>
            <p className="muted">A simple home for your tea collection and notes.</p>
          </div>

          <nav className="nav">
            <NavItem to="/teas">Teas</NavItem>
            <NavItem to="/sessions">Sessions</NavItem>
          </nav>
        </div>
      </header>

      <main className="page">{children}</main>
    </div>
  );
}

function NavItem({ to, children }: { to: string; children: ReactNode }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) => `nav__item${isActive ? " nav__item--active" : ""}`}
    >
      {children}
    </NavLink>
  );
}

function SessionsPage() {
  return (
    <section className="panel stack">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Sessions</p>
          <h2>Tasting sessions</h2>
        </div>
        <p className="muted">A place for brewing notes and tasting history.</p>
      </div>

      <p className="muted">
        Session tracking is coming next. For now, you can browse and manage your tea collection.
      </p>
    </section>
  );
}

export default function App() {
  return (
    <ShellLayout>
      <Routes>
        <Route path="/" element={<Navigate to="/teas" replace />} />
        <Route path="/teas" element={<TeasPage />} />
        <Route path="/teas/new" element={<NewTeaPage />} />
        <Route path="/teas/:teaId" element={<TeaDetailPage />} />
        <Route path="/sessions" element={<SessionsPage />} />
      </Routes>
    </ShellLayout>
  );
}
