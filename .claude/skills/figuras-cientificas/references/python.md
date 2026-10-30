# Figuras em Python (padrão)

## Preparação

```bash
pip install matplotlib seaborn scipy statsmodels    # base
pip install geopandas geobr scikit-learn            # mapas do Brasil e ROC, quando precisar
```

- A `lifelines` pode não compilar (dependência `autograd-gamma`). A sobrevida usa `statsmodels` e já está pronta em `kaplan_meier()`.
- Rode scripts que leem dados de terceiros com `python3 -I`.

```python
import sys
sys.path.insert(0, "<pasta da skill>/assets")
from estilo_pub import (aplicar_estilo, figura, letra_painel, salvar_pub, virgula_decimal, fmt_num,
                        raincloud, kaplan_meier, OKABE_ITO, CINZA, TINTA)

p = aplicar_estilo("revista-alto")          # sempre primeiro: define fontes, linhas e cores do perfil
fig, ax = figura(p, largura="1col", altura_mm=60)
```

Exemplo completo e testado: `assets/exemplos/km_raincloud.py`, com raincloud, diferença com IC 95%, Kaplan–Meier com tabela de risco, HR de Cox e log-rank.

## Helpers do `estilo_pub.py`

| Função | Para quê |
|---|---|
| `aplicar_estilo(perfil)` | Define o estilo da casa e devolve o perfil (fonte, linhas, dpi, formatos) |
| `figura(p, largura, altura_mm, mosaic=..., height_ratios=...)` | Figura no tamanho final (`"1col"`, `"2col"` ou mm); aceita `subplot_mosaic` |
| `letra_painel(ax, "A", p)` | Letra do painel em negrito, à esquerda |
| `virgula_decimal(ax, "xy", casas)` | Vírgula decimal e sinal de menos tipográfico nos eixos |
| `fmt_num(v, casas, idioma)` | Números para anotações (−14,3) |
| `raincloud(ax, grupos, valores)` | Pontos + boxplot + meia densidade, com n no eixo |
| `kaplan_meier(ax, ax_risco, tempos, eventos, grupos, ordem, ticks)` | KM com IC log-log, censuras e tabela de risco |
| `salvar_pub(fig, base, p, formatos)` | Exporta PDF (fontes embutidas), TIFF LZW e PNG no dpi do perfil |

## Receitas por tipo (catálogo → código)

- **Pontos + IC**: `ax.errorbar(x, media, yerr=[media - lo, hi - media], fmt="o", capsize=0)` + `ax.scatter` com jitter (`rng.uniform`, semente fixa).
- **Pareado**: um `ax.plot([0, 1], [antes_i, depois_i], color=CINZA, alpha=.5)` por par, mais a média em destaque.
- **Ridgeline**: um `ax.fill_between` por grupo, deslocado no y; ou `seaborn.FacetGrid` com `kdeplot` e `hspace` negativo.
- **Barras divergentes (Likert)**: `ax.barh` com `left=` acumulado, centralizando a categoria neutra no zero.
- **Dispersão + ajuste**: `seaborn.regplot(..., scatter_kws=dict(alpha=.6), line_kws=dict(color=TINTA))` ou statsmodels para a reta e a faixa de IC.
- **Heatmap de correlação**: `seaborn.heatmap(corr, mask=np.triu(...), cmap="RdBu_r", vmin=-1, vmax=1, center=0, annot=True, fmt=".2f")`. Em português, reformate os textos de `annot` com vírgula.
- **Heatmap agrupado**: `seaborn.clustermap(z, cmap="viridis", ...)` com a escala padronizada (z-score) declarada na barra de cor.
- **Série temporal com IC**: `ax.plot` + `ax.fill_between(alpha=.2)`; rótulo direto com `ax.text(x[-1], y[-1], " Nome", va="center", color=c)`.
- **Streamgraph** (só pôster ou slide): `ax.stackplot(x, ys, baseline="wiggle", colors=...)`, sem eixo y, rótulos dentro das camadas.
- **Forest plot**: um eixo; `ax.errorbar(est, y, xerr=..., fmt="s")` com o tamanho do marcador proporcional ao peso; `ax.axvline(1, ls="--", color=CINZA)`; `ax.set_xscale("log")` para OR/HR/RR; colunas de texto (n, estimativa e IC) com `ax.text` em coordenadas mistas (`ax.get_yaxis_transform()`).
- **Funnel plot**: `ax.scatter(efeito, ep)` com o eixo y invertido e as linhas do funil em ±1,96·EP em volta do efeito combinado.
- **ROC**: `sklearn.metrics.roc_curve` + `roc_auc_score`; IC da AUC por bootstrap (semente fixa, 2000 reamostras); `ax.set_aspect("equal")`; diagonal tracejada.
- **Mapa coroplético do Brasil**: `geobr.read_state()` / `read_municipality(code_muni=UF, year=...)` → `GeoDataFrame.merge` com a taxa → `.plot(column="taxa", cmap="viridis", scheme="quantiles" ou "natural_breaks", legend=True)` (o `scheme` precisa de `mapclassify`). Sem eixos: `ax.set_axis_off()`. Sempre taxa, nunca contagem. Se o `geobr` não baixar (rede bloqueada), use as malhas do IBGE (`geoftp.ibge.gov.br`) com `geopandas.read_file`.
- **Fluxograma (CONSORT/PRISMA)**: caixas com `matplotlib.patches.FancyBboxPatch` e setas com `ax.annotate("", xy=..., xytext=..., arrowprops=dict(arrowstyle="-|>"))`, em coordenadas de 0 a 1; ou Graphviz, se estiver instalado.

## Armadilhas conhecidas

- **Tamanho:** nunca use `bbox_inches="tight"`, porque ele muda o tamanho final. O `layout="constrained"` do `figura()` já cuida das margens.
- **Fontes no PDF:** o `pdf.fonttype = 42` já está no estilo; sem ele, a revista recebe texto convertido em contornos.
- **Vírgula decimal:** `virgula_decimal` muda só as marcações. Anotações, rótulos de barra e `annot` de heatmap precisam de `fmt_num`.
- **Marcações arredondadas:** com `casas=1`, defina `ax.set_yticks` compatíveis (0; 0,2; 0,4…). Senão 0,25 vira "0,2" e o eixo mente.
- **Cores do seaborn:** passe `palette=OKABE_ITO[:k]` explicitamente; algumas funções ignoram o `prop_cycle`.
- **Jitter:** sempre com `np.random.default_rng(semente)` para a figura sair igual em toda execução.
