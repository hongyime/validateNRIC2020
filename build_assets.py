"""Expose the existing Flask assets through Vercel's static CDN."""
from pathlib import Path
from shutil import copytree


def build_assets() -> None:
    root = Path(__file__).resolve().parent
    # Keep the original assets for Flask development and existing URLs.
    # Vercel serves public/static/* directly, without invoking the app.
    copytree(root / 'static', root / 'public' / 'static', dirs_exist_ok=True)


if __name__ == '__main__':
    build_assets()
