/**
 * StudyChart AI - Toast Notification Manager.
 */

export const toast = {
  show(message, type = "info", duration = 4000) {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const el = document.createElement("div");
    el.className = `toast toast-${type}`;
    
    const icons = {
      success: "✓",
      danger: "✕",
      info: "ℹ",
      warning: "⚠"
    };

    el.innerHTML = `
      <span style="font-weight: bold;">${icons[type] || "ℹ"}</span>
      <span>${message}</span>
    `;

    container.appendChild(el);

    setTimeout(() => {
      el.style.opacity = "0";
      el.style.transform = "translateX(50px)";
      el.style.transition = "all 0.3s ease";
      setTimeout(() => el.remove(), 300);
    }, duration);
  },

  success(msg) { this.show(msg, "success"); },
  error(msg) { this.show(msg, "danger"); },
  info(msg) { this.show(msg, "info"); },
  warning(msg) { this.show(msg, "warning"); }
};
