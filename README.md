# Nexora — Streamlit App

A Streamlit rebuild of the Nexora educational platform site (originally static HTML).
Includes Home, Courses, and About pages, plus working Login/Signup (SQLite-backed)
and a student Dashboard with progress tracking.

## Why a rebuild instead of a straight conversion?

Streamlit is a Python app framework — it can't run raw HTML/CSS/JS the way a browser
does with `index.html`. On top of that, the uploaded zip only contained the three
HTML files (`index.html`, `about.html`, `courses.html`); the `css/`, `js/`, and
`images/` folders it referenced weren't actually included. So there was no original
visual design to port — this recreates the same content and structure natively in
Streamlit, with a fresh look (`style.py`) inspired by the Nexora branding.

## Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Open the URL Streamlit prints (usually `http://localhost:8501`).

## Project structure

```
nexora_streamlit/
├── app.py              # Entry point — sets up navigation, loads pages
├── db.py               # SQLite persistence (users, enrollments)
├── auth.py             # Session-state login/logout helpers
├── style.py            # Shared CSS + reusable layout components
├── requirements.txt
├── views/
│   ├── home.py          # Landing page (hero, features, plans, newsletter)
│   ├── courses.py       # Course catalog (subjects, grades, learning paths)
│   ├── about.py         # Mission, vision, values, team
│   ├── login.py         # Login form
│   ├── signup.py        # Account creation form
│   └── dashboard.py     # Protected page: account info + course progress
└── data/
    └── nexora.db         # Created automatically on first run
```

## Notes on the auth system

- Passwords are hashed with PBKDF2-HMAC-SHA256 + a per-user random salt — never
  stored in plaintext.
- This is a **local demo-grade** auth system (SQLite file on disk, no HTTPS,
  no email verification, no rate limiting). It's fine for prototyping or a
  school project, but do not use it as-is for a real public-facing site with
  sensitive user data — you'd want a proper auth provider (e.g. Auth0, Supabase
  Auth, or Streamlit's own `st.login` with an OIDC provider) before going live.
- The dashboard's "Update Progress" control is a simple simulation so you can
  see progress bars move — it's not wired to real lesson content since none of
  the original course material was in the upload.

## Customizing

- **Colors/branding**: edit the CSS variables at the top of `style.py`
  (`--nexora-primary`, `--nexora-accent`, etc.).
- **Pricing/plans**: edit the plan cards directly in `views/home.py`.
- **Add a Contact page**: create `views/contact.py` following the same pattern
  as the other pages, then add it to the `pg = st.navigation(...)` call in `app.py`.
