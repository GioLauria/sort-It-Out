# install_hooks.py

Purpose
- Install a local git hook shim (`.git/hooks/pre-push`) that invokes the repository's `scripts/local_pre_push.py` logic.

Usage
- Run once after cloning to install the hook locally:

```bash
python scripts/install_hooks.py
```

What it does
- Writes an executable file to `.git/hooks/pre-push` that runs `scripts/local_pre_push.py` with the Python interpreter.

Notes
- This is a local convenience — hooks are not versioned in `.git/hooks` and other developers should run this after cloning.
- The script checks for `.git/hooks` and will error when not run in a git repository.
