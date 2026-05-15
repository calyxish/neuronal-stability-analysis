"""
simulation.py
-------------
Core numerical routines for the two-dimensional linear neuronal model.

Author : Kwakye Ishmael Affum
GitHub : https://github.com/calyxish
Email  : kwakyeishmael07@gmail.com

Description
-----------
Implements forward-Euler integration of the system

    dX/dt = A X,   X(0) = X0

where X = [V, W]^T (membrane potential, recovery variable) and
A is a 2x2 real system matrix whose eigenvalues govern stability.
"""

import numpy as np


def simulate(A: np.ndarray,
             X0: np.ndarray,
             dt: float = 0.01,
             T: float = 10.0) -> np.ndarray:
    """
    Integrate dX/dt = A @ X with forward Euler.

    Parameters
    ----------
    A  : (2, 2) system matrix
    X0 : (2,)  initial state [V0, W0]
    dt : float  time step (s)
    T  : float  total simulation time (s)

    Returns
    -------
    trajectory : (steps, 2) array of states
    """
    steps = int(T / dt)
    X = X0.copy().astype(float)
    trajectory = np.empty((steps, 2))

    for k in range(steps):
        trajectory[k] = X
        X = X + dt * (A @ X)

    return trajectory


def stability_info(A: np.ndarray) -> dict:
    """
    Compute eigenvalues, trace, determinant, and classify stability.

    Parameters
    ----------
    A : (2, 2) system matrix

    Returns
    -------
    info : dict with keys
        eigenvalues, trace, determinant, label, stable, oscillatory
    """
    eigvals = np.linalg.eigvals(A)
    tr = np.trace(A)
    det = np.linalg.det(A)

    real_parts = eigvals.real
    imag_parts = eigvals.imag

    stable     = bool(np.all(real_parts < 0))
    oscillatory = bool(np.any(np.abs(imag_parts) > 1e-10))

    if stable and oscillatory:
        label = "Stable Oscillatory (Damped)"
    elif stable and not oscillatory:
        label = "Stable Node"
    elif not stable and oscillatory:
        label = "Unstable Oscillatory"
    else:
        label = "Unstable"

    return {
        "eigenvalues" : eigvals,
        "trace"       : tr,
        "determinant" : det,
        "label"       : label,
        "stable"      : stable,
        "oscillatory" : oscillatory,
    }
