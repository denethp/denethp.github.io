# denethp.github.io

Personal portfolio site for **Deneth Priyadarshana** — Electronic & Telecommunication Engineering undergraduate at the University of Moratuwa, focused on robotics, embedded systems, computer vision and control systems.

Live at: https://denethp.github.io

## Structure

```
index.html              Single-page site (Home, About, Education, Projects, Skills, Experience, Contact)
assets/css/style.css     Styles (dark, technical theme)
assets/js/main.js        Scroll reveal, project filtering, nav highlighting
assets/img/profile.jpg   Profile photo
assets/files/            Downloadable CV (PDF)
```

## Editing

This is a static site — no build step. Edit `index.html` / `assets/css/style.css` / `assets/js/main.js` directly and refresh. To preview locally:

```
python3 -m http.server 8000
```

then open `http://localhost:8000`.

## Deploying

Since this repo is named `denethp.github.io`, GitHub Pages serves it automatically from the `main` branch root — just commit and push:

```
git add .
git commit -m "Update portfolio"
git push
```
