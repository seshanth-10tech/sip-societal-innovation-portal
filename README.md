# Samaj Setu — Societal Innovation Portal

Samaj Setu connects community-reported challenges with university teams whose areas of work may fit. Citizens can describe a challenge, review a five-step analysis, see a suggested first approach and college match, then choose whether to submit the challenge. University accounts can review assigned reports and post progress updates.

The project brief and team presentation are in [`docs/SIH 1.pptx`](docs/SIH%201.pptx).

## Run locally

Requirements: Python 3.10 or newer and pip.

Run these commands from the repository root.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). The SQLite database is created automatically beside `database.py` the first time the app runs. Keep the database file on persistent storage if you host the app; it is deliberately excluded from Git.

For a long-lived deployment, copy `.env.example` to `.env` and set a fresh `SECRET_KEY`. Local runs work without extra configuration.

## Demo university accounts

These accounts are included for local demonstration and appear on the sign-in page. They are public demo credentials and must be replaced before deploying with real users or real community data.

| Institution | Username | Password |
| --- | --- | --- |
| NIT Jamshedpur | `nitjsr` | `nit123` |
| BIT Sindri | `bitsindri` | `bit123` |
| BIT Mesra | `bitmesra` | `bit123` |
| Birsa Agricultural University | `bau` | `bau123` |
| GEC Palamu | `gecpalamu` | `gec123` |
| Birsa Institute of Technology | `birsa` | `birsa123` |

## How challenge matching works

`ai_engine.py` uses a local keyword and domain ruleset. It estimates a priority, recommends relevant expertise and a first-step approach, then scores the colleges in its sample directory. The five-second review is a user-facing sequence of those stages; it is not a remote AI service. College locations, focus areas, and match scores are demonstration data, not official contact or accreditation details.

## Configuration and deployment

Set a unique `SECRET_KEY` in the environment for any long-lived deployment. Local runs generate a temporary key automatically. `FLASK_DEBUG` enables debug mode only when set to `1`, `true`, or `yes`; leave it unset in production. The built-in Flask server is for local development. On a Linux host, install the requirements and run a production WSGI server, for example:

```bash
gunicorn --bind 0.0.0.0:${PORT:-8000} app:app
```

Use persistent disk storage for SQLite and replace the sample university credentials with a real authentication system before exposing this demo to the public. Do not collect sensitive personal information until production security, privacy, and access controls are in place.

## Repository contents

- `app.py` — Flask routes and session handling
- `ai_engine.py` — local challenge classification and college matching rules
- `database.py` — SQLite persistence and university-scoped report updates
- `templates/` and `static/` — portal, citizen, and university interfaces
- `docs/` — the original project presentation
