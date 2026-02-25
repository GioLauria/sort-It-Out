**Building Executables (Windows & Linux)**

This document explains how contributors can create standalone executables for Sort It Out using PyInstaller. It covers Windows native builds, Linux builds (WSL or native), and an example Dockerfile for reproducible Linux builds.

**Prerequisites**
- Python 3.8+ installed for the target platform.
- A clean virtual environment for building.
- The project sources (repository root).
- Optional: Docker (for containerized Linux builds).

**Why use PyInstaller**
- PyInstaller bundles Python, modules, and extension libraries into a single executable file. It is simple and widely used for Python CLIs and GUI apps.

**Common notes**
- Build on the target OS (Windows builds on Windows; Linux builds on Linux/WSL/Docker). Cross-building with PyInstaller is not supported reliably.
- If the project uses Tkinter for the GUI, make sure the Python installation on the build machine includes Tcl/Tk (standard on most official installers).
- Test the produced binary on a clean machine or VM to verify all runtime files are bundled.

**1. Create a tiny launcher**
Create a small launcher module that imports the packaged CLI entrypoint. Add the file `src/launcher.py` with the following contents:

```python
from sort_it_out import cli
import sys

if __name__ == "__main__":
    raise SystemExit(cli.main())
```

This file gives PyInstaller a clear module to freeze.

**2. Windows: build a single-file EXE (recommended on Windows)**
1. Open PowerShell and create/activate a venv in the repo root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e . pyinstaller
```

2. Run PyInstaller to make a one-file exe:

```powershell
pyinstaller --onefile --name sortItOut --console src\launcher.py
# output executable: dist\sortItOut.exe
```

Notes:
- Use `--windowed` instead of `--console` if you want no console window (GUI-only).
- If your system Python was installed from the Microsoft Store, prefer an official CPython installer to avoid packaging issues.

**3. Linux: build native ELF (WSL or native Linux recommended)**
Using WSL (Ubuntu) is convenient on Windows:

```bash
# inside WSL or on Linux
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e . pyinstaller
pyinstaller --onefile --name sortItOut --console src/launcher.py
# output artifact: dist/sortItOut
```

Docker (reproducible build): create a `Dockerfile` like this:

```dockerfile
FROM python:3.11-slim
WORKDIR /src
COPY . /src
RUN python -m pip install --upgrade pip && pip install -e . pyinstaller
RUN pyinstaller --onefile --name sortItOut --console src/launcher.py
```

Build and extract the artifact:

```bash
docker build -t sortitout-builder .
CONTAINER=$(docker create sortitout-builder)
docker cp $CONTAINER:/src/dist/sortItOut ./dist/sortItOut
docker rm $CONTAINER
```

**4. Signing / Notarization**
- Windows: sign the EXE with an Authenticode certificate (recommended for distribution). Use `signtool.exe` or CI secrets.
- Linux: optionally GPG-sign the file or provide checksums (SHA256) to consumers.

**5. Troubleshooting**
- Missing modules at runtime: build with `--log-level=DEBUG` to get PyInstaller analysis details and add hidden imports via `--hidden-import` or by editing a `spec` file.
- Tkinter runtime error: ensure the Python used to build includes the same Tcl/Tk libraries; avoid minimal/stripped images that lack Tcl/Tk.
- Large exe size: `--onefile` packs everything. To produce a folder build instead, remove `--onefile` and distribute the `dist/<name>/` directory.

**6. Example CI job (Linux) using Docker**
Add a GitHub Actions job step (simplified):

```yaml
jobs:
  build-exe-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image and extract binary
        run: |
          docker build -t sortitout-builder .
          CONTAINER=$(docker create sortitout-builder)
          docker cp $CONTAINER:/src/dist/sortItOut ./dist/sortItOut
          docker rm $CONTAINER
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: sortItOut-linux
          path: dist/sortItOut
```

**7. Quick checklist for contributors**
- [ ] Create and activate a venv on the target platform.
- [ ] Install `pip install -e . pyinstaller`.
- [ ] Add `src/launcher.py` if not present.
- [ ] Run `pyinstaller --onefile --name sortItOut --console src/launcher.py`.
- [ ] Test the produced binary on a clean environment/VM.
- [ ] (Optional) Sign the binary and produce checksums.

**8. Advanced notes**
- If you need Windows installer (MSI/NSIS), build the EXE first and then use NSIS or WiX to wrap it.
- For reproducible builds, pin Python version, PyInstaller version, and build inside a container that you control.

If you want, I can:
- Add `src/launcher.py` to the repo now and commit it, or
- Add a small `docs/` README snippet into `CONTRIBUTING.md` linking to this guide, or
- Create a sample GitHub Actions workflow that builds and uploads binaries for a tagged release.
