"""Animation: wavelength routing. Picking a comb line picks the destination.

An AWGR (arrayed waveguide grating router) is passive: each wavelength entering a
port leaves through a different output port. Switching = changing colour.
"""
import numpy as np
from matplotlib.animation import FuncAnimation

from common import (INK, LAMBDA_COLORS, MUTED, OPTICAL, blank_axes, box, plt,
                    save_anim, smoothstep)

N_FRAMES = 120
PHASE = 30
ORDER = [0, 2, 1, 3]                      # wavelength chosen in each phase
COLORS = [LAMBDA_COLORS[i] for i in (1, 3, 5, 7)]
OUT_Y = np.array([4.8, 3.6, 2.4, 1.2])
Y_C = 3.0
X_TX, X_AWGR_IN, X_FAN_END, X_RACK = 2.4, 4.2, 6.8, 8.4
SPEED = 0.2
LIFE = int((X_RACK - X_TX) / SPEED)

fig, ax = plt.subplots(figsize=(10, 5))
blank_axes(ax, (0, 10), (0, 6.2))
ax.set_title("Enrutado por longitud de onda: elegir color es elegir destino",
             weight="bold", fontsize=13)

box(ax, 0.2, 2.1, 2.2, 1.8, fc="#dbeafe", ec=OPTICAL)
ax.text(1.3, 2.35, "Transmisor", ha="center", fontsize=9)
comb_x = 0.65 + 0.43 * np.arange(4)
comb = [ax.plot([x, x], [2.75, 3.6], lw=5, solid_capstyle="butt")[0] for x in comb_x]
ax.plot([X_TX, X_AWGR_IN], [Y_C, Y_C], color=MUTED, lw=1.5, zorder=1)
box(ax, X_AWGR_IN, 0.7, 1.6, 4.6, fc="#f1f5f9")
ax.text(X_AWGR_IN + 0.8, 5.55, "AWGR (pasivo, sin consumo)", ha="center", fontsize=9)
for k, y in enumerate(OUT_Y):
    ax.plot([X_AWGR_IN + 1.6, X_FAN_END, X_RACK], [y, y, y], color=MUTED, lw=1.5,
            zorder=1)
    box(ax, X_RACK, y - 0.4, 1.4, 0.8, f"Rack {k + 1}", fc="white", ec=COLORS[k], lw=2.5)
status = ax.text(1.3, 4.35, "", ha="center", fontsize=11, weight="bold")
ax.text(5, 0.2, "Cambiar de línea del peine lleva nanosegundos: no hay nada que mover",
        ha="center", fontsize=9, color=INK)

emissions = np.arange(0, N_FRAMES, 2)
dots = ax.scatter([], [], s=45, zorder=5)


def update(frame):
    current = ORDER[(frame // PHASE) % len(ORDER)]
    for k, line in enumerate(comb):
        line.set_color(COLORS[k])
        line.set_alpha(1.0 if k == current else 0.18)
    status.set_text(rf"$\lambda_{current + 1}$ → Rack {current + 1}")
    status.set_color(COLORS[current])

    pts, cols = [], []
    for t0 in emissions:
        age = (frame - t0) % N_FRAMES
        if age >= LIFE:
            continue
        lam = ORDER[(t0 // PHASE) % len(ORDER)]
        x = X_TX + age * SPEED
        u = np.clip((x - X_AWGR_IN) / (X_FAN_END - X_AWGR_IN), 0, 1)
        pts.append((x, Y_C + (OUT_Y[lam] - Y_C) * smoothstep(u)))
        cols.append(COLORS[lam])
    dots.set_offsets(np.array(pts).reshape(-1, 2))
    dots.set_facecolors(cols)
    return (dots, status, *comb)


anim = FuncAnimation(fig, update, frames=N_FRAMES, blit=False)
save_anim(anim, "09_awgr_routing.gif")
