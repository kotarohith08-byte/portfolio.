/**
 * StudyChart AI - Reactive Application State.
 */

class Store {
  constructor() {
    this.state = {
      user: null,
      profile: null,
      theme: localStorage.getItem("studychart_theme") || "dark",
      unreadNotifications: 0,
    };
    this.listeners = [];
  }

  getState() {
    return this.state;
  }

  setState(partialState) {
    this.state = { ...this.state, ...partialState };
    this.notify();
  }

  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  notify() {
    for (const listener of this.listeners) {
      listener(this.state);
    }
  }

  setTheme(theme) {
    this.state.theme = theme;
    localStorage.setItem("studychart_theme", theme);
    document.documentElement.setAttribute("data-theme", theme);
    this.notify();
  }
}

export const store = new Store();
