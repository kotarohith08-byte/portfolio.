# Kota Rohith - Personal AI & ML Developer Portfolio

A modern, high-performance, dark-themed developer portfolio website built with semantic **HTML5**, **CSS3**, and **Vanilla JavaScript**. Specially tailored for academic presentations at **Lovely Professional University (LPU)**, recruiter reviews, and technical showcases.

---

## 🌟 Key Features

- 🌌 **Dark Futuristic AI Theme**: Glassmorphism cards, glowing gradients, and subtle neon highlights.
- 🧠 **Interactive Neural Particle Background**: Lightweight HTML5 Canvas particle network that gently interacts with mouse movement.
- ⚡ **Zero Dependencies**: Pure HTML/CSS/JS. No `npm install`, Node setup, or build pipelines required.
- 📽️ **Presentation & Projector Mode**:
  - Click the **Present** button in the navbar (or press `P` on your keyboard) to switch into high-contrast presentation mode optimized for classroom and conference room projectors.
  - Navigate sections like slides using **Left/Right Arrow keys**.
- 🛠️ **Interactive Project Modals**: Click *"View Details"* on any project to view architectural breakdowns, sensor telemetry, and hardware/software specs.
- 🎓 **Verified Credentials Preview**: Interactive certificate modal viewer.
- 📱 **100% Responsive**: Looks pristine across 4K displays, laptops, tablets, and smartphones.

---

## 📂 Project Structure

```
kota-rohith-portfolio/
│
├── index.html              # Main HTML5 single-page structure
├── css/
│   ├── style.css           # Core styling, responsive grid & glassmorphism
│   └── presentation.css    # High-contrast presentation/projector styles
├── js/
│   ├── neural-canvas.js    # Interactive canvas particle network
│   ├── presentation.js     # Presentation mode controller & keyboard navigation
│   └── main.js             # Modals, typewriter, filter tabs & form logic
└── README.md               # Customization & deployment guide
```

---

## 🚀 How to Run Locally

Simply double-click `index.html` in your file explorer or open it in any web browser (Chrome, Edge, Firefox, Brave, Safari).

If using VS Code, you can also right-click `index.html` and select **"Open with Live Server"**.

---

## ✏️ How to Customize Your Information

### 1. Change Social Links & Email
In `index.html`, search for `<!-- EDIT YOUR SOCIAL LINKS HERE -->` and replace the placeholder URLs with your actual links:
- GitHub: `https://github.com/kotarohith08-byte`
- LinkedIn: `https://www.linkedin.com/in/kota-rohith-undefined-92a355398/`
- Email: `kotarohith08@gmail.com`
- Live CodeVault App: `https://kota-rohith.onrender.com/`

### 2. Add Your Real Photo
To replace the default AI avatar with your real photo:
In `index.html`, find `.avatar-inner` inside the Hero section:
```html
<div class="avatar-inner">
  <img src="assets/my-photo.jpg" alt="Kota Rohith" style="width: 100%; height: 100%; object-fit: cover;">
</div>
```

### 3. Replace Placeholder Certificates
In `index.html`, locate the `<!-- Certificates Gallery -->` section and update the `data-cert-title`, `data-cert-issuer`, and `data-cert-date` attributes or link your actual credential URLs.

### 4. Update Resume File
Place your PDF resume (e.g. `Kota_Rohith_Resume.pdf`) in the folder and update the link in `index.html`:
```html
<a href="Kota_Rohith_Resume.pdf" download class="btn btn-secondary">
  <i class="fas fa-file-download"></i> Download Resume
</a>
```

---

## 🌐 How to Deploy for Free

### Option A: Deploy to GitHub Pages (Recommended)
1. Initialize a Git repository and commit your files:
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio release"
   ```
2. Create a new GitHub repository named `kotarohith.github.io` (or `portfolio`).
3. Push your repository:
   ```bash
   git remote add origin https://github.com/KotaRohith/kotarohith.github.io.git
   git branch -M main
   git push -u origin main
   ```
4. Go to **Repository Settings** -> **Pages** -> Select `main` branch -> **Save**. Your site will be live at `https://kotarohith.github.io`!

### Option B: Deploy to Vercel / Netlify
- Drag and drop the `kota-rohith-portfolio` folder directly into [Netlify Drop](https://app.netlify.com/drop) or import from GitHub into [Vercel](https://vercel.com).
