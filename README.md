# openbitly

A simple URL shortener. Paste a long URL, get a short code back, and every visit
to that code is recorded so you can see how many times a link was clicked.

- **Backend** — Django, exposing a small JSON API plus the redirect endpoint.
- **Frontend** — React (Vite), a single-page dashboard to create and list links.
- **Storage** — SQLite.
- **Deployment** — Docker Compose with Gunicorn behind Caddy.

<img width="1229" height="386" alt="image" src="https://github.com/user-attachments/assets/2ed7715b-6d63-490c-a5d9-e0e2720dec6c" />

> **Note: ** Since this is a take-home, I committed straight
> to `main` to keep a clean, linear, easy-to-review history. In a real project
> I'd use short-lived feature branches behind pull requests
> A few other things I'd add in production but left
> out of scope here:
>
> - **Accounts + per-user ownership** instead of the localStorage-only scoping.
> - **Postgres** once there are concurrent writers or multiple app instances.
> - **Rate limiting / abuse protection** on the shorten endpoint.
> - **Automated backups + a CI/CD deploy pipeline** rather than a manual
>   `docker compose up`.

## API

| Method | Path            | Description                                              |
| ------ | --------------- | -------------------------------------------------------- |
| `POST` | `/api/shorten`  | Create a short link. Body: `{ "url": "https://..." }`.   |
| `GET`  | `/api/links?codes=a,b` | List the given codes' links (the browser's own), with click counts. |
| `GET`  | `/<code>`       | Redirect (302) to the original URL and record the click. |

## Project layout

```
backend/    Django project (shortener app, API, redirect view, tests)
frontend/   React + Vite single-page app, plus the Caddyfile
docker-compose.yml   app (Gunicorn) + Caddy
```

## Design decisions

- **Clicks live in their own table, not a counter column.** Each visit is a row
  in `Click` (timestamp, referer, user agent) with a foreign key to the link.
  This keeps a full history for later analytics instead of a lossy running total.
- **Clicks are recorded synchronously in the redirect view.** Fine at current
  traffic; if the redirect path gets hot, the insert should move onto a queue so
  it stays off the request's critical path.
- **Short codes are random base62, not sequential IDs.** Codes are generated
  randomly and checked for collisions, so they aren't guessable or enumerable.
- **Redirects use 302, not 301.** A permanent redirect would be cached by
  browsers and we'd stop seeing repeat clicks.
- **Self-host URLs are rejected.** Shortening a URL that points back at this
  service would create a redirect loop.
- **Caddy serves the React build and proxies the API.** One origin in front of
  everything: static SPA at `/`, API/admin proxied to Django, and any other path
  treated as a short code and forwarded to the redirect view.
- **"My links" is a per-browser list, not accounts.** The browser keeps the
  codes it created in `localStorage`; the database is the source of truth and a
  link is never deleted by the client. Clearing `localStorage` only empties that
  browser's dashboard — the links still resolve. Cross-device history would need
  accounts.


## Run locally

Clone the repo:

```bash
git clone <repo-url>
cd openbitly
```

### With Docker (closest to production)

```bash
docker compose up --build
```

The app is then served by Caddy at <http://localhost>.

### Without Docker (for development)

Run the backend and frontend in two terminals.

**Backend** (Django on `:8000`):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend** (Vite dev server on `:5173`, proxies `/api` to Django):

```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:5173>.

## Tests

```bash
cd backend
python manage.py test
```
