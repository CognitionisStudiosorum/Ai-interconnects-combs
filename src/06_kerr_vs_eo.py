"""Static figure: typical spectral shapes of a Kerr soliton comb and an EO comb.

Illustrative shapes, not measured data.
- Kerr soliton: sech^2 spectral envelope.
- EO comb: intensity modulator carving a pulse on top of a strong phase
  modulation (the classic flat-top configuration), computed with an FFT.
"""
import numpy as np

from common import INK, LAMBDA_COLORS, MUTED, plt, save_fig

FLOOR_DB = -40

# Kerr soliton comb
n_kerr = np.arange(-45, 46)
kerr_db = 10 * np.log10(1 / np.cosh(n_kerr / 9.0) ** 2)

# EO comb: E = gate(theta) * exp(i*beta*cos(theta))
N = 1024
theta = 2 * np.pi * np.arange(N) / N
beta = 12.0
gate = 0.5 * (1 + np.cos(theta))
coeffs = np.fft.fft(gate * np.exp(1j * beta * np.cos(theta))) / N
n_eo = np.arange(-45, 46)
eo_power = np.abs(coeffs[n_eo % N]) ** 2
eo_db = 10 * np.log10(np.maximum(eo_power / eo_power.max(), 1e-12))

fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
panels = [
    (axes[0], n_kerr, kerr_db, LAMBDA_COLORS[0], "Peine Kerr (solitón en microresonador)",
     "Muchas líneas y chip diminuto,\npero envolvente sech² y poca potencia por línea"),
    (axes[1], n_eo, eo_db, LAMBDA_COLORS[3], "Peine electro-óptico (IM + PM)",
     "Menos líneas, pero planas, potentes\ny con espaciado fijado por la RF"),
]
for ax, n, p_db, color, title, note in panels:
    ax.bar(n, np.maximum(p_db, FLOOR_DB) - FLOOR_DB, bottom=FLOOR_DB, width=0.6,
           color=color)
    ax.set_title(title, weight="bold", color=INK)
    ax.set_xlabel("Índice de línea n")
    ax.set_ylim(FLOOR_DB, 12)
    ax.text(0.5, 0.97, note, transform=ax.transAxes, ha="center", va="top",
            fontsize=9, color=MUTED)
axes[0].set_ylabel("Potencia por línea (dB, normalizada)")
fig.tight_layout()
save_fig(fig, "06_kerr_vs_eo.png")
