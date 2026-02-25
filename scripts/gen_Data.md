# gen_data.py — usage guide

This file documents how to run the `gen_data.py` helper in `scripts/` to generate a newline-separated file of random integers.

Location
- `scripts/gen_data.py`

Purpose
- Quickly create test data files of integers for sorting and benchmarking.

Basic usage

Run the script with Python:

```bash
python scripts/gen_data.py
```

This writes 1000 random integers (one per line) to `data.txt` in the current directory.

Command-line options

- `-o`, `--output`  : output file path (default: `data.txt`)
- `-n`, `--count`   : number of integers to generate (default: `1000`)
- `--min`           : minimum integer (inclusive, default: `0`)
- `--max`           : maximum integer (inclusive, default: `1000000000`)

Examples

- Generate 10,000 integers to `sample.txt`:

```bash
python scripts/gen_data.py -o sample.txt -n 10000
```

- Generate 500 integers between 1 and 1000:

```bash
python scripts/gen_data.py -o small.txt -n 500 --min 1 --max 1000
```

- Use from PowerShell (same arguments):

```powershell
python scripts/gen_data.py -o data-pwsh.txt -n 5000
```

Integration notes

- The generated file is a plain text file with one integer per line and can be consumed by the CLI or GUI input (import the file in the GUI or pass the path to the CLI with `-i/--input` if implemented).
- For large files, ensure you have enough disk space — the script writes values line-by-line.

Troubleshooting

- If you get a permission error when writing to the target path, try running the command from a directory where you have write access or choose an output path under your user folder.
- The script uses Python's default pseudo-random generator; repeatable data can be added by modifying the script to seed with a fixed value if you need deterministic output.

Contact
- If you want the script to produce floats, CSV, or non-uniform distributions, I can extend `gen_data.py` — tell me which format you prefer.
