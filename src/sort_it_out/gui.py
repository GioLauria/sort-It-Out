"""Simple Tkinter GUI for SortItOut.

This provides a lightweight graphical interface to enter data, choose an
algorithm and view the sorted output or timing results.
"""
from __future__ import annotations

import time
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, List

from . import (
    bubble_sort,
    bucket_sort,
    cocktail_sort,
    comb_sort,
    counting_sort,
    gnome_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    radix_sort,
    selection_sort,
    shell_sort,
)
from .sorts import time_sort

ALGORITHMS: dict[str, Callable[[List], List]] = {
    "bubble": bubble_sort,
    "quick": quick_sort,
    "merge": merge_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "heap": heap_sort,
    "shell": shell_sort,
    "counting": counting_sort,
    "radix": radix_sort,
    "bucket": bucket_sort,
    "comb": comb_sort,
    "cocktail": cocktail_sort,
    "gnome": gnome_sort,
}


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

    ttk.Label(frm, text="Input (one value per line or comma-separated):").grid(
        row=0, column=0, sticky="w"
    )
    input_text = tk.Text(frm, height=10, width=60)
    input_text.grid(row=1, column=0, columnspan=3, pady=(2, 8))

    ttk.Label(frm, text="Algorithm:").grid(row=2, column=0, sticky="w")
    alg_var = tk.StringVar(value="merge")
    alg_menu = ttk.OptionMenu(frm, alg_var, "merge", *sorted(ALGORITHMS.keys()))
    alg_menu.grid(row=2, column=1, sticky="w")

    repeat_var = tk.IntVar(value=3)
    ttk.Label(frm, text="Repeat (for timing):").grid(row=2, column=2, sticky="w")
    repeat_entry = ttk.Entry(frm, textvariable=repeat_var, width=6)
    repeat_entry.grid(row=2, column=3, sticky="w")

    output_label = ttk.Label(frm, text="Output:")
    output_label.grid(row=3, column=0, sticky="w", pady=(8, 0))
    output_text = tk.Text(frm, height=10, width=60)
    output_text.grid(row=4, column=0, columnspan=4, pady=(2, 8))

    time_label = ttk.Label(frm, text="Last sort: N/A")
    time_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=(6, 0))

    def do_sort():
        txt = input_text.get("1.0", "end")
        data = _parse_input(txt)
        alg_name = alg_var.get()
        alg = ALGORITHMS.get(alg_name)
        if not alg:
            messagebox.showerror("Error", f"Unknown algorithm: {alg_name}")
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
        alg_name = alg_var.get()
        alg = ALGORITHMS.get(alg_name)
        if not alg:
            messagebox.showerror("Error", f"Unknown algorithm: {alg_name}")
            return
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
        output_text.insert("1.0", f"{alg_name}: {t:.6f} sec (avg over {rep} runs)")
        time_label.config(text=f"Last timed: {t:.6f} sec (avg)")

    btn_sort = ttk.Button(frm, text="Sort", command=do_sort)
    btn_sort.grid(row=5, column=0, sticky="w")
    btn_time = ttk.Button(frm, text="Time", command=do_time)
    btn_time.grid(row=5, column=1, sticky="w")

    root.mainloop()


if __name__ == "__main__":
    run_gui()
