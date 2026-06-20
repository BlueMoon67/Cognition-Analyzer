# Docker setup for `basic/` (PREDICTION + traffic-map)

Drop these files into your existing `basic/` folder at the matching paths, then run from `basic/`:

```
basic/
├── docker-compose.yml          <- new
├── PREDICTION/
│   ├── Dockerfile              <- new
│   ├── .dockerignore           <- new
│   └── ...(your existing files)
└── traffic-map/
    ├── Dockerfile              <- new
    ├── nginx.conf              <- new
    ├── .dockerignore           <- new
    ├── src/App.jsx             <- replace with App.jsx.patched (see below)
    └── ...(your existing files)
```

## What changed in App.jsx

Your `fetch("http://localhost:5000/traffic")` was hardcoded. I changed it to:

```js
fetch(`${import.meta.env.VITE_API_URL || "http://localhost:5000"}/traffic`)
```

This still defaults to `localhost:5000` for normal `npm run dev`, but lets Docker
override it at build time via `VITE_API_URL` (set in `docker-compose.yml`).
Rename/copy `traffic-map/App.jsx.patched` over `traffic-map/src/App.jsx`.

## Run it

```bash
cd basic
docker compose up --build
```

- Backend (Flask, `/traffic` endpoint): http://localhost:5000/traffic
- Frontend (map UI): http://localhost:5173

First build will be slow — it installs scikit-learn/pandas/numpy for the backend
and npm installs + builds the Vite app for the frontend. Subsequent builds are
cached unless you change `requirements.txt`/`package.json`.

## Notes / things worth knowing

- **`.env` file**: `docker-compose.yml` loads `PREDICTION/.env` (your `WEATHER_API`
  and `TRAFFIC_API` keys) via `env_file`. Nothing is baked into the image — if you
  rotate keys, just edit `.env` and restart (`docker compose up -d`).
- **`traffic.db` persistence**: mounted as a bind volume so predictions written by
  `main.py` (or anything else) survive container restarts and stay editable from
  the host.
- **`training_model/` excluded from the build**: it's ~150MB of notebooks/raw CSVs
  not needed to *run* the app, so it's skipped via `.dockerignore` to keep builds
  fast. Nothing on your filesystem is deleted.
- **`server.py` only serves `/traffic` (read-only)** — it does NOT run `main.py`'s
  scheduler that actually generates new predictions. If you want predictions to
  keep refreshing, you have two options:
  1. Run `python main.py` manually/separately (on host or in a second container —
     ask and I'll add a `scheduler` service to compose for this), or
  2. Treat the current `traffic.db` as a static snapshot for demo purposes.
- **Flask dev server runs with `debug=True`** in `server.py` as in your source —
  fine for a hackathon demo, but not meant for real production exposure.
- **Frontend → backend networking**: the React app runs in the *browser*, not
  inside the Docker network, so it must reach the backend via a host-mapped port
  (`localhost:5000`), not the Docker service name `backend`. That's why
  `VITE_API_URL` defaults to `http://localhost:5000` rather than
  `http://backend:5000`.
