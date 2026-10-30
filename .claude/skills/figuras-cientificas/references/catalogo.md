# Catálogo: qual gráfico para qual pergunta

Comece pela **pergunta** e pelo **tipo de dado**, nunca pelo gráfico que parece bonito. Cada linha diz quando usar, o que evitar e com que ferramenta fazer em R e em Python.

Fontes de referência para padrões e variações (consultar, nunca copiar código):
- Wickham, *ggplot2: Elegant Graphics for Data Analysis*, 3ª ed. — https://ggplot2-book.org
- Wilke, *Fundamentals of Data Visualization* — https://clauswilke.com/dataviz
- From Data to Viz (árvore de decisão por tipo de dado) — https://www.data-to-viz.com
- R Graph Gallery — https://r-graph-gallery.com ; Python Graph Gallery — https://python-graph-gallery.com
- Cédric Scherer (ggplot2 de alto nível, tutoriais e TidyTuesday) — https://www.cedricscherer.com
- Galeria do matplotlib — https://matplotlib.org/stable/gallery ; do seaborn — https://seaborn.pydata.org/examples

## 1. Comparar grupos (variável contínua)

| Situação | Gráfico | Evitar |
|---|---|---|
| n pequeno (< ~30 por grupo) | **Pontos individuais** + média ou mediana e IC 95% | Barra com erro ("dynamite plot"): esconde a distribuição (Weissgerber et al., *PLoS Biol* 2015) |
| n médio | **Boxplot + pontos** (jitter) ou **raincloud** (meia densidade + box + pontos) | Violino sozinho com n pequeno |
| n grande | **Raincloud**, violino + box, ou densidades sobrepostas | Pontos sobrepostos sem transparência |
| Antes e depois / pareado | **Linhas ligando os pares** + média | Dois boxplots independentes (perde o pareamento) |
| Muitos grupos | **Ridgeline** (densidades empilhadas) ou pontos ordenados | 15 boxplots lado a lado sem ordem |

- R: `geom_jitter`/`geom_point` + `stat_summary`; `ggdist::stat_halfeye` (raincloud); `ggridges::geom_density_ridges`.
- Python: `seaborn.stripplot`/`boxplot`/`violinplot`; raincloud = `violinplot` cortado ao meio + `boxplot` estreito + `stripplot` (ver `python.md`).

## 2. Proporções e contagens

| Situação | Gráfico | Evitar |
|---|---|---|
| Proporção por grupo | **Pontos com IC 95%** (Wilson) ou barras **com o eixo começando em 0** | Pizza com mais de 3 fatias |
| Composição (partes de um todo) | **Barras empilhadas 100%**, com poucas categorias | Pizza 3D, rosca com 8 fatias |
| Escala Likert | **Barras divergentes** centradas no neutro | Barras empilhadas sem centro |
| Fluxo entre categorias | **Alluvial / Sankey** | Tabela cruzada gigante numa figura |

- R: `geom_col`, `geom_pointrange`; `ggalluvial`.
- Python: `ax.barh`, `ax.errorbar`; Sankey em matplotlib (`matplotlib.sankey`) só para casos simples.

## 3. Relação entre variáveis

| Situação | Gráfico | Evitar |
|---|---|---|
| Duas contínuas | **Dispersão** + reta ou curva ajustada com IC | Linha ligando pontos não ordenados |
| Muitos pontos | Dispersão com transparência, **hexbin** ou densidade 2D | 10 mil pontos opacos |
| Terceira variável | Cor (categórica) ou tamanho (contínua), **ou facetas** | Cor e tamanho e forma ao mesmo tempo |
| Matriz de correlação | **Heatmap triangular** com paleta divergente centrada em 0 e valores escritos | Paleta arco-íris; matriz completa duplicada |
| Muitas variáveis × amostras | **Heatmap** com agrupamento (dendrograma) e escala padronizada | Heatmap sem escala de cor explicada |

- R: `geom_point`, `geom_smooth(method = "lm")`, `geom_hex`, `facet_wrap`; heatmap com `geom_tile`.
- Python: `ax.scatter`, `seaborn.regplot`, `ax.hexbin`, `seaborn.heatmap` / `seaborn.clustermap`.

## 4. Tempo

| Situação | Gráfico | Evitar |
|---|---|---|
| Série temporal | **Linhas** com rótulo direto no fim de cada série | Legenda longe das linhas |
| Série com incerteza | Linha + **faixa de IC** (ribbon) | Barras de erro em cada ponto de uma série longa |
| Composição ao longo do tempo | **Área empilhada**; para destaque narrativo em pôster ou slide, **streamgraph** | Streamgraph em artigo (dificulta ler valores exatos) |
| Taxas antes e depois de uma intervenção | **Série interrompida** com a linha da intervenção marcada | |

- R: `geom_line`, `geom_ribbon`, `geom_area`; streamgraph com `ggstream`.
- Python: `ax.plot`, `ax.fill_between`, `ax.stackplot` (com `baseline="wiggle"` vira streamgraph).

## 5. Pesquisa clínica e epidemiológica

| Situação | Gráfico | Detalhes obrigatórios |
|---|---|---|
| Tempo até evento | **Kaplan–Meier** | Tabela de número em risco abaixo do eixo, marcas de censura, IC (faixa), HR com IC 95% e p do log-rank na figura ou na legenda, eixo x em unidades claras |
| Incidência acumulada com riscos competitivos | **Curva de incidência acumulada** (Aalen–Johansen) | Não usar 1 − KM quando há risco competitivo |
| Efeitos de vários subgrupos ou variáveis | **Forest plot** | Linha de nulidade (1 para OR/HR/RR, 0 para diferença), escala log para razões, colunas com n e estimativa (IC) |
| Meta-análise | **Forest plot** com peso dos estudos (tamanho do quadrado) e diamante do efeito combinado; **funnel plot** para viés de publicação | I² e modelo (fixo ou aleatório) informados |
| Desempenho diagnóstico | **Curva ROC** com AUC (IC 95%) e diagonal de referência; calibração para modelos preditivos | Eixos quadrados (proporção 1:1) |
| Fluxo de participantes | **Fluxograma CONSORT / STROBE / PRISMA 2020** | Números em cada caixa e exclusões com motivo |
| Distribuição espacial | **Mapa coroplético** (taxa por área) com classes bem escolhidas e paleta sequencial | Mapear contagens absolutas (mapeia população, não risco); usar taxas, de preferência suavizadas para áreas pequenas |
| Pontos no mapa | Mapa de pontos ou **densidade (calor)** | Calor sem dizer o que a intensidade representa |
| Diagrama causal | **DAG** | Usar a skill `dag-development` |

- R: `survival` + `ggsurvfit` (KM com tabela de risco); `forestploter` ou ggplot manual (forest); `meta::forest` e `meta::funnel` (meta-análise); `pROC`; `sf` + `geobr` (malhas oficiais do Brasil); `consort` ou `DiagrammeR` (fluxogramas); `PRISMA2020`.
- Python: KM com `statsmodels.duration.survfunc.SurvfuncRight` (a `lifelines` não compila em alguns ambientes); forest plot manual com `ax.errorbar`; ROC com `sklearn.metrics.roc_curve`; mapas com `geopandas` + `geobr`; fluxogramas com `matplotlib.patches` ou Graphviz.

## 6. Combinações em painéis

- Uma figura com painéis A, B, C… quando os painéis contam **uma** história. Painéis independentes viram figuras separadas.
- Alinhar eixos que comparam a mesma variável; mesma escala quando a comparação é direta.
- R: `patchwork` (`p1 + p2 + plot_annotation(tag_levels = "A")`). Python: `plt.subplots` / `subplot_mosaic` + `letra_painel()` do `estilo_pub.py`.

## Sinais de que o gráfico escolhido está errado

- Precisa de mais de três frases na legenda para ser entendido.
- O leitor precisa comparar alturas de barras empilhadas no meio da pilha.
- Eixo y que não começa em 0 em gráfico de barras.
- Duas escalas y no mesmo painel (eixo duplo): quase sempre engana. Use dois painéis.
- Cor sendo a única forma de distinguir grupos.
