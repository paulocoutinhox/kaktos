import json
import os
import shutil
import subprocess
from pathlib import Path

from markupsafe import Markup

from modules import config

FRONTEND_DIR = Path(config.root_dir) / "frontend"
DIST_DIR = FRONTEND_DIR / "dist"
MANIFEST_PATH = DIST_DIR / ".vite" / "manifest.json"
STATIC_PREFIX = "/static"

_manifest_cache = None


# -----------------------------------------------------------------------------
def _npm_executable() -> str:
    npm = shutil.which("npm")
    if npm is None:
        raise RuntimeError(
            "npm was not found in environement path, install node.js to build the site"
        )
    return npm


# -----------------------------------------------------------------------------
def _ensure_frontend_dependencies(npm: str) -> None:
    marker = FRONTEND_DIR / "node_modules" / "vite" / "package.json"
    if marker.is_file():
        return
    result = subprocess.run(
        [npm, "install", "--no-fund", "--no-audit"],
        cwd=FRONTEND_DIR,
        env=os.environ,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "frontend npm install failed:\n" f"{result.stdout}\n{result.stderr}"
        )


# -----------------------------------------------------------------------------
def clear_manifest_cache() -> None:
    global _manifest_cache

    _manifest_cache = None


# -----------------------------------------------------------------------------
def get_manifest() -> dict:
    global _manifest_cache

    from modules import system

    if system.is_debug():
        _manifest_cache = None

    if _manifest_cache is not None:
        return _manifest_cache

    if not MANIFEST_PATH.is_file():
        raise FileNotFoundError(
            f"vite manifest not found at {MANIFEST_PATH} because the frontend build must complete before generating pages"
        )

    _manifest_cache = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return _manifest_cache


# -----------------------------------------------------------------------------
def _static_href(relative_path: str) -> str:
    normalized = relative_path.replace("\\", "/")
    return f"{STATIC_PREFIX}/{normalized}"


# -----------------------------------------------------------------------------
def _entry_by_name(manifest: dict, entry_name: str) -> dict:
    for data in manifest.values():
        if data.get("isEntry") and data.get("name") == entry_name:
            return data
    raise KeyError(f"no vite entry named {entry_name!r} in manifest.json")


def _manifest_is_entries(manifest: dict) -> list[dict]:
    """Rollup input entries (isEntry). Excludes dynamic-only chunks."""
    entries = [v for v in manifest.values() if v.get("isEntry")]
    entries.sort(key=lambda e: (e.get("src") or "", e.get("name") or ""))
    return entries


# -----------------------------------------------------------------------------
class Frontend:
    """
    All user-facing static assets (css, js, images) live under frontend/public/
    and are emitted under STATIC_PREFIX (/static/…). Site root files (favicon, …)
    live under frontend/raw/ and are copied to the build root by publish_site_root().
    """

    static_prefix = STATIC_PREFIX

    def url(self, relative: str) -> str:
        s = relative.strip()
        if s.startswith("https://") or s.startswith("http://"):
            return s
        rel = s.lstrip("/")
        return f"{self.static_prefix}/{rel}"

    def abs_url(self, relative: str) -> str:
        s = relative.strip()
        if s.startswith("https://") or s.startswith("http://"):
            return s
        base = config.base_url.rstrip("/")
        return f"{base}{self.url(relative)}"

    def root_url(self, relative: str) -> str:
        rel = relative.strip().lstrip("/")
        return f"/{rel}"

    def styles_for(self, entry_name: str) -> Markup:
        manifest = get_manifest()
        entry = _entry_by_name(manifest, entry_name)
        parts = []
        for css in entry.get("css", []):
            href = _static_href(css)
            parts.append(f'<link rel="stylesheet" href="{href}">')
        return Markup("\n    ".join(parts))

    def script_for(self, entry_name: str) -> Markup:
        manifest = get_manifest()
        entry = _entry_by_name(manifest, entry_name)
        js = entry.get("file")
        if not js:
            return Markup("")
        href = _static_href(js)
        return Markup(f'<script type="module" src="{href}" defer></script>')

    def styles_all(self) -> Markup:
        manifest = get_manifest()
        seen: set[str] = set()
        parts: list[str] = []
        for entry in _manifest_is_entries(manifest):
            for css in entry.get("css", []):
                if css in seen:
                    continue
                seen.add(css)
                parts.append(f'<link rel="stylesheet" href="{_static_href(css)}">')
        return Markup("\n    ".join(parts))

    def scripts_all(self) -> Markup:
        manifest = get_manifest()
        parts: list[str] = []
        for entry in _manifest_is_entries(manifest):
            js = entry.get("file")
            if not js:
                continue
            href = _static_href(js)
            parts.append(f'<script type="module" src="{href}" defer></script>')
        return Markup("\n    ".join(parts))


# -----------------------------------------------------------------------------
def run_frontend_build() -> None:
    npm = _npm_executable()
    _ensure_frontend_dependencies(npm)
    result = subprocess.run(
        [npm, "exec", "--", "vite", "build"],
        cwd=FRONTEND_DIR,
        env=os.environ,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "frontend vite build failed:\n" f"{result.stdout}\n{result.stderr}"
        )
    clear_manifest_cache()


# -----------------------------------------------------------------------------
def publish_static_to_build() -> None:
    if not DIST_DIR.is_dir():
        raise FileNotFoundError(f"vite output directory missing: {DIST_DIR}")

    dest = Path(config.build_dir) / "static"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(DIST_DIR, dest)


# -----------------------------------------------------------------------------
def publish_site_root() -> None:
    raw = FRONTEND_DIR / "raw"
    if not raw.is_dir():
        return

    build = Path(config.build_dir)
    build.mkdir(parents=True, exist_ok=True)

    for entry in raw.iterdir():
        dest = build / entry.name
        if entry.is_file():
            shutil.copy2(entry, dest)
        elif entry.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(entry, dest)


api = Frontend()
