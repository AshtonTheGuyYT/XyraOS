#!/usr/bin/env python3
"""
Windows 10 - Xyra Edition · Flask backend
Serves the shell, exposes /assets for games + ready.flag,
persists state and the virtual file system to data/.
Also serves /api/appicons for case-insensitive app-icon lookup.
"""

import json
import os
from pathlib import Path
from flask import Flask, render_template, jsonify, request

BASE_DIR   = Path(__file__).resolve().parent
DATA_DIR   = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
APPICONS   = ASSETS_DIR / "appicons"
APPS_DIR   = ASSETS_DIR / "apps"
STATE_FILE = DATA_DIR / "state.json"
FS_FILE    = DATA_DIR / "fs.json"

DATA_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
APPS_DIR.mkdir(exist_ok=True)
APPICONS.mkdir(exist_ok=True)

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(ASSETS_DIR),
    static_url_path="/assets",
)
app.config["JSON_SORT_KEYS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True


def _read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _write_json(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


# ------------------------------------------------------------------ routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({"ok": True, "edition": "XyraOS",
                    "version": "1.0.0"})


@app.route("/api/ready")
def ready():
    """Backend signal — mirrors /assets/ready.flag."""
    flag  = ASSETS_DIR / "ready.flag"
    games = sorted(p.stem for p in APPS_DIR.glob("*.html")) if APPS_DIR.exists() else []
    return jsonify({
        "ready":  flag.exists(),
        "games":  games,
        "assets": str(ASSETS_DIR),
    })


@app.route("/api/state", methods=["GET", "POST"])
def state():
    if request.method == "GET":
        return jsonify(_read_json(STATE_FILE, {}))
    data = request.get_json(silent=True) or {}
    _write_json(STATE_FILE, data)
    return jsonify({"ok": True})


@app.route("/api/fs", methods=["GET", "POST"])
def fs():
    if request.method == "GET":
        return jsonify(_read_json(FS_FILE, {}))
    data = request.get_json(silent=True) or {}
    _write_json(FS_FILE, data)
    return jsonify({"ok": True})


@app.route("/api/games")
def games_list():
    if not APPS_DIR.exists():
        return jsonify({"games": []})
    return jsonify({"games": [
        {"id": p.stem, "file": f"assets/apps/{p.name}"}
        for p in sorted(APPS_DIR.glob("*.html"))
    ]})


@app.route("/api/appicons")
def appicons_list():
    """Case-insensitive icon index.

    Returns {"icons": {lowercased_name: "assets/appicons/RealName.ext"}}.

    The client lowercases the app id when looking up, so files named
    Snake.png, SNAKE.PNG, sNaKe.SvG all resolve to app id "snake".

    If two files share a name but different extensions, the one with the
    higher-priority extension wins (png > svg > webp > gif > jpg > jpeg).
    """
    priority = [".png", ".svg", ".webp", ".gif", ".jpg", ".jpeg"]
    icons = {}   # lowercased_name -> (relative_url, priority_index)

    if APPICONS.is_dir():
        try:
            for fn in os.listdir(APPICONS):
                full = APPICONS / fn
                if not full.is_file():
                    continue
                name, ext = os.path.splitext(fn)
                ext = ext.lower()
                if ext not in priority:
                    continue
                key  = name.lower()
                prio = priority.index(ext)
                # keep the highest-priority extension for each key
                if key not in icons or prio < icons[key][1]:
                    # url-encode the filename so spaces / odd chars survive
                    from urllib.parse import quote
                    rel = "assets/appicons/" + quote(fn)
                    icons[key] = (rel, prio)
        except OSError as e:
            app.logger.warning("appicons scan failed: %s", e)

    return jsonify({"icons": {k: v[0] for k, v in icons.items()}})


@app.errorhandler(404)
def spa_fallback(e):
    return render_template("index.html"), 200


# ------------------------------------------------------------------- boot

if __name__ == "__main__":
    host = os.environ.get("XYRA_HOST", "127.0.0.1")
    port = int(os.environ.get("XYRA_PORT", 8000))
    print()
    print("  ┌──────────────────────────────────────────────┐")
    print("  │  XyraOS · v1.0.0                             │")
    print("  │  Built by AshtonAI · Shell by XyraAI         │")
    print("  └──────────────────────────────────────────────┘")
    print(f"   URL     http://{host}:{port}/")
    print(f"   Assets  {ASSETS_DIR}")
    print(f"   Icons   {APPICONS}")
    print(f"   Data    {DATA_DIR}")
    print()
    app.run(host=host, port=port, debug=True, use_reloader=True)