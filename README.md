# Hemalatha Yalamanchi — Portfolio

A clean, responsive, single-page portfolio built with plain HTML, CSS, and JavaScript.
No build step, no frameworks — just open the file or push it to GitHub Pages.

## Structure

```
.
├── index.html          # All content lives here (sections + nav)
├── css/styles.css      # Design system, layout, responsive rules
├── js/main.js          # Mobile menu, smooth scroll, scroll animations, active nav
├── assets/
│   ├── resume.pdf      # Your resume (currently a placeholder — replace it)
│   ├── profile.svg     # Headshot placeholder — replace with your photo
│   └── projects/       # Project screenshots
├── .nojekyll           # Tells GitHub Pages to serve files as-is
└── README.md
```

## How to edit the content

Open `index.html` and look for the `<!-- EDIT: ... -->` comments. They mark every spot
you'll want to personalize:

- **Hero** — your name, role/headline, and tagline (top of the page).
- **About** — your bio paragraphs, profile photo, and skill tags.
- **Projects** — copy the block marked `<!-- ==== PROJECT CARD ... ==== -->` once per project.
  Update the title, description, tech tags, image, and links.
- **Achievements** — copy the `<!-- ==== ACHIEVEMENT ITEM ... ==== -->` block per entry.
- **Resume** — replace `assets/resume.pdf` with your real file (keep the same name, or update
  the two links in the Resume section).
- **Contact** — update the email, LinkedIn, and GitHub links.

### Replacing images
- Profile photo: drop your image into `assets/` and update the `<img src="...">` in the About
  section. A square (1:1) image looks best.
- Project screenshots: add them to `assets/projects/` and point each card's `<img src="...">`
  at them. A 16:9 image looks best.

### Changing colors
All colors are CSS variables at the top of `css/styles.css` (the `:root` block). Change
`--accent` to re-theme the whole site. Light-mode colors are in the `prefers-color-scheme: light`
block just below.

## Previewing locally

Just double-click `index.html`, or run a small local server (recommended, matches GitHub Pages):

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploying to GitHub Pages

1. Create a new GitHub repository (e.g. `portfolio` or `<username>.github.io`).
2. Push these files to it:
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio"
   git branch -M main
   git remote add origin https://github.com/<username>/<repo>.git
   git push -u origin main
   ```
3. On GitHub: **Settings → Pages → Build and deployment**. Set **Source** to
   "Deploy from a branch", choose the `main` branch and `/ (root)` folder, then **Save**.
4. Your site goes live at `https://<username>.github.io/<repo>/` within a minute or two.

> Tip: naming the repo `<username>.github.io` publishes it at `https://<username>.github.io/`
> (no subpath needed).
