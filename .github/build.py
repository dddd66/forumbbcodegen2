import PyInstaller.__main__
from pathlib import Path
import os

assets = [
    f"{p}{os.pathsep}assets"
    for p in Path("assets").rglob("*")
    if p.is_file()
]

PyInstaller.__main__.run([
    "src/main.py",
    "--onefile",
    "--windowed",
    "--name", "mkobbcode",
    "--icon", "assets/favicon.ico",
    *[arg for p in assets for arg in ("--add-data", p)],
])