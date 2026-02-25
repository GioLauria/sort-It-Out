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
    # Append release/version to the title when available
    try:
        ver = __version__
    except Exception:
        ver = "unknown"
    root.title(f"SortItOut — GUI (v{ver})")

    frm = ttk.Frame(root, padding=10)
    frm.grid(row=0, column=0, sticky="nsew")

    # Create a smaller font for the documentation viewer to avoid overly large text
    try:
        import tkinter.font as tkfont

        _docs_font = tkfont.nametofont("TkDefaultFont").copy()
        _docs_font.configure(size=max(_docs_font.cget("size") - 2, 8))
    except Exception:
        _docs_font = None

    # initial pixel size used for HTML rendering (can be adjusted by user)
    _docs_font_px = int(_docs_font.cget("size")) if _docs_font is not None else 12

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
    alg_menu_top = tk.Menu(menubar, tearoff=0)

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
    menubar.add_cascade(label="Algorithms", menu=alg_menu_top)
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

    def _load_algorithm_doc(name: str):
        """Load the markdown doc for algorithm `name` and display in the docs view."""
        try:
            repo_root = Path(__file__).resolve().parents[2]
            doc_paths = [
                repo_root / "docs" / "alghorythms" / f"{name.lower()}.md",
                repo_root / "docs" / f"{name.lower()}.md",
                repo_root / "docs" / "alghorythms" / "index.md",
            ]
            content = None
            for p in doc_paths:
                if p.exists():
                    content = p.read_text(encoding="utf-8")
                    break
            if content is None:
                if _MD_HTML_AVAILABLE:
                    try:
                        not_found_html = _wrap_html_small(
                            f"<pre>No documentation found for '{name}'.</pre>"
                        )
                        docs_view.set_html(not_found_html)
                    except Exception:
                        # fallback to plain text if HTMLLabel doesn't support set_html
                        docs_view.delete("1.0", "end")
                        msg1 = "No documentation found for '{}'.".format(name)
                        msg2 = "Searched: " + str(doc_paths)
                        docs_view.insert("1.0", msg1 + "\n" + msg2)
                else:
                    docs_view.delete("1.0", "end")
                    docs_view.insert(
                        "1.0",
                        f"No documentation found for '{name}'.\nSearched: {doc_paths}",
                    )
                return

            if _MD_HTML_AVAILABLE:
                try:
                    html = markdown.markdown(
                        content, extensions=["fenced_code", "tables"]
                    )
                except Exception:
                    html = markdown.markdown(content) if markdown else ""
                try:
                    _docs_state["html"] = html
                    docs_view.set_html(_wrap_html_small(html))
                except Exception:
                    # If set_html not available, replace widget with plain text view
                    docs_view.delete("1.0", "end")
                    docs_view.insert("1.0", content)
            else:
                docs_view.delete("1.0", "end")
                _docs_state["text"] = content
                docs_view.insert("1.0", content)
                docs_view.insert(
                    "end",
                    "\n\nInstall 'markdown' and 'tkhtmlview' to render formatted docs.",
                )
        except Exception as exc:
            if _MD_HTML_AVAILABLE:
                try:
                    docs_view.set_html(
                        _wrap_html_small(
                            f"<pre>Error loading docs for '{name}': {exc}</pre>"
                        )
                    )
                except Exception:
                    docs_view.delete("1.0", "end")
                    docs_view.insert("1.0", f"Error loading docs for '{name}': {exc}")
            else:
                docs_view.delete("1.0", "end")
                docs_view.insert("1.0", f"Error loading docs for '{name}': {exc}")

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

    # Documentation viewer on the right
    docs_frame = ttk.Frame(frm)
    docs_frame.grid(row=0, column=4, rowspan=9, sticky="nsew", padx=(12, 0))
    # Move font controls left of the label: Font size controls in cols 0-1
    docs_font_size_var = tk.IntVar(value=_docs_font_px)
    ttk.Label(docs_frame, text="Font size:").grid(row=0, column=0, sticky="e")
    docs_size_spin = tk.Spinbox(
        docs_frame,
        from_=8,
        to=36,
        width=4,
        textvariable=docs_font_size_var,
        justify="center",
    )
    docs_size_spin.grid(row=0, column=1, sticky="w", padx=(6, 0))
    ttk.Label(docs_frame, text="Item Details").grid(row=0, column=2, sticky="w")

    def _set_docs_font_size(val):
        nonlocal _docs_font_px, _docs_font, _docs_state
        try:
            size = int(val)
        except Exception:
            return
        _docs_font_px = size
        try:
            if _docs_font is not None:
                _docs_font.configure(size=size)
            # apply to current widget if present
            try:
                docs_view.configure(font=_docs_font)
            except Exception:
                pass
        except Exception:
            pass
        # Re-apply currently shown content with the new size
        try:
            if _MD_HTML_AVAILABLE and _docs_state.get("html"):
                docs_view.set_html(_wrap_html_small(_docs_state.get("html")))
            elif not _MD_HTML_AVAILABLE and _docs_state.get("text"):
                docs_view.delete("1.0", "end")
                docs_view.insert("1.0", _docs_state.get("text"))
        except Exception:
            pass

    # invoke when spinbox value changes
    docs_size_spin.configure(
        command=lambda: _set_docs_font_size(docs_font_size_var.get())
    )
    # If markdown rendering libs are missing, show install hint and button
    if not _MD_HTML_AVAILABLE:
        hint_frame = ttk.Frame(docs_frame)
        hint_frame.grid(row=0, column=1, sticky="e")
        ttk.Label(
            hint_frame, text="(Install markdown+tkhtmlview for formatted docs)"
        ).pack(side="left")

        def _install_md_pkgs():
            try:
                messagebox.showinfo(
                    "Install",
                    "Installing markdown and tkhtmlview. This may take a moment.",
                )
                args = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "markdown",
                    "tkhtmlview",
                ]
                subprocess.check_call(args)
                install_done_msg = (
                    "Installation complete. Please restart the application to "
                    "enable formatted docs."
                )
                messagebox.showinfo("Install", install_done_msg)
            except Exception as exc:
                messagebox.showerror("Install failed", str(exc))

        ttk.Button(hint_frame, text="Install", command=_install_md_pkgs).pack(
            side="left", padx=(6, 0)
        )
    # Create a content area. Use HTML rendering when available; otherwise Text fallback
    docs_content = ttk.Frame(docs_frame)
    docs_content.grid(row=1, column=0, sticky="nsew")
    if _MD_HTML_AVAILABLE:
        # HTMLLabel: attempt to apply font and wrap HTML on set
        docs_view = HTMLLabel(docs_content, html="", width=60)
        docs_view.grid(row=0, column=0, sticky="nsew")
        try:
            if _docs_font is not None:
                docs_view.configure(font=_docs_font)
        except Exception:
            pass
        try:
            docs_scroll = ttk.Scrollbar(
                docs_content, orient="vertical", command=docs_view.yview
            )
            docs_view.configure(yscrollcommand=docs_scroll.set)
            docs_scroll.grid(row=0, column=1, sticky="ns")
        except Exception:
            # HTMLLabel may not support yview; ignore scrollbar in that case
            pass
    else:
        docs_view = tk.Text(
            docs_content, height=30, width=60, wrap="word", font=_docs_font
        )
        docs_view.grid(row=0, column=0, sticky="nsew")
        docs_scroll = ttk.Scrollbar(
            docs_content, orient="vertical", command=docs_view.yview
        )
        docs_view.configure(yscrollcommand=docs_scroll.set)
        docs_scroll.grid(row=0, column=1, sticky="ns")

    time_label = ttk.Label(frm, text="Last sort: N/A")
    time_label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(6, 0))

    items_label = ttk.Label(frm, text="Items: 0")
    items_label.grid(row=7, column=2, columnspan=2, sticky="w", pady=(6, 0))

    # Initialize algorithm menu to show all algorithms
    _update_alg_menu_for([])

    # Populate the Algorithms top-level menu so users can open docs
    try:
        for name in sorted(ALGORITHMS.keys()):
            alg_menu_top.add_command(
                label=name, command=lambda n=name: _load_algorithm_doc(n)
            )
    except Exception:
        pass

    # Help menu with Help and Changelog entries
    help_menu = tk.Menu(menubar, tearoff=0)

    def _show_help():
        try:
            repo_root = Path(__file__).resolve().parents[2]
            p = repo_root / "README.md"
            if not p.exists():
                messagebox.showinfo("Help", "README.md not found in repository.")
                return
            content = p.read_text(encoding="utf-8")
            if _MD_HTML_AVAILABLE and markdown:
                html = markdown.markdown(content, extensions=["fenced_code", "tables"])
                try:
                    docs_view.set_html(_wrap_html_small(html))
                    return
                except Exception:
                    pass
            docs_view.delete("1.0", "end")
            docs_view.insert("1.0", content)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _show_changelog():
        try:
            repo_root = Path(__file__).resolve().parents[2]
            p = repo_root / "CHANGELOG.md"
            if not p.exists():
                messagebox.showinfo(
                    "Changelog", "CHANGELOG.md not found in repository."
                )
                return
            content = p.read_text(encoding="utf-8")
            if _MD_HTML_AVAILABLE and markdown:
                html = markdown.markdown(content, extensions=["fenced_code", "tables"])
                try:
                    docs_view.set_html(_wrap_html_small(html))
                    return
                except Exception:
                    pass
            docs_view.delete("1.0", "end")
            docs_view.insert("1.0", content)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    help_menu.add_command(label="Changelog", command=_show_changelog)
    help_menu.add_separator()
    help_menu.add_command(label="Help", command=_show_help)
    menubar.add_cascade(label="Help", menu=help_menu)

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

    btn_sort = ttk.Button(frm, text="Sort", command=do_sort)
    btn_sort.grid(row=6, column=0, sticky="w")
    btn_time = ttk.Button(frm, text="Time", command=do_time)
    btn_time.grid(row=6, column=1, sticky="w")
    btn_clear = ttk.Button(frm, text="Clear", command=do_clear)
    btn_clear.grid(row=6, column=2, sticky="w")

    root.mainloop()


if __name__ == "__main__":
    run_gui()
