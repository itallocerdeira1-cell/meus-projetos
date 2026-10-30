"""Estilo da casa para figuras científicas em matplotlib/seaborn.

Uso:
    import sys; sys.path.insert(0, "<pasta da skill>/assets")
    from estilo_pub import aplicar_estilo, figura, letra_painel, salvar_pub, OKABE_ITO

    p = aplicar_estilo("revista-alto")
    fig, ax = figura(p, largura="1col", altura_mm=60)
    ...
    salvar_pub(fig, "figuras/minha-figura/minha-figura", p)
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter

# Perfis de destino (references/destinos.md). Fontes em pt no tamanho final.
PERFIS = {
    "revista-alto":     dict(largura_mm=89,  largura2_mm=183, fonte=7,  fonte_min=5,  linha=0.5,  dpi=600, formatos=("pdf", "tiff", "png")),
    "revista-nacional": dict(largura_mm=85,  largura2_mm=175, fonte=8,  fonte_min=6,  linha=0.5,  dpi=600, formatos=("pdf", "tiff", "png")),
    "resumo":           dict(largura_mm=160, largura2_mm=160, fonte=9,  fonte_min=7,  linha=0.75, dpi=300, formatos=("png", "jpg", "pdf")),
    "poster":           dict(largura_mm=280, largura2_mm=560, fonte=28, fonte_min=24, linha=1.5,  dpi=300, formatos=("pdf", "png")),
    "eposter":          dict(largura_mm=290, largura2_mm=290, fonte=18, fonte_min=14, linha=1.25, dpi=200, formatos=("png", "pdf")),
    "slide":            dict(largura_mm=290, largura2_mm=290, fonte=20, fonte_min=18, linha=1.5,  dpi=200, formatos=("png", "pdf")),
}

# Okabe & Ito (2008): segura para daltonismo. Amarelo fica por último (pouco contraste em fundo branco).
OKABE_ITO = ["#0072B2", "#D55E00", "#009E73", "#E69F00", "#56B4E9", "#CC79A7", "#000000", "#F0E442"]
CINZA = "#9A9A9A"
TINTA = "#333333"

_FONTES = ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"]


def mm(valor):
    """Milímetros para polegadas (unidade do matplotlib)."""
    return valor / 25.4


def _fonte_disponivel():
    nomes = {f.name for f in font_manager.fontManager.ttflist}
    return next((f for f in _FONTES if f in nomes), "DejaVu Sans")


def aplicar_estilo(perfil="revista-alto"):
    """Aplica o estilo da casa para o perfil e devolve o dicionário do perfil."""
    p = dict(PERFIS[perfil], nome=perfil)
    f, lw = p["fonte"], p["linha"]
    tick = max(round(f * 0.9, 1), p["fonte_min"])
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [_fonte_disponivel()] + _FONTES,
        "font.size": f,
        "axes.titlesize": f,
        "axes.labelsize": f,
        "xtick.labelsize": tick,
        "ytick.labelsize": tick,
        "legend.fontsize": tick,
        "legend.frameon": False,
        "axes.edgecolor": TINTA,
        "axes.labelcolor": TINTA,
        "axes.linewidth": lw,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "axes.prop_cycle": mpl.cycler(color=OKABE_ITO),
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "grid.color": "#E5E5E5",
        "grid.linewidth": lw * 0.8,
        "xtick.color": TINTA,
        "ytick.color": TINTA,
        "xtick.major.width": lw,
        "ytick.major.width": lw,
        "xtick.major.size": f * 0.4,
        "ytick.major.size": f * 0.4,
        "lines.linewidth": lw * 2.5,
        "lines.markersize": f * 0.6,
        "patch.linewidth": lw,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.bbox": None,  # o tamanho final é o tamanho pedido; nada de recorte automático
        "pdf.fonttype": 42,  # fontes embutidas e editáveis
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })
    return p


def figura(p, largura="1col", altura_mm=None, **kwargs):
    """Cria a figura no tamanho final. largura: '1col', '2col' ou número em mm."""
    w = {"1col": p["largura_mm"], "2col": p["largura2_mm"]}.get(largura, largura)
    h = altura_mm or w * 0.62
    kwargs.setdefault("layout", "constrained")
    if "mosaic" in kwargs:
        mosaic = kwargs.pop("mosaic")
        fig, axes = plt.subplot_mosaic(mosaic, figsize=(mm(w), mm(h)), **kwargs)
    else:
        fig, axes = plt.subplots(figsize=(mm(w), mm(h)), **kwargs)
    return fig, axes


def letra_painel(ax, letra, p=None):
    """Letra do painel (A, B, C...) em negrito, no canto superior esquerdo, fora da área de dados."""
    tamanho = (p["fonte"] if p else mpl.rcParams["font.size"]) * 1.15
    ax.set_title(letra, loc="left", fontweight="bold", fontsize=tamanho, pad=tamanho * 0.6)


def virgula_decimal(ax, eixos="xy", casas=None):
    """Troca ponto por vírgula nas marcações (destinos em português)."""
    def fmt(v, _pos):
        s = f"{v:.{casas}f}" if casas is not None else f"{v:g}"
        return s.replace("-", "−").replace(".", ",")
    for e in eixos:
        getattr(ax, f"{e}axis").set_major_formatter(FuncFormatter(fmt))


def fmt_num(v, casas=1, idioma="pt"):
    """Formata número para anotação, com vírgula decimal em português e sinal de menos tipográfico."""
    s = f"{v:.{casas}f}".replace("-", "−")
    return s.replace(".", ",") if idioma == "pt" else s


def raincloud(ax, grupos, valores, cores=None, largura=0.7, semente=1, rotulos_n=True, idioma="pt"):
    """Raincloud vertical: pontos + boxplot estreito + meia densidade, um grupo por posição no eixo x.

    grupos: lista de nomes na ordem desejada; valores: lista de arrays (um por grupo).
    """
    cores = cores or OKABE_ITO
    rng = np.random.default_rng(semente)
    lw = mpl.rcParams["axes.linewidth"]
    for i, (g, v) in enumerate(zip(grupos, valores)):
        v = np.asarray(v, dtype=float)
        v = v[~np.isnan(v)]
        c = cores[i % len(cores)]
        parte = ax.violinplot(v, positions=[i], widths=largura, showextrema=False)
        for corpo in parte["bodies"]:
            vert = corpo.get_paths()[0].vertices
            vert[:, 0] = np.clip(vert[:, 0], i, np.inf)  # só a metade direita
            corpo.set_facecolor(c)
            corpo.set_alpha(0.35)
            corpo.set_edgecolor("none")
        ax.boxplot(v, positions=[i - 0.08], widths=0.1, showfliers=False, patch_artist=True,
                   boxprops=dict(facecolor="white", edgecolor=TINTA, linewidth=lw),
                   medianprops=dict(color=TINTA, linewidth=lw * 2),
                   whiskerprops=dict(color=TINTA, linewidth=lw), capprops=dict(linewidth=0))
        x = i - 0.25 + rng.uniform(-0.06, 0.06, size=v.size)
        ax.scatter(x, v, s=mpl.rcParams["lines.markersize"] ** 2 * 0.8, color=c, alpha=0.7,
                   edgecolors="white", linewidths=lw * 0.4, zorder=3)
    nomes = [f"{g}\n(n = {len(np.asarray(v)[~np.isnan(np.asarray(v, dtype=float))])})" if rotulos_n else g
             for g, v in zip(grupos, valores)]
    ax.set_xticks(range(len(grupos)), nomes)
    ax.set_xlim(-0.5, len(grupos) - 0.5)


def kaplan_meier(ax, ax_risco, tempos, eventos, grupos, ordem=None, cores=None, ticks=None,
                 titulo_risco="Número em risco", z=1.96):
    """Curvas de Kaplan–Meier com IC 95% (log-log), marcas de censura e tabela de número em risco.

    ax_risco: eixo abaixo de ax (mesma largura), criado com subplot_mosaic/height_ratios.
    Usa statsmodels (a lifelines não compila em alguns ambientes).
    """
    from statsmodels.duration.survfunc import SurvfuncRight

    tempos, eventos, grupos = (np.asarray(v) for v in (tempos, eventos, grupos))
    ordem = list(ordem) if ordem is not None else list(dict.fromkeys(grupos))
    cores = cores or OKABE_ITO
    ticks = np.asarray(ticks) if ticks is not None else np.linspace(0, tempos.max(), 6).round()
    for i, g in enumerate(ordem):
        t, e = tempos[grupos == g], eventos[grupos == g]
        sf = SurvfuncRight(t, e)
        tt = np.r_[0, sf.surv_times, t.max()]  # curva vai até o último seguimento
        s = np.r_[1, sf.surv_prob, sf.surv_prob[-1]]
        se = np.r_[0, sf.surv_prob_se, sf.surv_prob_se[-1]]
        with np.errstate(divide="ignore", invalid="ignore"):
            ll = np.log(-np.log(s))
            h = z * se / (s * np.abs(np.log(s)))
            lo, hi = np.exp(-np.exp(ll + h)), np.exp(-np.exp(ll - h))
        lo = np.where(np.isfinite(lo), lo, s)
        hi = np.where(np.isfinite(hi), hi, s)
        c = cores[i % len(cores)]
        ax.step(tt, s, where="post", color=c, label=g)
        ax.fill_between(tt, lo, hi, step="post", color=c, alpha=0.15, linewidth=0)
        cens = t[e == 0]
        y_cens = s[np.searchsorted(tt, cens, side="right") - 1]
        ax.plot(cens, y_cens, linestyle="none", marker="|", color=c,
                markersize=mpl.rcParams["lines.markersize"] * 1.2,
                markeredgewidth=mpl.rcParams["axes.linewidth"] * 1.5)
        for x in ticks:
            ax_risco.text(x, i, str(int((t >= x).sum())), ha="center", va="center", color=c)
    ax.set_xticks(ticks)
    ax.set_xlim(ticks[0], ticks[-1])
    ax.set_ylim(0, 1.02)
    ax_risco.set_xlim(ax.get_xlim())
    ax_risco.set_ylim(len(ordem) - 0.4, -0.6)
    ax_risco.set_yticks(range(len(ordem)), ordem)
    for i, rot in enumerate(ax_risco.get_yticklabels()):
        rot.set_color(cores[i % len(cores)])
    ax_risco.tick_params(left=False, bottom=False, labelbottom=False,
                         pad=mpl.rcParams["ytick.labelsize"] * 1.2)
    for lado in ax_risco.spines.values():
        lado.set_visible(False)
    ax_risco.set_title(titulo_risco, loc="left", fontweight="normal",
                       fontsize=mpl.rcParams["ytick.labelsize"], pad=2)


def salvar_pub(fig, caminho_base, p, formatos=None):
    """Exporta no tamanho final em todos os formatos do perfil. Devolve a lista de arquivos."""
    base = Path(caminho_base)
    base.parent.mkdir(parents=True, exist_ok=True)
    feitos = []
    for fmt in formatos or p["formatos"]:
        arq = base.with_suffix(f".{fmt}")
        kw = {}
        if fmt == "tiff":
            kw = dict(dpi=p["dpi"], pil_kwargs={"compression": "tiff_lzw"})
        elif fmt in ("png", "jpg"):
            kw = dict(dpi=p["dpi"])
            if fmt == "jpg":
                kw["pil_kwargs"] = {"quality": 95}
        fig.savefig(arq, **kw)
        feitos.append(arq)
    return feitos
