"""Animation: an electro-optic comb appears as the phase-modulation depth grows.

A CW laser through a phase modulator gives E(t) = exp(i*beta*sin(2*pi*f_RF*t)).
Its spectrum has lines at f0 + n*f_RF with power J_n(beta)^2. We get the line
powers numerically with an FFT over one RF period, so no Bessel library is needed.
"""
import numpy as np
from matplotlib.animation import FuncAnimation

from common import ACCENT, COPPER, INK, MUTED, OPTICAL, blank_axes, box, plt, save_anim

N_FRAMES = 100
BETA_MAX = 10.0
N_SAMPLES = 256
orders = np.arange(-20, 21)
theta = 2 * np.pi * np.arange(N_SAMPLES) / N_SAMPLES
FLOOR_DB = -40


def line_powers_db(beta):
    coeffs = np.fft.fft(np.exp(1j * beta * np.sin(theta))) / N_SAMPLES
    power = np.abs(coeffs[orders % N_SAMPLES]) ** 2
    return 10 * np.log10(np.maximum(power, 1e-12))


fig = plt.figure(figsize=(9, 5.6))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 3.2], hspace=0.25)
ax_s = fig.add_subplot(gs[0])
ax = fig.add_subplot(gs[1])

blank_axes(ax_s, (0, 10), (0, 2.2))
box(ax_s, 0.4, 0.9, 1.8, 0.8, "Láser CW", fc="#dbeafe", ec=OPTICAL)
box(ax_s, 3.6, 0.9, 2.6, 0.8, "Modulador de fase", fc="#f1f5f9")
box(ax_s, 4.1, 0.0, 1.6, 0.5, r"RF a $f_{RF}$", fc="#fef3c7", ec=COPPER, fontsize=8)
ax_s.annotate("", xy=(3.6, 1.3), xytext=(2.2, 1.3),
              arrowprops=dict(arrowstyle="->", color=OPTICAL, lw=2))
ax_s.annotate("", xy=(8.2, 1.3), xytext=(6.2, 1.3),
              arrowprops=dict(arrowstyle="->", color=OPTICAL, lw=2))
ax_s.annotate("", xy=(4.9, 0.9), xytext=(4.9, 0.5),
              arrowprops=dict(arrowstyle="->", color=COPPER, lw=1.5))
ax_s.text(8.35, 1.3, "peine EO", va="center", color=OPTICAL, weight="bold")
ax_s.set_title("Formación de un peine electro-óptico", weight="bold", fontsize=13)

bars = ax.bar(orders, np.zeros(orders.size), width=0.55, bottom=FLOOR_DB, color=OPTICAL)
ax.axhline(-20, color=ACCENT, lw=1, ls="--")
ax.text(20.4, -19.2, "−20 dB", color=ACCENT, fontsize=8, ha="right")
ax.set_ylim(FLOOR_DB, 3)
ax.set_xlim(-21, 21)
ax.set_xlabel(r"Índice de línea n   (frecuencia $= f_0 + n\,f_{RF}$)")
ax.set_ylabel("Potencia por línea (dB respecto al láser)")
label = ax.text(0.02, 0.93, "", transform=ax.transAxes, fontsize=11, color=INK)
count = ax.text(0.02, 0.85, "", transform=ax.transAxes, fontsize=9, color=MUTED)


def update(frame):
    beta = BETA_MAX * (1 - np.cos(2 * np.pi * frame / N_FRAMES)) / 2
    p_db = line_powers_db(beta)
    for bar, p in zip(bars, p_db):
        bar.set_height(max(p, FLOOR_DB) - FLOOR_DB)
    label.set_text(rf"Profundidad de modulación $\beta$ = {beta:4.1f} rad")
    count.set_text(f"Líneas por encima de −20 dB: {(p_db > -20).sum()}")
    return (*bars, label, count)


anim = FuncAnimation(fig, update, frames=N_FRAMES, blit=False)
save_anim(anim, "05_eo_comb_formation.gif")
