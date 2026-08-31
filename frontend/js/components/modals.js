/**
 * StudyChart AI - Modal Controller.
 */

export const modal = {
  open(title, contentHtml, footerHtml = "") {
    const container = document.getElementById("modal-container");
    if (!container) return;

    container.innerHTML = `
      <div class="modal-overlay active" id="active-modal">
        <div class="modal-box">
          <div class="modal-header">
            <h3 style="font-size: 1.2rem; font-weight: 700;">${title}</h3>
            <button id="modal-close-btn" style="background:none; border:none; color:var(--text-muted); cursor:pointer; font-size:1.4rem;">&times;</button>
          </div>
          <div class="modal-body">${contentHtml}</div>
          ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ""}
        </div>
      </div>
    `;

    document.getElementById("modal-close-btn").addEventListener("click", () => this.close());
    document.getElementById("active-modal").addEventListener("click", (e) => {
      if (e.target.id === "active-modal") this.close();
    });
  },

  close() {
    const container = document.getElementById("modal-container");
    if (container) container.innerHTML = "";
  }
};
