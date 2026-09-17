# Manish Kanwar — Textile & CAD Designer Portfolio

A production-ready Django portfolio, blog and lightweight CMS for a textile
and CAD designer. Built as a self-contained Django project so the client
never has to touch code to add a project, write an article, or update the
homepage.

## Stack

- **Backend:** Django 5, PostgreSQL (SQLite for local dev by default)
- **Frontend:** Django templates, vanilla CSS (custom design system, no
  build step) and vanilla JS (sticky nav, mobile menu, image lightbox)
- **Static/media:** WhiteNoise for static files; local `/media/` in dev,
  a persistent volume or object storage in production
- **Deployment:** Docker image that runs Gunicorn; ready for Render
  (`render.yaml`) or any Docker-capable VPS (`docker-compose.yml`)

## Project layout

```
config/            Django project settings, root urls, sitemaps
apps/
  core/            Site settings, homepage content, social links, process
                   steps, testimonials, contact & hire forms
  portfolio/       Category, Tag, Project, ProjectImage — the case-study
                   portfolio pages
  profiles/        Experience, Skill, Service — About/Experience/Services
  blog/            BlogCategory, BlogPost
templates/         All HTML templates
static/            main.css (design system) + main.js (nav/lightbox)
```

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                 # defaults work out of the box (SQLite)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `/admin/` for the studio
dashboard.

### First-time content setup (no coding required)

1. Log in to `/admin/`.
2. Open **Site Settings** and **Homepage Settings** — fill in contact
   details, hero copy and images.
3. Add one or more **Categories** under Portfolio (e.g. "Surface Pattern
   Design"), each with a cover image.
4. Add a **Project**, assign it to a category, and use the inline image
   table on the same page to upload 4–5 images (set an *Image type* like
   Main Design / Motif / Repeat for each — this drives the "Design
   Breakdown" section automatically).
5. Fill in **Design Information** (technique, application, software, etc.)
   — only fields you fill in are shown on the page.
6. Tick **Published** and save. The project now appears on the site.
7. Repeat for **Experience**, **Services**, and **Blog Posts**.

## Environment variables

See `.env.example` for the full list. Nothing sensitive is hard-coded —
`SECRET_KEY`, database credentials and email credentials are all read from
the environment.

## Production

```bash
# Docker Compose (VPS / Hostinger)
cp .env.example .env   # fill in real production values
docker compose up -d --build

# Render
# Push to a Git repo and use render.yaml as the Blueprint — it provisions
# a Postgres database and a Docker web service automatically.
```

Either path runs `migrate`, `collectstatic` and starts Gunicorn
automatically (see `Dockerfile`).

## What's included vs. what to build next

This first delivery covers the full data model, the public site (home,
work/category/project pages with search, filtering, pagination and an
image lightbox, about, experience, services, blog, contact, hire), SEO
fundamentals (per-page meta tags, Open Graph, JSON-LD, `sitemap.xml`,
`robots.txt`), basic spam protection, email notification hooks, and a
Docker/Render/VPS-ready deployment setup — all wired to Django's admin,
customized with inline image galleries, list-editable publishing flags and
autocomplete/search so it's usable without touching code.

Reasonable next phases, not yet built:

- A fully custom, Hostinger-style dashboard UI in place of Django admin
  (current admin is functional and non-technical-friendly, but not
  visually restyled)
- Automated image variants (WebP/AVIF, multiple sizes, `srcset`)
- An automated test suite
- Redirect management and a scheduled/queued blog publish job

## Commands reference

```bash
python manage.py migrate            # apply database migrations
python manage.py createsuperuser    # create your admin login
python manage.py collectstatic      # bundle static files for production
python manage.py runserver          # local dev server
```
