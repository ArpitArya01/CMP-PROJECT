import os
import subprocess

C_SRC_DIR = "../c_sources"
IR_DIR = "../ir"
CLANG_PATH = "C:/msys64/ucrt64/bin/clang.exe"

os.makedirs(IR_DIR, exist_ok=True)

for fname in os.listdir(C_SRC_DIR):
    if fname.endswith('.c'):
        c_path = os.path.join(C_SRC_DIR, fname)
        base_name = os.path.splitext(fname)[0]
        ir_path = os.path.join(IR_DIR, f"{base_name}.ll")
        try:
            subprocess.run([
                CLANG_PATH,
                c_path,
                '-S',
                '-emit-llvm',
                '-O0',
                '-o', ir_path
            ], check=True)
            print(f"✅ Generated {ir_path}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to compile {c_path}")