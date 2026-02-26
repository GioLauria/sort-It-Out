"""Simple Tkinter GUI for SortItOut.

This provides a lightweight graphical interface to enter data, choose an
algorithm and view the sorted output or timing results.
"""
from __future__ import annotations

import subprocess
import sys
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from . import __version__
from .algorithms import ALGORITHMS, ALGORITHMS_LOWER
from .sorts import time_sort

# Optional markdown -> HTML rendering support
try:
    import markdown
    from tkhtmlview import HTMLLabel

    _MD_HTML_AVAILABLE = True
except Exception:
    markdown = None
    HTMLLabel = None
    _MD_HTML_AVAILABLE = False


def _parse_value(s: str):
    s = s.strip()
    if s == "":
        return s
    try:
        return int(s)
    except Exception:
        pass
    try:
        return float(s)
    except Exception:
        return s


def _parse_input(text: str):
    # Accept newline- or comma-separated values
    parts = [p for line in text.splitlines() for p in line.split(",")]
    return [_parse_value(p) for p in parts if p.strip() != ""]


def run_gui():
    root = tk.Tk()
    # Append release/version to the title when available. Use a small
    # polling loop that re-reads the package _version.py so the title
    # updates dynamically if the version file changes on disk.
    def _read_version_from_file() -> str:
        try:
            ver_path = Path(__file__).resolve().parent / "_version.py"
            txt = ver_path.read_text(encoding="utf-8")
            import re

            m = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", txt)
            if m:
                return m.group(1)
        except Exception:
            pass
        try:
            return __version__
        except Exception:
            return "unknown"

    ver = _read_version_from_file()
    root.title(f"SortItOut — GUI (v{ver})")

    # periodically refresh the title if the version file changes
    def _refresh_title():
        try:
            v2 = _read_version_from_file()
            current = root.title()
            # root.title() returns the full string; update only if different
            desired = f"SortItOut — GUI (v{v2})"
            if current != desired:
                root.title(desired)
        except Exception:
            pass
        try:
            root.after(5000, _refresh_title)
        except Exception:
            # if after is unavailable, ignore
            pass

    try:
        root.after(5000, _refresh_title)
    except Exception:
        pass

    frm = ttk.Frame(root, padding=10)
    frm.grid(row=0, column=0, sticky="nsew")
    # Ensure root expands so child frames can stretch
    try:
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
    except Exception:
        pass
    # Ensure input and output text rows expand so the docs frame's bottom
    # lines up with the `Items` label row when the window is resized.
    frm.grid_rowconfigure(1, weight=1)
    frm.grid_rowconfigure(5, weight=1)
    frm.grid_columnconfigure(0, weight=1)
    frm.grid_columnconfigure(4, weight=1)

    # Create a smaller font for the documentation viewer to avoid overly large text
    try:
        import tkinter.font as tkfont

        _docs_font = tkfont.nametofont("TkDefaultFont").copy()
        _docs_font.configure(size=max(_docs_font.cget("size") - 2, 8))
    except Exception:
        _docs_font = None

    # fixed pixel size used for HTML rendering (fixed to 8)
    _docs_font_px = 8
    if _docs_font is not None:
        try:
            _docs_font.configure(size=_docs_font_px)
        except Exception:
            pass

    def _wrap_html_small(html: str) -> str:
        # Wrap rendered HTML in a div that reduces base font-size for better readability
        if not html:
            return html
        return f'<div style="font-size:{_docs_font_px}px;line-height:1.2">{html}</div>'

    # keep track of the last-displayed content so we can re-render when the font changes
    _docs_state = {"html": "", "text": ""}

    # Menu: File -> Import, (separator), Exit
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)

    def _import_file():
        path = filedialog.askopenfilename(
            title="Import data file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except Exception as exc:
            messagebox.showerror("Import error", str(exc))
            return
        input_text.delete("1.0", "end")
        input_text.insert("1.0", content)
        # update items count and algorithm menu
        try:
            parsed = _parse_input(content)
            count = len(parsed)
        except Exception:
            parsed = []
            count = 0
        items_label.config(text=f"Items: {count}")
        _update_alg_menu_for(parsed)

    def _exit_app():
        root.quit()

    file_menu.add_command(label="Import", command=_import_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=_exit_app)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    ttk.Label(frm, text="Input (one value per line or comma-separated):").grid(
        row=0, column=0, sticky="w"
    )
    input_text = tk.Text(frm, height=10, width=60)
    input_text.grid(row=1, column=0, columnspan=3, pady=(2, 8))
    input_scroll = ttk.Scrollbar(frm, orient="vertical", command=input_text.yview)
    input_text.configure(yscrollcommand=input_scroll.set)
    input_scroll.grid(row=1, column=3, sticky="ns", pady=(2, 8))

    def _on_input_modified(event=None):
        # Update items count live when the Text widget is modified
        try:
            txt = input_text.get("1.0", "end")
            count = len(_parse_input(txt))
            items_label.config(text=f"Items: {count}")
            _update_alg_menu_for(_parse_input(txt))
        except Exception:
            items_label.config(text="Items: 0")
        finally:
            # Reset the modified flag to continue receiving events
            try:
                input_text.edit_modified(False)
            except Exception:
                pass

    # Bind to the Text modified virtual event so the count updates as user types/pastes
    input_text.bind("<<Modified>>", lambda e: _on_input_modified())

    # Algorithm label + selector inline
    alg_frame = ttk.Frame(frm)
    alg_frame.grid(row=2, column=0, columnspan=2, sticky="w")
    ttk.Label(alg_frame, text="Algorithm:").pack(side="left")
    # Default to the canonical first algorithm name (capitalized)
    default_alg = next(iter(sorted(ALGORITHMS.keys())), "Merge")
    alg_var = tk.StringVar(value=default_alg)
    alg_menu = ttk.OptionMenu(
        alg_frame, alg_var, default_alg, *sorted(ALGORITHMS.keys())
    )
    alg_menu.pack(side="left", padx=(6, 0))

    def _supported_algorithms_for(data_list):
        """Return list of algorithm names (capitalized keys) that support data."""
        if not data_list:
            return list(sorted(ALGORITHMS.keys()))

        # Determine types present
        has_str = any(isinstance(x, str) for x in data_list)
        has_int = any(isinstance(x, int) and not isinstance(x, bool) for x in data_list)
        has_float = any(isinstance(x, float) for x in data_list)

        # Mixed strings and numbers are not comparable in Python3
        if has_str and (has_int or has_float):
            return []

        allowed = []
        for name, func in ALGORITHMS.items():
            lname = name.lower()
            if lname in ("counting", "radix"):
                # integer-only algorithms
                if has_int and not has_float and not has_str:
                    allowed.append(name)
            elif lname == "bucket":
                # bucket expects floats in [0,1)
                if not has_str and (has_float or has_int):
                    # check values are floats in [0,1)
                    try:
                        vals = [float(x) for x in data_list]
                    except Exception:
                        continue
                    if vals and all(0.0 <= v < 1.0 for v in vals):
                        allowed.append(name)
            else:
                # comparison-based algorithms: require homogeneous comparable types
                if has_str and not (has_int or has_float):
                    allowed.append(name)
                elif (has_int or has_float) and not has_str:
                    allowed.append(name)
        return sorted(allowed)

    def _update_alg_menu_for(data_list):
        menu = alg_menu["menu"]
        menu.delete(0, "end")
        allowed = _supported_algorithms_for(data_list)
        if not allowed:
            menu.add_command(label="(no supported algorithms)", state="disabled")
            alg_var.set("")
            return
        for name in allowed:
            menu.add_command(label=name, command=lambda v=name: alg_var.set(v))
        # If current selection is not allowed, set to the first allowed
        if alg_var.get() not in allowed:
            alg_var.set(allowed[0])

    # Documentation loading removed — GUI focuses on sorting only.

    repeat_var = tk.IntVar(value=3)
    # Move Repeat controls to align with input/output columns (left side)
    ttk.Label(frm, text="Repeat (for timing):").grid(row=3, column=0, sticky="w")
    repeat_entry = ttk.Entry(frm, textvariable=repeat_var, width=6)
    # place the entry so its right edge aligns with the input/output area
    repeat_entry.grid(row=3, column=2, sticky="e")

    output_label = ttk.Label(frm, text="Output:")
    output_label.grid(row=4, column=0, sticky="w", pady=(8, 0))
    output_text = tk.Text(frm, height=10, width=60)
    output_text.grid(row=5, column=0, columnspan=3, pady=(2, 8))
    output_scroll = ttk.Scrollbar(frm, orient="vertical", command=output_text.yview)
    output_text.configure(yscrollcommand=output_scroll.set)
    output_scroll.grid(row=5, column=3, sticky="ns", pady=(2, 8))

    # Documentation / item details area removed — GUI now focuses on sorting only.

    time_label = ttk.Label(frm, text="Last sort: N/A")
    time_label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(6, 0))

    items_label = ttk.Label(frm, text="Items: 0")
    # Align the right edge of the items count with the Clear button (same column)
    items_label.grid(row=7, column=2, sticky="e", pady=(6, 0))

    # Defer populating algorithm menu entries so the main window appears quickly.
    def _init_algorithm_menus():
        try:
            _update_alg_menu_for([])
        except Exception:
            pass

    # Schedule menu population once the UI is idle to avoid startup delay
    try:
        root.after_idle(_init_algorithm_menus)
    except Exception:
        _init_algorithm_menus()

    # Help / changelog removed — simplified UI for sorting only.

    def do_sort():
        txt = input_text.get("1.0", "end")
        data = _parse_input(txt)
        items_label.config(text=f"Items: {len(data)}")
        alg_raw = alg_var.get()
        alg = ALGORITHMS.get(alg_raw) or ALGORITHMS_LOWER.get(alg_raw.lower())
        if alg is None:
            messagebox.showerror("Error", f"Unknown algorithm: {alg_raw}")
            return
        try:
            t0 = time.perf_counter()
            res = alg(data)
            t1 = time.perf_counter()
            elapsed = t1 - t0
        except Exception as exc:
            messagebox.showerror("Error while sorting", str(exc))
            return
        output_text.delete("1.0", "end")
        output_text.insert("1.0", "\n".join(str(x) for x in res))
        time_label.config(text=f"Last sort: {elapsed:.6f} sec")

    def do_time():
        txt = input_text.get("1.0", "end")
        data = _parse_input(txt)
        items_label.config(text=f"Items: {len(data)}")
        alg_raw = alg_var.get()
        alg = ALGORITHMS.get(alg_raw) or ALGORITHMS_LOWER.get(alg_raw.lower())
        if alg is None:
            messagebox.showerror("Error", f"Unknown algorithm: {alg_raw}")
            return
        display_name = next((n for n, f in ALGORITHMS.items() if f is alg), alg_raw)
        try:
            rep = int(repeat_var.get())
        except Exception:
            rep = 3
        try:
            t = time_sort(alg, data, repeat=rep)
        except Exception as exc:
            messagebox.showerror("Error while timing", str(exc))
            return
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"{display_name}: {t:.6f} sec (avg over {rep} runs)")
        time_label.config(text=f"Last timed: {t:.6f} sec (avg)")

    def do_clear():
        """Clear both input and output text areas and reset counters."""
        try:
            input_text.delete("1.0", "end")
        except Exception:
            pass
        try:
            output_text.delete("1.0", "end")
        except Exception:
            pass
        items_label.config(text="Items: 0")
        time_label.config(text="Last sort: N/A")
        _update_alg_menu_for([])

    # Group Sort and Time so they remain adjacent regardless of column widths
    action_frame = ttk.Frame(frm)
    action_frame.grid(row=6, column=0, sticky="w")
    btn_sort = ttk.Button(action_frame, text="Sort", command=do_sort)
    btn_sort.pack(side="left")
    btn_time = ttk.Button(action_frame, text="Time", command=do_time)
    btn_time.pack(side="left", padx=(6, 0))

    # Keep Clear aligned to the right edge of the output column
    btn_clear = ttk.Button(frm, text="Clear", command=do_clear)
    btn_clear.grid(row=6, column=2, sticky="e")

    root.mainloop()


if __name__ == "__main__":
    run_gui()
