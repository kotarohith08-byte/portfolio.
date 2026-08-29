/**
 * Kota Rohith Portfolio - Presentation & Projector Mode Controller
 * Enables high-visibility presentation view, slide navigation, and fullscreen support.
 */

(function () {
  const toggleBtn = document.getElementById('presentation-toggle-btn');
  const sections = Array.from(document.querySelectorAll('section.section, header.hero-section'));
  let currentSectionIndex = 0;
  let isPresentationActive = false;

  // Create presentation control bar element if not present
  let presBar = document.querySelector('.presentation-bar');
  if (!presBar) {
    presBar = document.createElement('div');
    presBar.className = 'presentation-bar';
    presBar.innerHTML = `
      <span class="pres-info" id="pres-slide-indicator">Slide 1/${sections.length}</span>
      <div class="pres-nav-btns">
        <button class="pres-btn" id="pres-prev-btn" title="Previous Slide (Left Arrow)"><i class="fas fa-chevron-left"></i></button>
        <button class="pres-btn" id="pres-next-btn" title="Next Slide (Right Arrow)"><i class="fas fa-chevron-right"></i></button>
        <button class="pres-btn" id="pres-fs-btn" title="Toggle Fullscreen"><i class="fas fa-expand"></i></button>
      </div>
      <button class="pres-btn-exit" id="pres-exit-btn" title="Exit Presentation Mode (Esc)">
        <i class="fas fa-times"></i> Exit
      </button>
    `;
    document.body.appendChild(presBar);
  }

  const slideIndicator = document.getElementById('pres-slide-indicator');
  const prevBtn = document.getElementById('pres-prev-btn');
  const nextBtn = document.getElementById('pres-next-btn');
  const fsBtn = document.getElementById('pres-fs-btn');
  const exitBtn = document.getElementById('pres-exit-btn');

  function updateSlideIndicator() {
    if (slideIndicator && sections[currentSectionIndex]) {
      const sectionName = sections[currentSectionIndex].getAttribute('data-section-name') || 
                          sections[currentSectionIndex].id.toUpperCase();
      slideIndicator.textContent = `Slide ${currentSectionIndex + 1}/${sections.length} • ${sectionName}`;
    }
  }

  function goToSection(index) {
    if (index < 0) index = 0;
    if (index >= sections.length) index = sections.length - 1;
    currentSectionIndex = index;
    updateSlideIndicator();

    const target = sections[currentSectionIndex];
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function togglePresentationMode(forceState) {
    if (typeof forceState === 'boolean') {
      isPresentationActive = forceState;
    } else {
      isPresentationActive = !isPresentationActive;
    }

    if (isPresentationActive) {
      document.body.classList.add('presentation-mode');
      if (toggleBtn) {
        toggleBtn.innerHTML = '<i class="fas fa-times"></i> Exit Presentation';
      }
      // Determine nearest current section
      const scrollPos = window.scrollY + 200;
      for (let i = sections.length - 1; i >= 0; i--) {
        if (scrollPos >= sections[i].offsetTop) {
          currentSectionIndex = i;
          break;
        }
      }
      updateSlideIndicator();
      if (window.showToast) {
        window.showToast('Presentation Mode Activated! Use Arrow keys to navigate slides.');
      }
    } else {
      document.body.classList.remove('presentation-mode');
      if (toggleBtn) {
        toggleBtn.innerHTML = '<i class="fas fa-desktop"></i> Present';
      }
      if (document.fullscreenElement) {
        document.exitFullscreen().catch(() => {});
      }
      if (window.showToast) {
        window.showToast('Exited Presentation Mode.');
      }
    }
  }

  // Toggle button event
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => togglePresentationMode());
  }

  // Navigation events
  if (prevBtn) prevBtn.addEventListener('click', () => goToSection(currentSectionIndex - 1));
  if (nextBtn) nextBtn.addEventListener('click', () => goToSection(currentSectionIndex + 1));
  if (exitBtn) exitBtn.addEventListener('click', () => togglePresentationMode(false));

  if (fsBtn) {
    fsBtn.addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    });
  }

  // Keyboard navigation
  window.addEventListener('keydown', (e) => {
    // If user is typing in form input/textarea, ignore shortcuts
    if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

    if (e.key === 'p' || e.key === 'P') {
      if (!e.ctrlKey && !e.metaKey && !e.altKey) {
        togglePresentationMode();
      }
    } else if (isPresentationActive) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
        e.preventDefault();
        goToSection(currentSectionIndex + 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        goToSection(currentSectionIndex - 1);
      } else if (e.key === 'Escape') {
        togglePresentationMode(false);
      }
    }
  });

  window.togglePresentationMode = togglePresentationMode;
})();
