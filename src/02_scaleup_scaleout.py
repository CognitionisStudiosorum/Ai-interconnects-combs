"""Static diagram: scale-up versus scale-out networks in an AI cluster."""
from common import COPPER, INK, MUTED, OPTICAL, blank_axes, box, plt, save_fig

fig, ax = plt.subplots(figsize=(11, 6))
blank_axes(ax, (0, 12), (0, 7.6))

RACK_X = [0.8, 4.8, 8.8]
RACK_W = 2.4
spine_x = [3.2, 7.0]

for sx in spine_x:
    box(ax, sx, 6.4, 1.8, 0.6, "Spine", fc="#dbeafe", ec=OPTICAL)

for rx in RACK_X:
    box(ax, rx, 0.4, RACK_W, 3.7, fc="#f8fafc", zorder=0)
    ax.text(rx + RACK_W / 2, 0.15, "Rack", ha="center", fontsize=9, color=MUTED)
    box(ax, rx + 0.5, 3.35, 1.7, 0.55, "Switch scale-up", fc="#fef3c7", ec=COPPER,
        fontsize=8)
    for k in range(4):
        gy = 0.6 + k * 0.66
        box(ax, rx + 0.5, gy, 1.7, 0.5, f"GPU {k + 1}", fc="#e5e7eb", fontsize=8)
        # scale-up link along the left side of the rack
        ax.plot([rx + 0.5, rx + 0.2, rx + 0.2, rx + 0.5],
                [gy + 0.25, gy + 0.25, 3.62, 3.62], color=COPPER, lw=1.8, zorder=1)
    leaf_x = rx + 0.3
    box(ax, leaf_x, 4.9, 1.8, 0.6, "Leaf", fc="#dbeafe", ec=OPTICAL)
    ax.plot([rx + 1.35, rx + 1.35], [3.9, 4.9], color=OPTICAL, lw=1.8, zorder=1)
    for sx in spine_x:
        ax.plot([leaf_x + 0.9, sx + 0.9], [5.5, 6.4], color=OPTICAL, lw=1.8, zorder=1)

ax.plot([], [], color=COPPER, lw=2.5,
        label="Scale-up: GPU con GPU dentro del rack o pod (metros).\n"
              "Hoy cobre, migrando a óptica. Aquí encajan OCS pequeños y rápidos")
ax.plot([], [], color=OPTICAL, lw=2.5,
        label="Scale-out: rack con rack (decenas a cientos de metros).\n"
              "Ya es óptico. Aquí usa Google sus OCS de gran número de puertos")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, frameon=False,
          fontsize=9)
ax.set_title("Dos redes dentro de un clúster de IA", fontsize=13, weight="bold",
             color=INK)
save_fig(fig, "02_scaleup_scaleout.png")
