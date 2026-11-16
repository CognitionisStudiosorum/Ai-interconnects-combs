"""Static figure: a frequency comb seen in time and in frequency."""
import numpy as np

from common import ACCENT, INK, MUTED, OPTICAL, plt, save_fig

n = np.arange(-15, 16)
amp = np.exp(-(n / 7.0) ** 2)  # Gaussian spectral envelope (field amplitude)
t = np.linspace(-0.6, 3.6, 4000)  # time in units of the repetition period T
field = (amp[:, None] * np.exp(2j * np.pi * n[:, None] * t[None, :])).sum(axis=0)
intensity = np.abs(field) ** 2
intensity /= intensity.max()

fig, (ax_t, ax_f) = plt.subplots(1, 2, figsize=(11, 3.8))

ax_t.plot(t, intensity, color=OPTICAL, lw=1.8)
ax_t.fill_between(t, intensity, color=OPTICAL, alpha=0.15)
ax_t.annotate("", xy=(1, 1.08), xytext=(2, 1.08),
              arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1.5))
ax_t.text(1.5, 1.13, r"$T = 1/f_{rep}$", ha="center", color=ACCENT)
ax_t.set_ylim(0, 1.3)
ax_t.set_xlabel("Tiempo (en periodos T)")
ax_t.set_ylabel("Intensidad (u.a.)")
ax_t.set_title("En el tiempo: un tren de pulsos", weight="bold", color=INK)

power = amp ** 2
ax_f.vlines(n, 0, power, color=OPTICAL, lw=2)
ax_f.plot(n, power, "--", color=MUTED, lw=1)
ax_f.annotate("", xy=(3, 0.45), xytext=(4, 0.45),
              arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1.5))
ax_f.text(5.2, 0.52, r"$f_{rep}$", ha="center", color=ACCENT)
ax_f.text(-15, 1.12, r"$f_n = f_0 + n\,f_{rep}$", color=INK, fontsize=11)
ax_f.set_ylim(0, 1.3)
ax_f.set_xlabel("Índice de línea n")
ax_f.set_ylabel("Potencia por línea (u.a.)")
ax_f.set_title("En frecuencia: líneas equiespaciadas", weight="bold", color=INK)

fig.tight_layout()
save_fig(fig, "04_comb_time_frequency.png")
