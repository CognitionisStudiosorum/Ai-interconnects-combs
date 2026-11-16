"""Static figure: why comb flatness decides how many channels are usable.

Illustrative numbers. A link needs a minimum optical power per carrier. With a
sech^2 comb only the central lines clear that threshold. Redistributing the same
total power evenly (even after paying a 3 dB penalty) makes more lines usable.
"""
import numpy as np

from common import ACCENT, INK, LAMBDA_COLORS, MUTED, plt, save_fig

n = np.arange(-30, 31)
THRESHOLD_DBM = -10.0
FLOOR = -32
PENALTY_DB = 3.0
N_FLAT = 41

raw_mw = 1.0 / np.cosh(n / 8.0) ** 2            # central line = 0 dBm
raw_dbm = 10 * np.log10(raw_mw)
total_mw = raw_mw.sum()

flat_level_mw = total_mw / N_FLAT / 10 ** (PENALTY_DB / 10)
flat_dbm = np.full(n.size, -99.0)
flat_dbm[np.abs(n) <= N_FLAT // 2] = 10 * np.log10(flat_level_mw)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
titles = ["Peine sin aplanar (envolvente sech²)",
          f"Misma potencia total, aplanada (con {PENALTY_DB:.0f} dB de penalización)"]
for ax, p_dbm, title in zip(axes, (raw_dbm, flat_dbm), titles):
    usable = p_dbm >= THRESHOLD_DBM
    heights = np.maximum(p_dbm, FLOOR) - FLOOR
    ax.bar(n[usable], heights[usable], bottom=FLOOR, width=0.6, color=LAMBDA_COLORS[3],
           label="Línea utilizable")
    ax.bar(n[~usable], heights[~usable], bottom=FLOOR, width=0.6, color="#cbd5e1",
           label="Demasiado débil")
    ax.axhline(THRESHOLD_DBM, color=ACCENT, ls="--", lw=1.2,
               label="Potencia mínima por portadora")
    ax.set_ylim(FLOOR, 8)
    ax.set_xlabel("Índice de línea n")
    ax.set_title(title, weight="bold", color=INK, fontsize=10)
    ax.text(0.5, 0.95, f"{usable.sum()} canales utilizables", transform=ax.transAxes,
            ha="center", va="top", fontsize=12, weight="bold", color=LAMBDA_COLORS[3])
axes[0].set_ylabel("Potencia por línea (dBm)")
fig.tight_layout()
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.07), ncol=3,
           frameon=False, fontsize=9)
fig.text(0.99, -0.05, "Valores ilustrativos", ha="right", fontsize=8, color=MUTED)
save_fig(fig, "10_flatness_link_budget.png")
