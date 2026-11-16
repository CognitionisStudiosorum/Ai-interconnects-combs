"""Animation: electrical packet switch (O-E-O) versus optical circuit switch."""
import numpy as np
from matplotlib.animation import FuncAnimation

from common import (ELECTRIC, INK, LAMBDA_COLORS, MUTED, blank_axes, box, plt,
                    save_anim, smoothstep)

N_FRAMES = 120
PORT_Y = np.array([1.2, 2.3, 3.4, 4.5])
PORT_COLORS = [LAMBDA_COLORS[i] for i in (1, 3, 5, 7)]
X_IN, X_OUT = 3.0, 7.0

fig, (ax_eps, ax_ocs) = plt.subplots(1, 2, figsize=(11, 4.8))
for ax in (ax_eps, ax_ocs):
    blank_axes(ax, (0, 10), (-0.3, 6.4))
    for y in PORT_Y:
        ax.plot([0, X_IN], [y, y], color=MUTED, lw=1.5, zorder=1)
        ax.plot([X_OUT, 10], [y, y], color=MUTED, lw=1.5, zorder=1)
    box(ax, X_IN, 0.6, X_OUT - X_IN, 4.5, fc="#f8fafc")

# --- Electrical packet switch -------------------------------------------------
ax_eps.text(5, 6.1, "Conmutador electrónico de paquetes (EPS)", ha="center",
            fontsize=12, weight="bold")
box(ax_eps, 3.1, 0.75, 0.8, 4.2, "O→E", fc="#fde8e8", ec="#d64545", fontsize=8)
box(ax_eps, 4.2, 0.75, 1.6, 4.2, "ASIC\nlee cada\npaquete", fc="#e5e7eb", fontsize=8)
box(ax_eps, 6.1, 0.75, 0.8, 4.2, "E→O", fc="#fde8e8", ec="#d64545", fontsize=8)
ax_eps.text(5, 0.0, "Decide paquete a paquete, pero paga 2 transceptores\n"
            "y un chip de conmutación en cada salto", ha="center", fontsize=9,
            color=INK)

rng = np.random.default_rng(7)
eps_packets = []  # (emission frame, input port, output port)
for i in range(4):
    for t0 in np.arange(0, N_FRAMES, 10):
        eps_packets.append((t0 + 2.5 * i, i, int(rng.integers(0, 4))))

eps_light = ax_eps.scatter([], [], s=70, zorder=5)
eps_elec = ax_eps.scatter([], [], s=60, marker="s", zorder=5, linewidths=1.8,
                          facecolors=ELECTRIC)

# --- Optical circuit switch ---------------------------------------------------
ax_ocs.text(5, 6.1, "Conmutador de circuitos ópticos (OCS)", ha="center",
            fontsize=12, weight="bold")
ax_ocs.text(5, 0.0, "La luz cruza sin convertirse. Conecta puerto con puerto\n"
            "y se reconfigura cuando cambia la carga de trabajo", ha="center",
            fontsize=9, color=INK)
PERMS = [[1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
PHASE = N_FRAMES // len(PERMS)
TRAVEL = 12
ocs_lines = [ax_ocs.plot([], [], lw=2.5, alpha=0.35, zorder=3)[0] for _ in range(4)]
ocs_light = ax_ocs.scatter([], [], s=70, zorder=5)
ocs_status = ax_ocs.text(5, 5.35, "", ha="center", fontsize=9, color="#d64545",
                         weight="bold")

ocs_packets = []  # (emission frame, input port, output port)
for p, perm in enumerate(PERMS):
    for local in range(2, PHASE - TRAVEL - 2, 4):
        for i in range(4):
            ocs_packets.append((p * PHASE + local, i, perm[i]))


def eps_state(age, i, j):
    """Position and domain (optical/electrical) of an EPS packet."""
    if age < 6:
        return X_IN * age / 6, PORT_Y[i], True
    if age < 18:
        u = (age - 6) / 12
        y = PORT_Y[i] + (PORT_Y[j] - PORT_Y[i]) * smoothstep(u)
        return X_IN + (X_OUT - X_IN) * u, y, False
    return X_OUT + (10 - X_OUT) * (age - 18) / 6, PORT_Y[j], True


def ocs_state(age, i, j):
    x = 10 * age / TRAVEL
    u = np.clip((x - X_IN) / (X_OUT - X_IN), 0, 1)
    return x, PORT_Y[i] + (PORT_Y[j] - PORT_Y[i]) * u


def update(frame):
    light, light_c, elec, elec_c = [], [], [], []
    for t0, i, j in eps_packets:
        age = (frame - t0) % N_FRAMES
        if age < 24:
            x, y, optical = eps_state(age, i, j)
            (light if optical else elec).append((x, y))
            (light_c if optical else elec_c).append(PORT_COLORS[j])
    eps_light.set_offsets(np.array(light).reshape(-1, 2))
    eps_light.set_facecolors(light_c)
    eps_elec.set_offsets(np.array(elec).reshape(-1, 2))
    eps_elec.set_edgecolors(elec_c)

    phase, local = divmod(frame, PHASE)
    perm = PERMS[phase]
    reconfiguring = local >= PHASE - 3
    for i, line in enumerate(ocs_lines):
        line.set_data([X_IN, X_OUT], [PORT_Y[i], PORT_Y[perm[i]]])
        line.set_color(PORT_COLORS[i])
        line.set_alpha(0.1 if reconfiguring else 0.35)
    ocs_status.set_text("reconfigurando…" if reconfiguring else "")
    pts, cols = [], []
    for t0, i, j in ocs_packets:
        age = frame - t0
        if 0 <= age < TRAVEL:
            pts.append(ocs_state(age, i, j))
            cols.append(PORT_COLORS[i])
    ocs_light.set_offsets(np.array(pts).reshape(-1, 2))
    ocs_light.set_facecolors(cols)
    return eps_light, eps_elec, ocs_light, ocs_status, *ocs_lines


fig.tight_layout()
anim = FuncAnimation(fig, update, frames=N_FRAMES, blit=False)
save_anim(anim, "01_eps_vs_ocs.gif")
