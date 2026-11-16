"""Static diagram: front-panel pluggable optics versus co-packaged optics."""
import numpy as np

from common import ACCENT, COPPER, INK, MUTED, OPTICAL, blank_axes, box, plt, save_fig

fig, (ax_p, ax_c) = plt.subplots(1, 2, figsize=(11, 5))
PORT_Y = np.linspace(0.9, 5.1, 8)

for ax in (ax_p, ax_c):
    blank_axes(ax, (0, 10), (-0.9, 6.9))
    box(ax, 0.3, 0.4, 8.2, 5.2, fc="#ecfdf5", ec="#059669", zorder=0)  # PCB
    ax.text(0.5, 5.3, "Placa", fontsize=8, color="#059669")
    ax.plot([8.5, 8.5], [0.4, 5.6], color=INK, lw=3)  # front panel
    ax.text(8.5, 5.85, "Panel frontal", ha="center", fontsize=8, color=MUTED)

# --- Pluggables ---------------------------------------------------------------
ax_p.set_title("Óptica enchufable (hoy)", fontsize=12, weight="bold")
box(ax_p, 1.2, 2.2, 1.6, 1.6, "ASIC", fc="#e5e7eb", fontsize=10)
for y in PORT_Y:
    ax_p.plot([2.8, 7.4], [3.0, y], color=COPPER, lw=1.6, zorder=1)
    box(ax_p, 7.4, y - 0.2, 1.3, 0.4, "DSP+óptica", fc="#fde8e8", ec=ACCENT, fontsize=6)
    ax_p.plot([8.7, 10], [y, y], color=OPTICAL, lw=1.6)
ax_p.text(5, -0.5, "Trazas eléctricas largas (decenas de cm) a 100-200 G por lane:\n"
          "hacen falta DSP y retimers en cada módulo", ha="center", fontsize=9)

# --- Co-packaged optics -------------------------------------------------------
ax_c.set_title("Óptica co-empaquetada (CPO)", fontsize=12, weight="bold")
box(ax_c, 2.4, 1.6, 2.8, 2.8, fc="#f1f5f9", ec=MUTED, zorder=0.5)  # shared substrate
ax_c.text(3.8, 4.55, "Sustrato común", ha="center", fontsize=7, color=MUTED)
box(ax_c, 3.1, 2.3, 1.4, 1.4, "ASIC", fc="#e5e7eb", fontsize=10)
# (x, y) of each photonic engine and the front-panel ports it serves
engines = [((3.55, 3.8), PORT_Y[6:8]), ((4.6, 3.15), PORT_Y[4:6]),
           ((4.6, 2.35), PORT_Y[2:4]), ((3.55, 1.7), PORT_Y[0:2])]
for (ex, ey), ports in engines:
    box(ax_c, ex, ey, 0.5, 0.5, "PIC", fc="#dbeafe", ec=OPTICAL, fontsize=6)
    for y in ports:
        ax_c.plot([ex + 0.5, 6.4, 8.5, 10], [ey + 0.25, y, y, y], color=OPTICAL,
                  lw=1.4, zorder=1)
box(ax_c, 7.2, -0.1, 1.5, 0.45, "Láser externo", fc="#fef3c7", ec=COPPER, fontsize=7)
ax_c.annotate("", xy=(5.25, 1.9), xytext=(7.2, 0.15),
              arrowprops=dict(arrowstyle="->", color=COPPER, lw=1.5,
                              connectionstyle="arc3,rad=-0.2"))
ax_c.text(4.2, 0.72, "luz continua\n(aquí puede ir un peine)", fontsize=7,
          color=COPPER, ha="center")
ax_c.text(5, -0.72, "Trazas eléctricas de milímetros: menos consumo por bit.\n"
          "El láser se saca fuera para poder sustituirlo", ha="center", fontsize=9)

ax_p.plot([], [], color=COPPER, lw=2, label="Eléctrico")
ax_p.plot([], [], color=OPTICAL, lw=2, label="Óptico (fibra)")
ax_p.legend(loc="upper left", bbox_to_anchor=(0.02, 1.0), frameon=False, fontsize=8,
            ncol=2)
fig.tight_layout()
save_fig(fig, "03_pluggable_vs_cpo.png")
