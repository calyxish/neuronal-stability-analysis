"""
analysis.py
-----------
Reproduce all numerical results from the paper in one script.

    Eigenvalue Analysis of Neuronal Firing Stability
    in a Two-Dimensional Linear Dynamical System

Author : Kwakye Ishmael Affum
GitHub : https://github.com/calyxish
Email  : kwakyeishmael07@gmail.com

Usage
-----
    python analysis.py

Outputs
-------
    Console : eigenvalue table for each system
    figures/ : all four publication figures
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import numpy as np
from simulation import stability_info

SYSTEMS = {
    "Stable Node":          np.array([[-1.0,  0.0], [ 0.0, -2.0]]),
    "Stable Oscillatory":   np.array([[-1.0,  2.0], [-2.0, -1.0]]),
    "Unstable Oscillatory": np.array([[ 0.5,  2.0], [-2.0,  0.5]]),
    "Unstable Node":        np.array([[ 1.0,  0.0], [ 0.0,  2.0]]),
}

SEP = "─" * 68

def print_report():
    print(f"\n{SEP}")
    print("  NEURONAL STABILITY ANALYSIS  —  Kwakye Ishmael Affum")
    print(f"{SEP}\n")

    for name, A in SYSTEMS.items():
        info = stability_info(A)
        ev   = info["eigenvalues"]
        print(f"  [{name}]")
        print(f"    Matrix A          : {A.tolist()}")
        print(f"    Trace             : {info['trace']:.4f}")
        print(f"    Determinant       : {info['determinant']:.4f}")
        print(f"    Eigenvalue 1      : {ev[0].real:.4f} {ev[0].imag:+.4f}i")
        print(f"    Eigenvalue 2      : {ev[1].real:.4f} {ev[1].imag:+.4f}i")
        print(f"    Classification    : {info['label']}")
        print(f"    Stable            : {info['stable']}")
        print(f"    Oscillatory       : {info['oscillatory']}")
        print()

    print(f"{SEP}\n")


if __name__ == "__main__":
    print_report()
    print("Generating figures …")
    # delegate to generate_figures.py
    import subprocess
    subprocess.run([sys.executable, "generate_figures.py"], check=True)
    print("Done.  See figures/ directory.")
