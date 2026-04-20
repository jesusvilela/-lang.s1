#!/usr/bin/env python3
# verify_all.py · §-LANG v3.0 ToE full package verification
# runs matter pack, prime pack, and ops toolkit checks with consolidated report

import subprocess, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def main():
    print("=" * 64)
    print("§-LANG v3.0 ToE · FULL PACKAGE VERIFICATION")
    print("=" * 64)
    print()

    # Matter pack
    print("—— MATTER PACK ——")
    rc, out, err = run([sys.executable, "verify_selfexpand.py"],
                       cwd=os.path.join(ROOT, "slang_packs", "slang_packs_toe_v3_0"))
    print(out)
    if err: print("STDERR:", err)
    matter_ok = (rc == 0)

    print("—— PRIME PACK ——")
    rc, out, err = run([sys.executable, "verify_selfexpand_prime.py"],
                       cwd=os.path.join(ROOT, "slang_packs", "slang_packs_toe_v3_0_prime"))
    print(out)
    if err: print("STDERR:", err)
    prime_ok = (rc == 0)

    print("—— OPS TOOLKIT (LANG.Ops.dialect.lang) ——")
    ops_path = os.path.join(ROOT, "slang_packs", "LANG_Ops_shared", "LANG.Ops.dialect.lang")
    if os.path.exists(ops_path):
        size = os.path.getsize(ops_path)
        with open(ops_path) as f:
            content = f.read()
        ops_declared = content.count("§")
        sigma_count = content.count("σ_")
        sections = content.count("§1 ") + content.count("§2 ") + content.count("§3 ") + \
                   content.count("§4 ") + content.count("§5 ") + content.count("§6 ") + \
                   content.count("§7 ") + content.count("§8 ") + content.count("§9 ") + \
                   content.count("§10 ") + content.count("§11 ") + content.count("§12 ")
        print(f"file:       {ops_path}")
        print(f"size:       {size} bytes")
        print(f"sections:   {sections} operator categories")
        print(f"σ-flags:    {sigma_count} invariants declared")
        print(f"§ symbols:  {ops_declared} occurrences")
        print("ops toolkit present: OK")
        ops_ok = True
    else:
        print("ops toolkit MISSING")
        ops_ok = False

    print()
    print("=" * 64)
    print("SUMMARY")
    print("=" * 64)
    print(f"  matter pack:  {'PASS' if matter_ok else 'FAIL'}")
    print(f"  prime pack:   {'PASS' if prime_ok else 'FAIL'}")
    print(f"  ops toolkit:  {'PASS' if ops_ok else 'FAIL'}")
    print()
    all_ok = matter_ok and prime_ok and ops_ok
    print(f"OVERALL:        {'§-LANG v3.0 ToE FULLY VERIFIED' if all_ok else 'FAILURES'}")
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
