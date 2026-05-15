"""
generate_figures.py
-------------------
Produce all publication-quality figures for the research paper:

    "Eigenvalue Analysis of Neuronal Firing Stability in a
     Two-Dimensional Linear Dynamical System"

Author : Kwakye Ishmael Affum
GitHub : https://github.com/calyxish
Email  : kwakyeishmael07@gmail.com

Run
---
    python generate_figures.py

Outputs (saved to figures/)
---------------------------
    fig1_phase_portraits.png
    fig2_time_series.png
    fig3_stability_map.png
    fig4_eigenvalue_locus.png
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe
from simulation import simulate, stability_info

# ── global aesthetics ────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family"      : "serif",
    "font.size"        : 11,
    "axes.linewidth"   : 1.2,
    "axes.spines.top"  : False,
    "axes.spines.right": False,
    "xtick.direction"  : "in",
    "ytick.direction"  : "in",
    "figure.dpi"       : 150,
    "savefig.dpi"      : 200,
    "savefig.bbox"     : "tight",
})

COLORS = {
    "stable"    : "#2C7BB6",
    "oscillatory": "#1A9641",
    "unstable"  : "#D7191C",
    "neutral"   : "#756BB1",
}

OUT = "figures"
os.makedirs(OUT, exist_ok=True)

X0 = np.array([1.0, 0.0])

SYSTEMS = [
    {
        "label" : "Stable Node",
        "A"     : np.array([[-1.0,  0.0],
                             [ 0.0, -2.0]]),
        "color" : COLORS["stable"],
        "ls"    : "-",
    },
    {
        "label" : "Stable Oscillatory",
        "A"     : np.array([[-1.0,  2.0],
                             [-2.0, -1.0]]),
        "color" : COLORS["oscillatory"],
        "ls"    : "-",
    },
    {
        "label" : "Unstable Oscillatory",
        "A"     : np.array([[ 0.5,  2.0],
                             [-2.0,  0.5]]),
        "color" : COLORS["unstable"],
        "ls"    : "--",
    },
    {
        "label" : "Unstable Node",
        "A"     : np.array([[ 1.0,  0.0],
                             [ 0.0,  2.0]]),
        "color" : "#E67E22",
        "ls"    : ":",
    },
]

# ── Figure 1: Phase Portraits ─────────────────────────────────────────────────
def fig1_phase_portraits():
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()

    for ax, sys in zip(axes, SYSTEMS):
        info = stability_info(sys["A"])
        T    = 6.0 if "Unstable" not in sys["label"] else 2.5
        traj = simulate(sys["A"], X0, dt=0.005, T=T)

        ax.plot(traj[:, 0], traj[:, 1],
                color=sys["color"], lw=1.8, label=sys["label"])
        ax.plot(*X0, "o", color="black", ms=5, zorder=5)

        # arrow to show direction
        mid = len(traj) // 4
        ax.annotate("",
            xy    =(traj[mid+5, 0], traj[mid+5, 1]),
            xytext=(traj[mid,   0], traj[mid,   1]),
            arrowprops=dict(arrowstyle="->", color=sys["color"], lw=1.5))

        ev   = info["eigenvalues"]
        estr = (f"λ = {ev[0].real:.2f}{ev[0].imag:+.2f}i,\n"
                f"    {ev[1].real:.2f}{ev[1].imag:+.2f}i")
        ax.text(0.97, 0.97, estr,
                transform=ax.transAxes, fontsize=8.5,
                va="top", ha="right",
                bbox=dict(boxstyle="round,pad=0.3", fc="white",
                          ec=sys["color"], alpha=0.85))

        ax.set_title(sys["label"], fontsize=11, fontweight="bold",
                     color=sys["color"])
        ax.set_xlabel("Membrane Potential  V", fontsize=9)
        ax.set_ylabel("Recovery Variable  W", fontsize=9)
        ax.axhline(0, color="grey", lw=0.6, ls="--", alpha=0.5)
        ax.axvline(0, color="grey", lw=0.6, ls="--", alpha=0.5)
        ax.grid(alpha=0.15)

    fig.suptitle("Figure 1 — Phase Portraits of Neuronal System Dynamics",
                 fontsize=12, fontweight="bold", y=1.01)
    fig.tight_layout()
    path = f"{OUT}/fig1_phase_portraits.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")


# ── Figure 2: Time Series ─────────────────────────────────────────────────────
def fig2_time_series():
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=False)
    axes = axes.flatten()

    for ax, sys in zip(axes, SYSTEMS):
        T = 8.0 if "Unstable" not in sys["label"] else 2.0
        traj = simulate(sys["A"], X0, dt=0.005, T=T)
        t    = np.linspace(0, T, len(traj))

        ax.plot(t, traj[:, 0], color=sys["color"],  lw=1.8, label="V (potential)")
        ax.plot(t, traj[:, 1], color=sys["color"],  lw=1.2,
                ls="--", alpha=0.7, label="W (recovery)")
        ax.set_title(sys["label"], fontsize=11, fontweight="bold",
                     color=sys["color"])
        ax.set_xlabel("Time (s)", fontsize=9)
        ax.set_ylabel("Amplitude", fontsize=9)
        ax.legend(fontsize=8, framealpha=0.6)
        ax.grid(alpha=0.15)

    fig.suptitle("Figure 2 — Temporal Evolution of Neuronal State Variables",
                 fontsize=12, fontweight="bold", y=1.01)
    fig.tight_layout()
    path = f"{OUT}/fig2_time_series.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")


# ── Figure 3: Trace–Determinant Stability Map ─────────────────────────────────
def fig3_stability_map():
    tr_vals  = np.linspace(-3, 3, 600)
    det_vals = np.linspace(-1, 5, 600)
    TR, DET  = np.meshgrid(tr_vals, det_vals)

    # discriminant  Δ = Tr² - 4 Det
    disc = TR**2 - 4 * DET

    # region codes
    region = np.zeros_like(TR)
    region[(DET > 0) & (TR < 0) & (disc >= 0)] = 1   # stable node
    region[(DET > 0) & (TR < 0) & (disc <  0)] = 2   # stable spiral
    region[(DET > 0) & (TR > 0) & (disc >= 0)] = 3   # unstable node
    region[(DET > 0) & (TR > 0) & (disc <  0)] = 4   # unstable spiral
    region[DET < 0]                              = 5   # saddle
    region[np.abs(TR) < 0.01]                   = 6   # centre (approx)

    cmap = matplotlib.colors.ListedColormap([
        "#CCCCCC",   # 0 boundary
        "#AED6F1",   # 1 stable node
        "#2C7BB6",   # 2 stable spiral
        "#F1948A",   # 3 unstable node
        "#D7191C",   # 4 unstable spiral
        "#F9E79F",   # 5 saddle
        "#1A9641",   # 6 centre
    ])

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.pcolormesh(TR, DET, region, cmap=cmap, shading="auto",
                       vmin=0, vmax=6, alpha=0.85)

    # parabola Δ=0
    tr_pos = tr_vals[tr_vals >= 0]
    tr_neg = tr_vals[tr_vals <= 0]
    ax.plot(tr_pos,  tr_pos**2 / 4, "k--", lw=1.2, label=r"$\Delta = 0$")
    ax.plot(tr_neg,  tr_neg**2 / 4, "k--", lw=1.2)
    ax.axhline(0, color="black", lw=0.8)
    ax.axvline(0, color="black", lw=0.8)

    # annotate regions
    annotations = [
        ( 1.5, 3.5, "Unstable\nSpiral",   "#D7191C"),
        (-1.8, 3.5, "Stable\nSpiral",     "#2C7BB6"),
        ( 1.5, 0.3, "Unstable\nNode",     "#E74C3C"),
        (-1.8, 0.3, "Stable\nNode",       "#1A5276"),
        ( 0.0,-0.5, "Saddle",             "#7D6608"),
        ( 0.0, 0.05,"Centre",             "#1A9641"),
    ]
    for x, y, txt, col in annotations:
        ax.text(x, y, txt, ha="center", va="center", fontsize=9,
                color=col, fontweight="bold",
                bbox=dict(fc="white", ec="none", alpha=0.6, pad=1.5))

    # mark our three systems
    markers = [
        ("Stable Node",       SYSTEMS[0]["A"], "^", COLORS["stable"]),
        ("Stable Oscillatory",SYSTEMS[1]["A"], "o", COLORS["oscillatory"]),
        ("Unstable Osc.",     SYSTEMS[2]["A"], "s", COLORS["unstable"]),
    ]
    for mlabel, A, mk, col in markers:
        tr  = np.trace(A)
        det = np.linalg.det(A)
        ax.plot(tr, det, mk, color=col, ms=9, zorder=10,
                label=mlabel, mec="black", mew=0.8)

    ax.set_xlabel("Trace  (a + d)", fontsize=11)
    ax.set_ylabel("Determinant  (ad − bc)", fontsize=11)
    ax.set_title("Figure 3 — Stability Map in Trace–Determinant Space",
                 fontsize=12, fontweight="bold")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.8)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-1, 5)
    ax.grid(alpha=0.2)

    fig.tight_layout()
    path = f"{OUT}/fig3_stability_map.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")


# ── Figure 4: Eigenvalue Locus in Complex Plane ───────────────────────────────
def fig4_eigenvalue_locus():
    fig, ax = plt.subplots(figsize=(7, 6))

    # sweep 'a' (diagonal entry) while keeping off-diagonals fixed
    b, c = 2.0, -2.0
    a_range = np.linspace(-2.5, 1.5, 300)

    reals = []
    imags = []
    for a in a_range:
        A = np.array([[a, b], [c, a]])
        ev = np.linalg.eigvals(A)
        reals.append(ev.real)
        imags.append(ev.imag)

    reals = np.array(reals)
    imags = np.array(imags)

    sc = ax.scatter(reals[:, 0], imags[:, 0],
                    c=a_range, cmap="RdYlGn_r", s=8, alpha=0.7, zorder=3)
    ax.scatter(reals[:, 1], imags[:, 1],
               c=a_range, cmap="RdYlGn_r", s=8, alpha=0.7, zorder=3)

    cb = plt.colorbar(sc, ax=ax, pad=0.02)
    cb.set_label("Parameter  a", fontsize=10)

    # highlight specific systems
    for sys in SYSTEMS[:3]:
        ev = np.linalg.eigvals(sys["A"])
        ax.plot(ev.real, ev.imag, "*", color=sys["color"],
                ms=14, mec="black", mew=0.6,
                label=sys["label"], zorder=6)

    ax.axvline(0, color="black", lw=1.2, ls="--", alpha=0.7)
    ax.axhline(0, color="black", lw=0.6, alpha=0.4)
    ax.set_xlabel("Re(λ)", fontsize=11)
    ax.set_ylabel("Im(λ)", fontsize=11)
    ax.set_title("Figure 4 — Eigenvalue Locus as Parameter  a  Varies",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=8, framealpha=0.8)
    ax.text(-0.15, ax.get_ylim()[1]*0.92, "← Stable | Unstable →",
            ha="center", fontsize=9, color="grey", style="italic")
    ax.grid(alpha=0.15)

    fig.tight_layout()
    path = f"{OUT}/fig4_eigenvalue_locus.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")


if __name__ == "__main__":
    print("Generating figures …")
    fig1_phase_portraits()
    fig2_time_series()
    fig3_stability_map()
    fig4_eigenvalue_locus()
    print("Done.")
