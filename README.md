# XyraOS
A custom web-based operating system simulator.



XyraOS is a local Browser-based Operating System. Flask backend, HTML shell, virtual file system,
app store, games loaded from `assets/apps/`.

## Run

Double-click `run.bat`, or:

    pip install -r requirements.txt
    python app.py

Open http://127.0.0.1:8000/

## Layout

    app.py              Flask server
    requirements.txt    Python deps
    run.bat             Windows launcher
    templates/          index.html
    assets/             static files served at /assets/
      ready.flag        setup completion signal
      apps/             game HTML files
    data/               auto-created · state.json · fs.json

## Adding a game

Drop `<name>.html` into `assets/apps/`. Install it from the
Xyra App Store. It loads in a sandboxed iframe.

## Endpoints

    GET  /                    shell
    GET  /api/health          version ping
    GET  /api/ready           setup poll + game list
    GET  /api/games           installed games on disk
    GET  /api/state           profile (name, accent, wallpaper, installed)
    POST /api/state           save profile
    GET  /api/fs              virtual file system tree
    POST /api/fs              save VFS

# This project is ENTIRELY open sourced! If you feel free making drastic changes, rebranding, or ANYTHING, its okay! Feel free to do so! Just PLEASE add some sort of credits! (Example, the settings!)    
