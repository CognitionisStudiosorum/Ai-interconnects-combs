"""Shared style, colours and helpers used by every figure script."""
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import PillowWriter  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

FIG_DIR = Path(__file__).resolve().parents[1] / "figures"
FIG_DIR.mkdir(exist_ok=True)

INK = "#1f2933"
MUTED = "#7b8794"
PANEL = "#eef2f6"
ELECTRIC = "#9aa5b1"
COPPER = "#d97706"
OPTICAL = "#2563eb"
ACCENT = "#d64545"
# One colour per wavelength channel (violet -> red).
LAMBDA_COLORS = [
    "#7c3aed", "#2563eb", "#0891b2", "#059669",
    "#65a30d", "#ca8a04", "#ea580c", "#dc2626",
]

mpl.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "text.color": INK,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def smoothstep(u):
    """Smooth 0 -> 1 transition, used to bend paths without kinks."""
    return u * u * (3 - 2 * u)


def box(ax, x, y, w, h, label="", fc=PANEL, ec=MUTED, fontsize=9, lw=1.2,
        text_color=INK, zorder=2, **text_kw):
    """Draw a rounded box with a centred label."""
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                           fc=fc, ec=ec, lw=lw, zorder=zorder)
    ax.add_patch(patch)
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fontsize, color=text_color, zorder=zorder + 1, **text_kw)
    return patch


def blank_axes(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")


def save_fig(fig, name, dpi=150):
    path = FIG_DIR / name
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {path.relative_to(FIG_DIR.parent)}")


def save_anim(anim, name, fps=20, dpi=80):
    path = FIG_DIR / name
    anim.save(path, writer=PillowWriter(fps=fps), dpi=dpi)
    plt.close(anim._fig)
    print(f"saved {path.relative_to(FIG_DIR.parent)}")
