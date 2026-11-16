"""Animation: one comb source feeding a WDM link.

comb -> demux -> one modulator per line -> mux -> single fibre -> demux -> detectors
After the modulators, a missing dot is a '0' bit and a present dot is a '1' bit.
"""
import numpy as np
from matplotlib.animation import FuncAnimation

from common import (INK, LAMBDA_COLORS, MUTED, OPTICAL, blank_axes, box, plt,
                    save_anim, smoothstep)

N_CH = 8
LENGTH = 12.0          # x extent travelled by the light
SPEED = 0.1            # x units per frame
N_FRAMES = int(LENGTH / SPEED)
SPACING = 0.4
Y0 = 3.3
X_MOD = 4.5

fig = plt.figure(figsize=(11, 6.2))
gs = fig.add_gridspec(2, 2, height_ratios=[3, 1.25], hspace=0.3, wspace=0.25)
ax = fig.add_subplot(gs[0, :])
ax_comb = fig.add_subplot(gs[1, 0])
ax_fibre = fig.add_subplot(gs[1, 1])
blank_axes(ax, (-1.6, 13.4), (0.6, 6.3))
ax.set_title("Un solo peine alimenta todos los canales WDM de un enlace",
             weight="bold", fontsize=13)


def lane_y(x, ch):
    """Vertical position of channel ch at horizontal position x."""
    wide = (ch - (N_CH - 1) / 2) * 0.52
    tight = (ch - (N_CH - 1) / 2) * 0.05
    spread = np.where(
        x < 2.5, 0.0,
        np.where(x < 3.5, smoothstep(np.clip(x - 2.5, 0, 1)),
                 np.where(x < 5.5, 1.0,
                          np.where(x < 6.5, 1 - smoothstep(np.clip(x - 5.5, 0, 1)),
                                   np.where(x < 9.5, 0.0,
                                            np.where(x < 10.5,
                                                     smoothstep(np.clip(x - 9.5, 0, 1)),
                                                     1.0))))))
    return Y0 + tight + (wide - tight) * spread


xs = np.linspace(0, LENGTH, 400)
for ch in range(N_CH):
    ax.plot(xs, lane_y(xs, ch), color=LAMBDA_COLORS[ch], lw=1, alpha=0.25, zorder=1)
    y = lane_y(np.array(X_MOD), ch)
    box(ax, X_MOD - 0.3, y - 0.17, 0.6, 0.34, "MOD", fc="white", fontsize=6, zorder=5)
    y_det = lane_y(np.array(LENGTH), ch)
    box(ax, LENGTH, y_det - 0.17, 0.6, 0.34, "PD", fc="#e5e7eb", fontsize=6, zorder=5)

box(ax, -1.5, Y0 - 0.45, 1.5, 0.9, "Peine", fc="#dbeafe", ec=OPTICAL, fontsize=10)
for x, text in [(3.0, "demux"), (X_MOD, "datos\n(1 por línea)"), (6.0, "mux"),
                (8.0, "una sola fibra"), (10.0, "demux"), (12.3, "detectores")]:
    ax.text(x, 5.85, text, ha="center", va="center", fontsize=9, color=MUTED)

rng = np.random.default_rng(3)
n_dots = int(LENGTH / SPACING)
bits = rng.integers(0, 2, size=(N_CH, n_dots)).astype(bool)
base_x = np.arange(n_dots) * SPACING
rgb = np.array([plt.matplotlib.colors.to_rgb(c) for c in LAMBDA_COLORS])
dots = ax.scatter(np.zeros(N_CH * n_dots), np.zeros(N_CH * n_dots), s=22, zorder=4)


def update(frame):
    x = (base_x[None, :] + frame * SPEED) % LENGTH
    x = np.repeat(x, N_CH, axis=0)
    y = np.stack([lane_y(x[ch], ch) for ch in range(N_CH)])
    visible = (x < X_MOD) | bits
    colors = np.zeros((N_CH, n_dots, 4))
    colors[..., :3] = rgb[:, None, :]
    colors[..., 3] = visible
    dots.set_offsets(np.column_stack([x.ravel(), y.ravel()]))
    dots.set_facecolors(colors.reshape(-1, 4))
    return (dots,)


# Bottom-left: the comb itself
n = np.arange(N_CH)
ax_comb.vlines(n, 0, 1, colors=LAMBDA_COLORS, lw=4)
ax_comb.set_ylim(0, 1.25)
ax_comb.set_xlim(-1, N_CH)
ax_comb.set_yticks([])
ax_comb.set_xticks(n, [rf"$\lambda_{k + 1}$" for k in n])
ax_comb.set_title("Lo que sale del peine: 8 portadoras equiespaciadas", fontsize=9,
                  color=INK)

# Bottom-right: spectrum on the fibre after modulation
f = np.linspace(-1, N_CH, 1600)
for k in n:
    lobe = np.sinc((f - k) / 0.42) ** 2
    lobe[np.abs(f - k) > 0.42] = 0
    ax_fibre.fill_between(f, lobe, color=LAMBDA_COLORS[k], alpha=0.6, lw=0)
ax_fibre.set_ylim(0, 1.25)
ax_fibre.set_xlim(-1, N_CH)
ax_fibre.set_yticks([])
ax_fibre.set_xticks(n, [rf"$\lambda_{k + 1}$" for k in n])
ax_fibre.set_title("Lo que viaja por la fibra: 8 canales de datos", fontsize=9,
                   color=INK)

anim = FuncAnimation(fig, update, frames=N_FRAMES, blit=False)
save_anim(anim, "07_wdm_comb_link.gif")
