import os
import subprocess
import pandas as pd

C_SRC_DIR = "../c_sources"
TMP_DIR = "../tmp_ir"
CLANG_PATH = "C:/msys64/ucrt64/bin/clang.exe"
OPT_LEVELS = ['0', '1', '2', '3']
OUTPUT_CSV = "../data/labels.csv"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def compile_and_count(c_file):
    counts = {}
    base_name = os.path.basename(c_file).replace('.c', '')

    for level in OPT_LEVELS:
        tmp_ll = os.path.join(TMP_DIR, f"{base_name}_O{level}.ll")
        try:
            subprocess.run([
                CLANG_PATH,
                c_file,
                '-S',
                '-emit-llvm',
                f'-O{level}',
                '-o',
                tmp_ll
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            with open(tmp_ll, 'r') as f:
                ir_text = f.read()

            instr_count = sum(1 for line in ir_text.splitlines()
                              if line.strip() and not line.strip().startswith(';'))
            counts[f'O{level}'] = instr_count
        except subprocess.CalledProcessError:
            counts[f'O{level}'] = -1  # Flag error case

    return counts

def main():
    ensure_dir(TMP_DIR)

    data = []

    for fname in os.listdir(C_SRC_DIR):
        if not fname.endswith('.c'):
            continue

        c_path = os.path.join(C_SRC_DIR, fname)
        instr_counts = compile_and_count(c_path)

        # Skip file if any level failed
        if any(v == -1 for v in instr_counts.values()):
            print(f"⚠️ Skipping {fname} due to compile error.")
            continue

        # Find the optimization level with minimum instructions
        best_opt = min(instr_counts, key=instr_counts.get)
        row = {
            'file': fname,
            **instr_counts,
            'label': best_opt
        }
        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Saved labels to {OUTPUT_CSV} with {len(df)} rows.")

if __name__ == "__main__":
    main()