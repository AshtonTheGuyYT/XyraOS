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
      appicons/         custom app icons (see below)
    data/               auto-created · state.json · fs.json

## Adding a game

Drop `<name>.html` into `assets/apps/`. Install it from the
Xyra App Store. It loads in a sandboxed iframe.

If the game needs an input box to receive keyboard focus, the shell
already patches `Event.prototype.preventDefault` and
`Event.prototype.stopImmediatePropagation` inside the iframe so
typing works even in aggressive games.

## Endpoints

    GET  /                    shell
    GET  /api/health          version ping
    GET  /api/ready           setup poll + game list
    GET  /api/games           installed games on disk
    GET  /api/state           profile (name, accent, wallpaper, installed)
    POST /api/state           save profile
    GET  /api/fs              virtual file system tree
    POST /api/fs              save VFS
    GET  /api/appicons        case-insensitive app-icon index

---

# Customization

Everything in XyraOS is stored in the browser's `localStorage` under
two keys:

    xyra.win10.state.v5    profile · accent · wallpaper · clock · installed
    xyra.fs.v5             the entire virtual file system

Use the **reset** button in the dev badge (bottom-right, appears only when
localStorage is blocked) or clear site data to wipe everything.

## 1. Profile name

**Settings → System → Display name**

Changes the name shown on the lock screen, the Start menu footer, and
the home folder path (`C:/Users/<name>/`). The VFS automatically
migrates your files if you rename.

## 2. Profile picture

**Settings → Personalization → Profile picture → Upload…**

Pick any PNG/JPG/GIF/WebP from your computer. Stored as a base64 data
URL in `localStorage`, so it survives reloads. **Reset** clears it back
to the first letter of your name.

## 3. Accent color

**Settings → Personalization → Accent color**

Eight presets. Affects the taskbar underline, buttons, dock running
indicator, focus rings, the lock-screen avatar gradient, and the
particle background.

The Terminal can also change it live:

    color #ff6b9d

Any 6-digit hex works. Invalid values are rejected.

## 4. Wallpaper

**Settings → System → Wallpaper**

Six built-in themes:

| Name       | Look                                              |
|------------|---------------------------------------------------|
| `deep`     | Default blue radial                              |
| `pressure` | Purple/magenta deep-space                        |
| `surface`  | Teal/cyan underwater                             |
| `ember`    | Warm dark ember                                  |
| `aurora`   | Multi-stop aurora gradient                       |
| `void`     | Pure black                                       |

The animated particle canvas and the gradient layer are two separate
elements — the wallpaper only changes the gradient. Particles
automatically tint to match your accent color.

## 5. 12-hour / 24-hour clock

**Settings → Time & Language → 24-hour clock**

Toggle **On** / **Off**. When off, times render as `1:30 PM`; when on,
as `13:30`. Applies instantly to:

- Lock screen clock
- Tray clock
- Clock app
- Terminal `time` command
- Notification timestamps

On first run, XyraOS **auto-detects** your preference from your
browser's locale (US users default to 12-hour, most others to 24-hour).

The clock always reads your **device's real local time and timezone** —
`Settings → Time & Language` shows your detected timezone and locale
for verification.

## 6. App icons (case-insensitive)

XyraOS looks for icons in `assets/appicons/`. Filenames must match the
**app id** (which is the same as the `.html` filename for games, or the
key in `APP_DEFS` for built-ins).

Supported extensions, in priority order:

    png  >  svg  >  webp  >  gif  >  jpg  >  jpeg

**Case does not matter.** All of these resolve to the same icon:

    assets/appicons/snake.png
    assets/appicons/Snake.PNG
    assets/appicons/SNAKE.svg
    assets/appicons/sNaKe.webp

The Flask backend exposes `/api/appicons`, which lists the real
filenames on disk and returns a lowercased lookup table. The client
then matches every app id with `.toLowerCase()`. On `file://` (no
server), the client falls back to probing four casings directly.

### Built-in app ids

    thispc  recycle  browser  notepad  terminal  calc  music
    taskmgr  settings  store  photos  clock

### Store app ids (seed catalogue)

    snake  tetris  game2048  pong  minesweeper  breakout  flappy  tictactoe

### Example

Drop `assets/appicons/snake.png` → the App Store card, Start Menu
tile, taskbar entry, and window title bar all swap from 🐍 to your
image, without any code changes.

Click **↻ Rescan games** in the App Store after adding or renaming
files to pick up new icons without a page reload.

## 7. Adding custom games

1. Drop `<name>.html` into `assets/apps/`.
2. (Optional) Drop `<name>.png` into `assets/appicons/`.
3. Open the **App Store** and click **↻ Rescan games**.
4. Click **Install** — it now appears in your Start Menu.
5. (Optional) Add a desktop icon by editing `templates/index.html`
   inside `<div class="desktop-icons">`:

       <div class="desk-icon" data-app="myname">
         <div class="ico" data-icon-id="myname">🎮</div>
         <div class="lbl">My Game</div>
       </div>

## 8. Importing and downloading files

The File Explorer (This PC, or any folder) has a toolbar with:

- **📁 New** — create a folder
- **⬆ Import** — pick files from your real computer
- **⬇ Download** — save the selected file back to your computer
- **🗑** — delete the selected file

Images are stored as data URLs (so they persist). Text files are
stored as plain text. Both work with the Download button — a Blob is
created on the fly and the browser handles the save dialog.

## 9. Photos app

The Photos app (desktop icon, dock, Start menu) has its own **Import**
button for the `Pictures` folder. Double-clicking any image in File
Explorer opens it in Photos.

When opening a single photo, the app shows a **white loading screen
with a pulsing 🖼️ icon** for ~450 ms before fading in the real image,
so it never flashes white on slow imports.

## 10. Installing / uninstalling apps

**App Store → Install** adds a game to your Start Menu. **Settings →
Apps → Uninstall** removes it. The list is stored as `installed[]` in
state.

## 11. Password

Set during first-time setup. Stored in plain text in `localStorage` —
this is a simulator, not a real OS. Leave it blank to skip the password
prompt entirely.

## 12. Developer reset

When `localStorage` is blocked (e.g. opening `index.html` directly
from disk), a green dev badge appears in the bottom-right corner with a
**reset** button that wipes all `xyra.*` keys and reloads.

---

# Credits

XyraOS · Built by AshtonAI · Shell by XyraAI

This project is **ENTIRELY open sourced!** If you feel like making
drastic changes, rebranding, or anything else — it's okay! Feel free
to do so! Just **please add some sort of credits** somewhere visible
(example: the Settings → About pane).
