"""Static figure: two ways of carrying 1.6 Tb/s on one fibre.

Channel width is drawn proportional to the symbol rate:
- 4 x 400 G: 200 GBd PAM4, needs heavy DSP.
- 32 x 50 G: 50 GBd NRZ, simple electronics, but needs 32 carriers (a comb).
"""
import numpy as np

from common import INK, LAMBDA_COLORS, MUTED, plt, save_fig

SPAN = 3400  # GHz shown


def draw(ax, n_ch, baud_ghz, title, note):
    spacing = 2 * baud_ghz
    centres = (np.arange(n_ch) - (n_ch - 1) / 2) * spacing
    f = np.linspace(-SPAN / 2, SPAN / 2, 6000)
    for k, fc in enumerate(centres):
        lobe = np.exp(-((f - fc) / (0.42 * baud_ghz)) ** 4)
        colour = LAMBDA_COLORS[int(k * len(LAMBDA_COLORS) / n_ch)]
        ax.fill_between(f, lobe, color=colour, alpha=0.75, lw=0)
    ax.set_ylim(0, 1.45)
    ax.set_yticks([])
    ax.set_title(title, weight="bold", color=INK, loc="left")
    ax.text(0.995, 0.95, note, transform=ax.transAxes, ha="right", va="top",
            fontsize=9, color=MUTED)


fig, (ax_a, ax_b) = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
draw(ax_a, 4, 200, "Rápido y estrecho: 4 λ × 400 G = 1,6 Tb/s",
     "200 GBd PAM4 por canal: SerDes y DSP al límite, 4 láseres")
draw(ax_b, 32, 50, "Ancho y lento: 32 λ × 50 G = 1,6 Tb/s",
     "50 GBd NRZ por canal: electrónica sencilla, pero 32 portadoras (un peine)")
ax_b.set_xlabel("Frecuencia óptica relativa (GHz)")
fig.tight_layout()
save_fig(fig, "08_wide_and_slow.png")
