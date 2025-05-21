import os
import csv
import subprocess

LABELS_CSV = "../data/labels.csv"
IR_DIR = "../ir"
OPT_DIR = "../ir_optimized"
OPT_PATH = "C:/msys64/ucrt64/bin/opt.exe"

def run_opt_passes(ir_path, opt_path):
    subprocess.run([
        OPT_PATH,
        '-passes=loop-unroll,inline',
        ir_path,
        '-S',
        '-o', opt_path
    ], check=True)

def extract_instruction_features(opt_file_path):
    features = {
        'add': 0,
        'sub': 0,
        'mul': 0,
        'div': 0,
        'load': 0,
        'store': 0,
        'call': 0,
        'icmp': 0,
        'br': 0,
        'phi': 0,
        'ret': 0
    }

    with open(opt_file_path, 'r') as file:
        for line in file:
            for instr in features:
                if f" {instr} " in line:
                    features[instr] += 1

    return features

def main():
    if not os.path.exists(LABELS_CSV):
        print("❌ ERROR: Please run 1_generate_labels.py first.")
        return

    os.makedirs(OPT_DIR, exist_ok=True)

    with open(LABELS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    feature_rows = []
    for row in rows:
        c_file = row['file']
        base_name = os.path.splitext(os.path.basename(c_file))[0]
        ir_file = os.path.join(IR_DIR, f"{base_name}.ll")
        opt_path = os.path.join(OPT_DIR, f"{base_name}_opt.ll")

        if not os.path.exists(ir_file):
            print(f"⚠️ IR file not found: {ir_file}")
            continue

        try:
            run_opt_passes(ir_file, opt_path)
            features = extract_instruction_features(opt_path)
            features['label'] = row['label']
            feature_rows.append(features)
        except subprocess.CalledProcessError:
            print(f"⚠️ LLVM opt failed for: {ir_file}")
        except Exception as e:
            print(f"❌ Unexpected error with {ir_file}: {e}")

    if feature_rows:
        fieldnames = list(feature_rows[0].keys())
        with open('../data/features.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(feature_rows)
        print(f"✅ Saved features to ../data/features.csv with {len(feature_rows)} rows.")
    else:
        print("❌ No features extracted. Check for errors.")

if __name__ == "__main__":
    main()