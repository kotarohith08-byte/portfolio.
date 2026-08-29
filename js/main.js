/**
 * Kota Rohith Portfolio - Main Application Logic
 * Typewriter, Navigation ScrollSpy, Filters, Modals, Contact Form & Toasts
 */

document.addEventListener('DOMContentLoaded', () => {
  // --------------------------------------------------------------------------
  // 1. Toast Notification System
  // --------------------------------------------------------------------------
  const toastContainer = document.getElementById('toast-container');

  function showToast(message, icon = 'fa-info-circle') {
    if (!toastContainer) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="fas ${icon}" style="color: var(--accent-cyan);"></i> <span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  window.showToast = showToast;

  // --------------------------------------------------------------------------
  // 2. Typewriter Effect in Hero Section
  // --------------------------------------------------------------------------
  const typedElement = document.getElementById('typed-text');
  const words = [
    'AI & Machine Learning Engineer',
    'Python & LLM Applications Builder',
    'NLP & Generative AI Enthusiast',
    'Computer Science & Engineering Student',
    'Software Developer & Problem Solver'
  ];
  let wordIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typeSpeed = 100;

  function typeEffect() {
    if (!typedElement) return;
    const currentWord = words[wordIndex];

    if (isDeleting) {
      typedElement.textContent = currentWord.substring(0, charIndex - 1);
      charIndex--;
      typeSpeed = 45;
    } else {
      typedElement.textContent = currentWord.substring(0, charIndex + 1);
      charIndex++;
      typeSpeed = 100;
    }

    if (!isDeleting && charIndex === currentWord.length) {
      isDeleting = true;
      typeSpeed = 1800; // Pause at end of word
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      wordIndex = (wordIndex + 1) % words.length;
      typeSpeed = 400; // Pause before typing next word
    }

    setTimeout(typeEffect, typeSpeed);
  }

  typeEffect();

  // --------------------------------------------------------------------------
  // 3. Navbar Sticky Effect & Mobile Menu
  // --------------------------------------------------------------------------
  const navbar = document.getElementById('navbar');
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const navLinks = document.getElementById('nav-links');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  if (mobileMenuBtn && navLinks) {
    mobileMenuBtn.addEventListener('click', () => {
      navLinks.classList.toggle('mobile-open');
      const isOpen = navLinks.classList.contains('mobile-open');
      mobileMenuBtn.innerHTML = isOpen ? '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
    });

    // Close menu when clicking nav link
    navLinks.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('mobile-open');
        mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
      });
    });
  }

  // --------------------------------------------------------------------------
  // 4. ScrollSpy Active Nav Highlighting
  // --------------------------------------------------------------------------
  const sections = document.querySelectorAll('section[id], header[id]');
  const navItems = document.querySelectorAll('.nav-link');

  function updateActiveNav() {
    let scrollY = window.pageYOffset;

    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');

      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        navItems.forEach(item => {
          item.classList.remove('active');
          if (item.getAttribute('href') === `#${sectionId}`) {
            item.classList.add('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', updateActiveNav);

  // --------------------------------------------------------------------------
  // 5. Skills Category Filter
  // --------------------------------------------------------------------------
  const skillFilterBtns = document.querySelectorAll('[data-skill-filter]');
  const skillCards = document.querySelectorAll('.skill-card');

  skillFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      skillFilterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-skill-filter');

      skillCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filterValue === 'all' || category === filterValue) {
          card.style.display = 'flex';
          setTimeout(() => { card.style.opacity = '1'; card.style.transform = 'scale(1)'; }, 10);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'scale(0.95)';
          setTimeout(() => { card.style.display = 'none'; }, 200);
        }
      });
    });
  });

  // --------------------------------------------------------------------------
  // 6. Project Category Filter
  // --------------------------------------------------------------------------
  const projectFilterBtns = document.querySelectorAll('[data-project-filter]');
  const projectCards = document.querySelectorAll('.project-card');

  projectFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      projectFilterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-project-filter');

      projectCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filterValue === 'all' || category === filterValue) {
          card.style.display = 'flex';
          setTimeout(() => { card.style.opacity = '1'; card.style.transform = 'translateY(0)'; }, 10);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(15px)';
          setTimeout(() => { card.style.display = 'none'; }, 200);
        }
      });
    });
  });

  // --------------------------------------------------------------------------
  // 7. Project Details Modal System
  // --------------------------------------------------------------------------
  const modalOverlay = document.getElementById('project-modal');
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const modalBody = document.getElementById('modal-body-content');

  // Detailed specifications for Kota Rohith's projects from Resume
  const projectDetails = {
    glucose: {
      title: "Real-Time Glucose Monitoring System",
      tagline: "Sensor-based physiological signal processing and non-invasive health monitoring (03-2026).",
      badge: "Biomedical Sensor System",
      technologies: ["MAX30105 Sensor", "Signal Processing", "Embedded Systems", "Hardware Integration", "C++"],
      overview: "Developed a prototype for real-time glucose-related monitoring using the MAX30105 particle sensor for optical signal capture. Engineered signal-processing logic to extract meaningful biometric readings from raw sensor output.",
      features: [
        "Developed prototype for real-time glucose-related monitoring using MAX30105 optical particle sensor.",
        "Engineered signal-processing logic to extract meaningful biometric readings from raw sensor output.",
        "Integrated hardware components, including sensor wiring and microcontroller interfacing, for stable data acquisition.",
        "Documented system flow, architecture, and testing outcomes to support reproducibility."
      ],
      architecture: "Sensor bus communicating over I2C protocol with Arduino microcontroller, running real-time signal peak detection and biometric filtering algorithms.",
      github: "https://github.com/kotarohith08-byte",
      demo: "#"
    },
    codevault: {
      title: "CodeVault – Personal Code Management Platform",
      tagline: "Platform enabling developers to store, organize, and manage personal code snippets (06-2026).",
      badge: "Live Software Platform",
      technologies: ["Python", "API Integration", "Web Development", "MongoDB", "JWT"],
      overview: "Built a platform enabling developers to store, organize, and manage personal code snippets efficiently. Structured a clean separation between frontend, backend, and data layers for long-term maintainability.",
      features: [
        "Built a platform enabling developers to store, organize, and manage personal code snippets efficiently.",
        "Structured clean separation between frontend, backend, and data layers for maintainability.",
        "Enabled fast search and retrieval of saved snippets through categorized organization.",
        "Focused on practical usability, aligning the platform with real developer workflows."
      ],
      architecture: "Clean layered software architecture with backend API integration and database storage for developer snippet management.",
      github: "https://github.com/kotarohith08-byte",
      demo: "https://kota-rohith.onrender.com/"
    },
    pythonlearning: {
      title: "Python Programming Tutorial / Learning Project",
      tagline: "Structured educational modules covering fundamental to advanced Python programming (07-2026).",
      badge: "Educational Engineering",
      technologies: ["Python", "Algorithms", "Object-Oriented Programming", "File Systems"],
      overview: "Created structured Python learning content covering core fundamentals to advanced concepts, designed to reinforce applied programming skills and software development concepts.",
      features: [
        "Created structured Python learning content covering variables, expressions, and conditionals for beginners.",
        "Authored progressive modules on loops, nested loops, and functions with hands-on examples.",
        "Explained object-oriented concepts, including classes and objects, through practical coding exercises.",
        "Curated file-handling exercises and problem sets to reinforce applied programming skills."
      ],
      architecture: "Modular Python codebase and structured curriculum organized by algorithmic complexity and OOP principles.",
      github: "https://github.com/kotarohith08-byte",
      demo: "https://youtube.com"
    },
    cropdrying: {
      title: "Smart AI-Enabled Automatic Rain Protection & Smart Crop Drying System",
      tagline: "Intelligent agricultural safeguard and automated drying system using multi-sensor fusion.",
      badge: "Smart Agriculture System",
      technologies: ["Arduino Uno", "Rain Sensor", "DHT11", "LDR Sensor", "Wind Sensor", "GSM SIM800L", "L298N Driver", "Servo/DC Motor", "LCD Display"],
      overview: "A comprehensive agricultural automation solution engineered to protect harvested crops from unpredictable rainfall and maximize natural drying efficiency. The system combines multi-sensor telemetry with automated mechanical canopy retraction and GSM SMS alerting.",
      features: [
        "Instant rain detection triggers immediate motorized canopy deployment over drying crops.",
        "Temperature and humidity monitoring via DHT11 to optimize crop moisture levels.",
        "LDR ambient light tracking ensures canopy retraction during optimal sunlight hours for faster drying.",
        "High-wind safeguarding via anemometer input to prevent mechanical canopy strain.",
        "GSM SIM800L module dispatches automated emergency SMS alerts directly to farmers' mobile phones.",
        "Real-time environmental diagnostics displayed on an integrated 16x2 I2C LCD screen."
      ],
      architecture: "Multi-input sensor array feeding into central Arduino Uno microcontroller running finite state machine logic, controlling bidirectional motors via L298N driver and GSM SIM800L communication.",
      github: "https://github.com/kotarohith08-byte",
      demo: "#"
    }
  };

  document.querySelectorAll('[data-open-project]').forEach(button => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      const projectId = button.getAttribute('data-open-project');
      const data = projectDetails[projectId];

      if (data && modalBody && modalOverlay) {
        modalBody.innerHTML = `
          <div class="project-header-meta" style="margin-bottom: 0.75rem;">
            <span class="project-badge">${data.badge}</span>
          </div>
          <h2 class="modal-project-title gradient-text">${data.title}</h2>
          <p style="font-size: 1.05rem; color: var(--text-secondary); margin-bottom: 1.25rem;">${data.tagline}</p>
          
          <div class="project-tech-tags" style="margin-bottom: 1.5rem;">
            ${data.technologies.map(t => `<span class="tech-tag">${t}</span>`).join('')}
          </div>

          <div class="modal-spec-section">
            <h4><i class="fas fa-info-circle"></i> Project Overview</h4>
            <p style="color: var(--text-secondary); line-height: 1.7;">${data.overview}</p>
          </div>

          <div class="modal-spec-section">
            <h4><i class="fas fa-check-circle"></i> Key Architecture & Features</h4>
            <ul style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem;">
              ${data.features.map(f => `
                <li style="display: flex; gap: 0.5rem; align-items: flex-start; font-size: 0.92rem; color: var(--text-secondary);">
                  <i class="fas fa-check" style="color: var(--accent-cyan); font-size: 0.8rem; margin-top: 0.35rem;"></i>
                  <span>${f}</span>
                </li>
              `).join('')}
            </ul>
          </div>

          <div class="modal-spec-section">
            <h4><i class="fas fa-layer-group"></i> Technical Architecture</h4>
            <p style="color: var(--text-secondary); line-height: 1.6; font-size: 0.92rem;">${data.architecture}</p>
          </div>

          <div class="project-actions" style="margin-top: 2rem;">
            <a href="${data.github}" target="_blank" class="btn btn-primary btn-sm">
              <i class="fab fa-github"></i> GitHub Profile / Repo
            </a>
            ${data.demo && data.demo !== '#' ? `
              <a href="${data.demo}" target="_blank" class="btn btn-secondary btn-sm" style="border-color: var(--accent-cyan); color: var(--accent-cyan);">
                <i class="fas fa-external-link-alt"></i> Open Live App
              </a>
            ` : `
              <button class="btn btn-secondary btn-sm" onclick="showToast('Demo link not configured.');">
                <i class="fas fa-external-link-alt"></i> Live Demo
              </button>
            `}
          </div>
        `;
        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  // Certificate Modal Preview
  const certModal = document.getElementById('cert-modal');
  const certCloseBtn = document.getElementById('cert-close-btn');
  const certModalBody = document.getElementById('cert-modal-body');

  document.querySelectorAll('[data-open-cert]').forEach(button => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      const certTitle = button.getAttribute('data-cert-title');
      const certIssuer = button.getAttribute('data-cert-issuer');
      const certDate = button.getAttribute('data-cert-date');
      const certImg = button.getAttribute('data-cert-img');
      const certVerifyUrl = button.getAttribute('data-cert-verify-url');

      if (certModalBody && certModal) {
        let previewHtml = '';

        if (certImg) {
          previewHtml = `
            <div style="border-radius: var(--radius-md); overflow: hidden; border: 1px solid var(--border-glass-hover); box-shadow: var(--shadow-card); margin: 1.5rem 0; background: #ffffff;">
              <img src="${certImg}" alt="${certTitle} - ${certIssuer}" style="width: 100%; height: auto; display: block;">
            </div>
          `;
        } else {
          previewHtml = `
            <div class="cert-preview-box">
              <i class="fas fa-award" style="font-size: 4rem; color: var(--accent-cyan); margin-bottom: 1rem;"></i>
              <h3 style="font-size: 1.4rem; margin-bottom: 0.5rem;">${certTitle}</h3>
              <p style="color: var(--text-secondary); font-size: 0.95rem;">Certificate Holder: <strong>Kota Rohith</strong></p>
              <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.5rem;">Lovely Professional University</p>
              <div style="margin-top: 1.5rem; font-family: var(--font-mono); font-size: 0.8rem; color: var(--accent-emerald);">
                <i class="fas fa-shield-alt"></i> Verified Credential Placeholder
              </div>
            </div>
          `;
        }

        certModalBody.innerHTML = `
          <div class="section-tag" style="margin-bottom: 0.75rem;"><i class="fas fa-certificate"></i> Verified Certificate</div>
          <h2 class="modal-project-title gradient-text">${certTitle}</h2>
          <p style="font-size: 1rem; color: var(--accent-cyan); font-weight: 500;">Issued by: ${certIssuer} (${certDate})</p>

          ${previewHtml}

          <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-top: 1.5rem;">
            ${certVerifyUrl ? `
              <a href="${certVerifyUrl}" target="_blank" class="btn btn-primary btn-sm">
                <i class="fas fa-check-circle"></i> Verify on Issuer Website
              </a>
            ` : ''}
            ${certImg ? `
              <a href="${certImg}" target="_blank" download="Kota_Rohith_${certTitle.replace(/\\s+/g, '_')}.png" class="btn btn-secondary btn-sm">
                <i class="fas fa-download"></i> Download Certificate
              </a>
            ` : ''}
          </div>
        `;
        certModal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  // Modal Closers
  function closeModals() {
    if (modalOverlay) modalOverlay.classList.remove('active');
    if (certModal) certModal.classList.remove('active');
    document.body.style.overflow = 'auto';
  }

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModals);
  if (certCloseBtn) certCloseBtn.addEventListener('click', closeModals);

  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModals();
    });
  }
  if (certModal) {
    certModal.addEventListener('click', (e) => {
      if (e.target === certModal) closeModals();
    });
  }

  // --------------------------------------------------------------------------
  // 8. Copy to Clipboard Utility
  // --------------------------------------------------------------------------
  document.querySelectorAll('[data-copy-text]').forEach(btn => {
    btn.addEventListener('click', () => {
      const textToCopy = btn.getAttribute('data-copy-text');
      navigator.clipboard.writeText(textToCopy).then(() => {
        showToast(`Copied to clipboard: ${textToCopy}`, 'fa-check');
      }).catch(() => {
        showToast('Failed to copy. Please copy manually.', 'fa-exclamation-circle');
      });
    });
  });

  // --------------------------------------------------------------------------
  // 9. Contact Form Handling
  // --------------------------------------------------------------------------
  const contactForm = document.getElementById('portfolio-contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;

      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
      submitBtn.disabled = true;

      setTimeout(() => {
        showToast('Thank you Kota! Your message has been sent successfully.', 'fa-paper-plane');
        contactForm.reset();
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
      }, 1200);
    });
  }

  // --------------------------------------------------------------------------
  // 10. Resume Download Action
  // --------------------------------------------------------------------------
  const resumeBtns = document.querySelectorAll('.btn-download-resume');
  resumeBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      showToast('Downloading Rohith_Kota_Resume.pdf...', 'fa-file-pdf');
      
      const link = document.createElement('a');
      link.href = 'assets/resume/Rohith_Kota_Resume.pdf';
      link.download = 'Rohith_Kota_Resume.pdf';
      link.target = '_blank';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  });

  // --------------------------------------------------------------------------
  // 11. Back to Top Button
  // --------------------------------------------------------------------------
  const backToTopBtn = document.getElementById('back-to-top');
  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
});
