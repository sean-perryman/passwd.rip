# passwd.rip

A tiny password generator website + CLI endpoint designed for deployment on Railway.

## Features

- Dark-mode friendly UI
- Click password to copy to clipboard
- Refresh icon fetches a new password via AJAX
- Passwords are generated on demand and **not stored**
- CLI-friendly output:
  - `curl https://passwd.it` returns **one password + newline** (auto-detected)
  - `curl https://passwd.it/raw` always returns plain text
  - `curl https://passwd.it/api/password` returns JSON

## Password format

Default format:
- **Capitalized English word** (first letter uppercase, rest lowercase)
- **1 or 2 digits**
- **1 symbol** (no percent sign)

Example: `Foxhall!26`

## Run locally (no Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open: http://localhost:8080

Test CLI output:

```bash
curl -s http://localhost:8080
curl -s http://localhost:8080/raw
curl -s http://localhost:8080/api/password
```

## Run locally with Docker

```bash
docker build -t passwd-it .
docker run --rm -p 8080:8080 passwd-it
```

## Deploy to Railway

1. Create a GitHub repo and push this project.
2. In Railway: **New Project → Deploy from GitHub Repo**
3. Railway will detect the `Dockerfile` automatically.
4. Add your custom domain: `passwd.it`

## Notes

- `/` returns raw text for terminal-like clients (curl/wget/httpie) and HTML for browsers.
- `/raw` exists for guaranteed plain text output.
