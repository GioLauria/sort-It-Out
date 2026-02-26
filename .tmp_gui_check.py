import sys
from pathlib import Path

print("Python executable:", sys.executable)
try:
    import sort_it_out.gui as g

    gui_file = getattr(g, "__file__", None)
    print("gui __file__ =", gui_file)
    if gui_file:
        repo_root = Path(gui_file).resolve().parents[2]
        print("repo_root =", repo_root)
        print("repo_root/README.md exists =", (repo_root / "README.md").exists())
        print("repo_root/CHANGELOG.md exists =", (repo_root / "CHANGELOG.md").exists())
    print("cwd =", Path.cwd())
    print("cwd/README.md exists =", (Path.cwd() / "README.md").exists())
    print("cwd/CHANGELOG.md exists =", (Path.cwd() / "CHANGELOG.md").exists())
    try:
        import importlib.resources as pkg_res

        candidate = pkg_res.files("sort_it_out") / "README.md"
        print("pkg resource README candidate repr =", repr(candidate))
        try:
            print(
                "pkg candidate is_file =",
                getattr(candidate, "is_file", lambda: False)(),
            )
        except Exception as e:
            print("pkg candidate is_file error", e)
    except Exception as e:
        print("importlib.resources error", e)
except Exception as e:
    print("error importing gui:", e)
