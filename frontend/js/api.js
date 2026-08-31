/**
 * StudyChart AI - Centralized HTTP API Client.
 * Automatically injects JWT Bearer tokens and handles token refreshes.
 */

const API_BASE = window.location.port === "8000" ? "/api/v1" : "http://localhost:8000/api/v1";

class APIClient {
  constructor() {
    this.token = localStorage.getItem("studychart_access_token") || null;
    this.refreshToken = localStorage.getItem("studychart_refresh_token") || null;
  }

  setTokens(access, refresh) {
    this.token = access;
    this.refreshToken = refresh;
    if (access) localStorage.setItem("studychart_access_token", access);
    else localStorage.removeItem("studychart_access_token");
    if (refresh) localStorage.setItem("studychart_refresh_token", refresh);
    else localStorage.removeItem("studychart_refresh_token");
  }

  clearTokens() {
    this.token = null;
    this.refreshToken = null;
    localStorage.removeItem("studychart_access_token");
    localStorage.removeItem("studychart_refresh_token");
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = {
      "Content-Type": "application/json",
      ...(options.headers || {})
    };

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    try {
      let resp = await fetch(url, { ...options, headers });

      // Handle 401 Unauthorized (attempt refresh)
      if (resp.status === 401 && this.refreshToken && !endpoint.includes("/auth/")) {
        const refreshed = await this.tryRefreshToken();
        if (refreshed) {
          headers["Authorization"] = `Bearer ${this.token}`;
          resp = await fetch(url, { ...options, headers });
        } else {
          this.clearTokens();
          window.location.hash = "#/auth/login";
          throw new Error("Session expired. Please log in again.");
        }
      }

      const data = await resp.json();
      if (!resp.ok) {
        const errMsg = data?.error?.message || data?.detail || "An unexpected error occurred.";
        throw new Error(errMsg);
      }
      return data;
    } catch (err) {
      throw err;
    }
  }

  async tryRefreshToken() {
    try {
      const resp = await fetch(`${API_BASE}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: this.refreshToken })
      });
      if (resp.ok) {
        const data = await resp.json();
        this.setTokens(data.access_token, data.refresh_token);
        return true;
      }
    } catch (e) {}
    return false;
  }

  // Auth
  register(body) { return this.request("/auth/register", { method: "POST", body: JSON.stringify(body) }); }
  login(body) { return this.request("/auth/login", { method: "POST", body: JSON.stringify(body) }); }
  forgotPassword(email) { return this.request("/auth/forgot-password", { method: "POST", body: JSON.stringify({ email }) }); }
  resetPassword(token, new_password) { return this.request("/auth/reset-password", { method: "POST", body: JSON.stringify({ token, new_password }) }); }

  // Profile & User
  getProfile() { return this.request("/me"); }
  updateProfile(body) { return this.request("/me", { method: "PATCH", body: JSON.stringify(body) }); }
  exportData() { return this.request("/me/export"); }
  deleteAccount() { return this.request("/me", { method: "DELETE" }); }

  // Dashboard & Analytics
  getDashboard() { return this.request("/dashboard"); }
  getAnalytics() { return this.request("/analytics"); }

  // Subjects
  getSubjects(include_archived = false) { return this.request(`/subjects?include_archived=${include_archived}`); }
  getSubject(id) { return this.request(`/subjects/${id}`); }
  createSubject(body) { return this.request("/subjects", { method: "POST", body: JSON.stringify(body) }); }
  updateSubject(id, body) { return this.request(`/subjects/${id}`, { method: "PATCH", body: JSON.stringify(body) }); }
  deleteSubject(id) { return this.request(`/subjects/${id}`, { method: "DELETE" }); }
  addUnit(subjectId, body) { return this.request(`/subjects/${subjectId}/units`, { method: "POST", body: JSON.stringify(body) }); }

  // Study Plans
  getStudyPlans() { return this.request("/study-plans"); }
  getActivePlan() { return this.request("/study-plans/active"); }
  createPlan(body) { return this.request("/study-plans", { method: "POST", body: JSON.stringify(body) }); }
  updatePlanItem(itemId, body) { return this.request(`/study-plans/items/${itemId}`, { method: "PATCH", body: JSON.stringify(body) }); }

  // Study Sessions (Timer)
  getSessions(limit = 50) { return this.request(`/study-sessions?limit=${limit}`); }
  recordSession(body) { return this.request("/study-sessions", { method: "POST", body: JSON.stringify(body) }); }

  // Quizzes
  getQuizzes() { return this.request("/quizzes"); }
  getQuiz(id) { return this.request(`/quizzes/${id}`); }
  submitQuiz(id, body) { return this.request(`/quizzes/${id}/attempt`, { method: "POST", body: JSON.stringify(body) }); }

  // Notes
  getNotes(search = "", tag = "") {
    let q = "";
    if (search) q += `search=${encodeURIComponent(search)}&`;
    if (tag) q += `tag=${encodeURIComponent(tag)}`;
    return this.request(`/notes?${q}`);
  }
  getNote(id) { return this.request(`/notes/${id}`); }
  createNote(body) { return this.request("/notes", { method: "POST", body: JSON.stringify(body) }); }
  updateNote(id, body) { return this.request(`/notes/${id}`, { method: "PATCH", body: JSON.stringify(body) }); }
  deleteNote(id) { return this.request(`/notes/${id}`, { method: "DELETE" }); }
  performNoteAI(id, action) { return this.request(`/notes/${id}/ai`, { method: "POST", body: JSON.stringify({ action }) }); }

  // AI Services
  generateAIStudyPlan(body) { return this.request("/ai/study-plan", { method: "POST", body: JSON.stringify(body) }); }
  generateAIQuiz(body) { return this.request("/ai/quiz", { method: "POST", body: JSON.stringify(body) }); }
  chatAITutor(body) { return this.request("/ai/tutor", { method: "POST", body: JSON.stringify(body) }); }
  analyzePerformance() { return this.request("/ai/analyze-performance", { method: "POST" }); }

  // Calendar
  getCalendarEvents() { return this.request("/calendar"); }
  createCalendarEvent(body) { return this.request("/calendar", { method: "POST", body: JSON.stringify(body) }); }
  updateCalendarEvent(id, body) { return this.request(`/calendar/${id}`, { method: "PATCH", body: JSON.stringify(body) }); }
  deleteCalendarEvent(id) { return this.request(`/calendar/${id}`, { method: "DELETE" }); }

  // Programming Lab
  getProblems() { return this.request("/programming/problems"); }
  getProblem(slug) { return this.request(`/programming/problems/${slug}`); }
  submitCode(body) { return this.request("/programming/submit", { method: "POST", body: JSON.stringify(body) }); }

  // Achievements
  getAchievements() { return this.request("/achievements"); }

  // Notifications
  getNotifications() { return this.request("/notifications"); }
  markNotificationRead(id) { return this.request(`/notifications/${id}/read`, { method: "POST" }); }
  markAllNotificationsRead() { return this.request("/notifications/read-all", { method: "POST" }); }

  // Search
  search(query) { return this.request(`/search?q=${encodeURIComponent(query)}`); }
}

export const api = new APIClient();
