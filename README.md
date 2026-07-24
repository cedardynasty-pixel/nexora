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

## Admin account

On first run, a default admin account is created automatically:
- Username: `admin`
- Password: `changeme123`

**Change this immediately** — log in, go to **Admin Panel → Manage Users → Reset a Password**,
and set a new password for `admin`. Or, better, override the defaults before first run via
Streamlit secrets (see `.streamlit/secrets.toml` example below):

```toml
ADMIN_USERNAME = "your_admin_username"
ADMIN_EMAIL = "you@example.com"
ADMIN_PASSWORD = "a-strong-password"
```

From the Admin Panel you can also: promote/demote other users to admin, create additional
admin accounts, delete accounts, and reset anyone's password.

## Book Library (admin) → grounded AI generations (students)

Admins manage books in **Admin Panel → Book Library**:
1. **Create a book** (just give it a title).
2. **Add chapters to it** one at a time — each chapter can come from its own PDF upload
   or pasted text, with its own title. This keeps content organized and lets students
   target a specific chapter instead of an entire textbook.

Students then see "Base this on a book" + "Chapter" dropdowns on every AI Study Tools tab.
Choosing a specific chapter feeds just that chapter's text to Gemini as grounding context;
choosing "Entire book" concatenates all its chapters (with the same keyword-relevance
excerpt-picking used for single chapters, so long books still fit within the prompt).

Notes:
- Only text-based PDFs work — scanned page images without OCR won't extract any text.
- Admin accounts don't see the AI Study Tools page themselves; that's a student-only
  feature. Admins manage books/chapters and the Gemini key instead.

## AI Study Tools (Gemini-powered, students only)

Students get a "AI Study Tools" page (visible once logged in) that generates notes,
practice worksheets, study plans, and flashcards using Google's Gemini API.

**Setup:**
1. Get a free API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. Log in as admin → **Admin Panel → Settings tab** → paste the key → **Save Key**.

That's the easiest path — no code or redeploy needed. Alternatively, set it as a
Streamlit secret instead (persists more reliably across app restarts):
```toml
GEMINI_API_KEY = "your-gemini-api-key"
```
The app checks the Admin-panel-stored key first, then falls back to this secret.

⚠️ **Never commit an API key to GitHub.** If you ever paste a key into a chat, file, or
commit by mistake, treat it as compromised — revoke it at aistudio.google.com/apikey and
generate a new one immediately.

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
