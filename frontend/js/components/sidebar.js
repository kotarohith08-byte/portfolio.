/**
 * StudyChart AI - App Sidebar Navigation.
 */

import { store } from "../store.js";
import { auth } from "../auth.js";

export function renderSidebar(currentPath) {
  const profile = store.getState().profile;
  const level = profile ? profile.current_level : 1;
  const xp = profile ? profile.current_xp : 0;

  const links = [
    { path: "#/app/dashboard", label: "Dashboard", icon: "📊" },
    { path: "#/app/study-plan", label: "AI Study Plan", icon: "🗓️" },
    { path: "#/app/subjects", label: "Subjects", icon: "📚" },
    { path: "#/app/quiz", label: "AI Quizzes", icon: "🧠" },
    { path: "#/app/ai-tutor", label: "AI Tutor", icon: "🤖" },
    { path: "#/app/notes", label: "Notes & Cards", icon: "📝" },
    { path: "#/app/timer", label: "Study Timer", icon: "⏱️" },
    { path: "#/app/calendar", label: "Calendar", icon: "📅" },
    { path: "#/app/programming", label: "Coding Lab", icon: "💻" },
    { path: "#/app/analytics", label: "Analytics", icon: "📈" },
    { path: "#/app/achievements", label: "Achievements", icon: "🏆" },
    { path: "#/app/profile", label: "Profile & Settings", icon: "⚙️" },
  ];

  return `
    <aside class="sidebar">
      <div class="sidebar-header">
        <span style="font-size: 1.5rem;">⚡</span>
        <span class="sidebar-brand">StudyChart AI</span>
      </div>

      <nav class="sidebar-nav">
        ${links.map(l => `
          <a href="${l.path}" class="nav-link ${currentPath === l.path ? "active" : ""}">
            <span style="font-size: 1.15rem;">${l.icon}</span>
            <span>${l.label}</span>
          </a>
        `).join("")}
      </nav>

      <div class="sidebar-footer">
        <div style="display: flex; flex-direction: column;">
          <span style="font-size: 0.85rem; font-weight: 700; color: var(--accent-primary);">Level ${level} Scholar</span>
          <span style="font-size: 0.75rem; color: var(--text-muted);">${xp} Total XP</span>
        </div>
        <button id="sidebar-logout-btn" style="background: none; border: none; color: var(--danger); cursor: pointer; font-size: 1.2rem;" title="Sign Out">🚪</button>
      </div>
    </aside>
  `;
}
