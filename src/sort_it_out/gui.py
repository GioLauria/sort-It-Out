"""Simple Tkinter GUI for SortItOut.

This provides a lightweight graphical interface to enter data, choose an
algorithm and view the sorted output or timing results.
"""
from __future__ import annotations

import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .algorithms import ALGORITHMS, ALGORITHMS_LOWER
from .sorts import time_sort


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
    root.title("SortItOut — GUI")

    frm = ttk.Frame(root, padding=10)
    frm.grid(row=0, column=0, sticky="nsew")

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
        # update items count
        try:
            count = len(_parse_input(content))
        except Exception:
            count = 0
        items_label.config(text=f"Items: {count}")

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

    repeat_var = tk.IntVar(value=3)
    ttk.Label(frm, text="Repeat (for timing):").grid(row=2, column=2, sticky="w")
    repeat_entry = ttk.Entry(frm, textvariable=repeat_var, width=6)
    repeat_entry.grid(row=2, column=3, sticky="w")

    output_label = ttk.Label(frm, text="Output:")
    output_label.grid(row=3, column=0, sticky="w", pady=(8, 0))
    output_text = tk.Text(frm, height=10, width=60)
    output_text.grid(row=4, column=0, columnspan=3, pady=(2, 8))
    output_scroll = ttk.Scrollbar(frm, orient="vertical", command=output_text.yview)
    output_text.configure(yscrollcommand=output_scroll.set)
    output_scroll.grid(row=4, column=3, sticky="ns", pady=(2, 8))

    time_label = ttk.Label(frm, text="Last sort: N/A")
    time_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=(6, 0))

    items_label = ttk.Label(frm, text="Items: 0")
    items_label.grid(row=6, column=2, columnspan=2, sticky="w", pady=(6, 0))

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

    btn_sort = ttk.Button(frm, text="Sort", command=do_sort)
    btn_sort.grid(row=5, column=0, sticky="w")
    btn_time = ttk.Button(frm, text="Time", command=do_time)
    btn_time.grid(row=5, column=1, sticky="w")
    btn_clear = ttk.Button(frm, text="Clear", command=do_clear)
    btn_clear.grid(row=5, column=2, sticky="w")

    root.mainloop()


if __name__ == "__main__":
    run_gui()
