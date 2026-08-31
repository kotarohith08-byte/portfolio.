/**
 * StudyChart AI - Authentication Helper Module.
 */

import { api } from "./api.js";
import { store } from "./store.js";

export const auth = {
  isAuthenticated() {
    return !!localStorage.getItem("studychart_access_token");
  },

  async login(email, password) {
    const res = await api.login({ email, password });
    api.setTokens(res.access_token, res.refresh_token);
    await this.fetchProfile();
    return res;
  },

  async register(name, email, password, confirm_password) {
    const res = await api.register({ name, email, password, confirm_password });
    api.setTokens(res.access_token, res.refresh_token);
    await this.fetchProfile();
    return res;
  },

  async fetchProfile() {
    try {
      const profile = await api.getProfile();
      store.setState({ profile, user: { name: profile.name, email: profile.email, id: profile.user_id } });
      return profile;
    } catch (err) {
      this.logout();
      return null;
    }
  },

  logout() {
    api.clearTokens();
    store.setState({ user: null, profile: null });
    window.location.hash = "#/auth/login";
  }
};
