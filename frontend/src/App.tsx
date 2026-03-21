import type { ReactNode } from "react";
import { Navigate, NavLink, Route, Routes } from "react-router";
import { NewTeaPage } from "./pages/NewTeaPage";
import { NewTeawarePage } from "./pages/NewTeawarePage";
import { SessionDetailPage } from "./pages/SessionDetailPage";
import { SessionsPage } from "./pages/SessionsPage";
import { TeaDetailPage } from "./pages/TeaDetailPage";
import { TeasPage } from "./pages/TeasPage";
import { TeawareDetailPage } from "./pages/TeawareDetailPage";
import { TeawarePage } from "./pages/TeawarePage";

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
            <NavItem to="/teaware">Teaware</NavItem>
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

export default function App() {
  return (
    <ShellLayout>
      <Routes>
        <Route path="/" element={<Navigate to="/teas" replace />} />
        <Route path="/teas" element={<TeasPage />} />
        <Route path="/teas/new" element={<NewTeaPage />} />
        <Route path="/teas/:teaId" element={<TeaDetailPage />} />
        <Route path="/teaware" element={<TeawarePage />} />
        <Route path="/teaware/new" element={<NewTeawarePage />} />
        <Route path="/teaware/:teawareId" element={<TeawareDetailPage />} />
        <Route path="/sessions" element={<SessionsPage />} />
        <Route path="/sessions/:sessionId" element={<SessionDetailPage />} />
      </Routes>
    </ShellLayout>
  );
}
