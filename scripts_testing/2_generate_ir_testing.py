import os
import subprocess

C_SRC_DIR = "../c_testing"  # Folder containing test C files
IR_DIR = "../ir_testing"    # Folder to save IR files
CLANG_PATH = "C:/msys64/ucrt64/bin/clang.exe"

os.makedirs(IR_DIR, exist_ok=True)

for fname in os.listdir(C_SRC_DIR):
    if fname.endswith('.c'):
        c_path = os.path.join(C_SRC_DIR, fname)
        base_name = os.path.splitext(fname)[0]
        ir_path = os.path.join(IR_DIR, f"{base_name}.ll")
        try:
            subprocess.run([CLANG_PATH, "-S", "-emit-llvm", c_path, "-o", ir_path], check=True)
            print(f"✅ Generated IR for {fname}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate IR for {fname}: {e}")