# Figuras em R (só com gatilho do usuário)

## Preparação

- **Rode sempre em UTF-8:** `LANG=C.UTF-8 Rscript script.R`. Sem isso, "Pressão" vira "Press..o". O `tema_pub.R` tenta corrigir sozinho e avisa se não conseguir.
- Pacotes: o ambiente da nuvem os instala pelo script de configuração (repositório binário da Posit). Para conferir o que existe: `Rscript -e 'rownames(installed.packages())'`. Se faltar pacote e não houver acesso ao CRAN, use a alternativa "só ggplot2" indicada abaixo, ou entregue o script com a prévia em Python (ver SKILL.md, seção 0).

```r
source("<pasta da skill>/assets/tema_pub.R")
perfil <- "revista-alto"
p <- ggplot(df, aes(x, y, colour = grupo)) +
  geom_point(size = tamanho_ponto(perfil)) +
  scale_colour_okabe() +
  theme_pub(perfil)                        # sempre: nunca o tema cinza padrão
salvar_pub(p, "figuras/nome/nome", perfil, largura = "1col", altura_mm = 60)
```

Exemplo completo e testado: `assets/exemplos/km_raincloud.R`, com pontos + boxplot, diferença com IC 95%, Kaplan–Meier com tabela de risco (só `survival` + `ggplot2` + `patchwork`), HR e log-rank.

## Helpers do `tema_pub.R`

| Função | Para quê |
|---|---|
| `theme_pub(perfil, grade = "nenhuma"/"y"/"x"/"xy")` | Tema da casa no tamanho de fonte do perfil |
| `scale_colour_okabe()`, `scale_fill_okabe()` | Paleta Okabe–Ito |
| `linha_dados(perfil)`, `linha_eixo(perfil)` | Espessuras (`linewidth`) coerentes com o perfil |
| `tamanho_ponto(perfil)`, `tamanho_texto(perfil, fator)` | `size` para pontos e para `geom_text`/`annotate` |
| `rotulo_num("pt", casas)` | Vírgula decimal e sinal de menos nos eixos (`labels =`) |
| `fmt_num(v, casas, "pt")` | Números para subtítulos e anotações |
| `arredondar(v, casas)` | Metade para longe do zero (igual ao Python) |
| `degraus(d, x, grupo)` | Dados em degrau para `geom_ribbon` (IC de KM) |
| `salvar_pub(plot, base, perfil, largura, altura_mm)` | PDF (cairo, fontes embutidas), TIFF LZW e PNG via `ragg` |

## Pacotes por tipo de gráfico

| Tipo | Pacote recomendado | Alternativa só com ggplot2 |
|---|---|---|
| Raincloud | `ggdist::stat_halfeye(adjust = .6, width = .6, justification = -.2, .width = 0)` + `geom_boxplot(width = .12)` + `geom_jitter` | `geom_jitter` + `geom_boxplot(position = position_nudge(x = .28))` (como no exemplo) |
| Ridgeline | `ggridges::geom_density_ridges()` | facetas com `geom_density` |
| Kaplan–Meier | `ggsurvfit::survfit2()` + `ggsurvfit()` + `add_confidence_interval()` + `add_censor_mark()` + `add_risktable()` | `survival::survfit` + `geom_step` + tabela de risco com `patchwork` (exemplo) |
| Incidência acumulada (riscos competitivos) | `tidycmprsk::cuminc()` + `ggsurvfit::ggcuminc()` | — |
| Forest plot (regressão, subgrupos) | `forestploter::forest()` ou ggplot manual: `geom_pointrange` + `geom_vline(xintercept = 1)` + `scale_x_log10()` + colunas de texto com `patchwork` | ggplot manual |
| Meta-análise | `meta::metabin`/`metagen` → `meta::forest()` e `meta::funnel()` (gráficos em grid/base: exporte com `ragg::agg_tiff` direto, sem ggsave) | — |
| ROC | `pROC::roc()` + `pROC::ci.auc()` + `pROC::ggroc()` com `+ theme_pub()` e `coord_equal()` | — |
| Correlação | `geom_tile` + `scale_fill_distiller(palette = "RdBu", limits = c(-1, 1))` + `geom_text(label = fmt_num(r, 2))` | igual |
| Heatmap agrupado | `pheatmap` ou `ComplexHeatmap` (Bioconductor) | `geom_tile` com a ordem vinda de `hclust` |
| Streamgraph (pôster ou slide) | `ggstream::geom_stream()` | `geom_area` |
| Alluvial | `ggalluvial` | — |
| Rótulos sem sobreposição | `ggrepel::geom_text_repel()` | — |
| Texto com formatação (itálico, cor) | `ggtext::element_markdown()` | — |
| Mapas do Brasil | `geobr::read_state()` / `read_municipality()` + `sf` + `geom_sf(aes(fill = taxa), colour = "white", linewidth = .1)` + `scale_fill_viridis_c()` + `theme_void()` com a fonte do perfil | malhas do IBGE com `sf::st_read()` |
| Fluxograma CONSORT | `consort::consort_plot()` | `DiagrammeR` |
| PRISMA 2020 | `PRISMA2020::PRISMA_flowdiagram()` | — |
| Painéis | `patchwork`: `(p1 \| p2) / p3 + plot_annotation(tag_levels = "A")` | — |

## Armadilhas conhecidas (vistas nos testes)

- **Eixo arredondado mente:** `rotulo_num("pt", 1)` com as quebras padrão do ggplot (0; 0,25; 0,5…) imprime "0,2 / 0,5 / 0,8". Sempre passe `breaks` compatíveis com as casas.
- **Censuras na legenda:** use `show.legend = FALSE` no `geom_point` das censuras, senão a legenda vira "+".
- **Números cortados nas bordas** (tabela de risco, rótulos no fim das linhas): `coord_cartesian(clip = "off")`.
- **Anotação saindo do painel:** prefira `labs(subtitle = ...)` a `annotate()` perto do topo.
- **IC de sobrevida em diagonal:** o `geom_ribbon` liga os pontos com retas; a curva de KM é em degrau. Use `geom_ribbon(data = degraus(km), ...)` (helper do `tema_pub.R`).
- **Colunas de texto no patchwork** (forest plot com rótulos e HR ao lado): o patchwork não mede texto. Dê às colunas de texto largura em mm, `plot_layout(widths = unit(c(108, 1, 76), c("mm", "null", "mm")))`, e confira que nada encosta na borda.
- **Fonte das anotações:** o `tema_pub.R` já ajusta `geom_text`/`annotate` para a fonte da casa. Se usar `ggrepel` ou `ggtext`, passe `family = fonte_pub()`.
- **Arredondamento:** use `fmt_num()` (metade para longe do zero), nunca `sprintf`, para os números saírem iguais aos da versão em Python.
- **Tamanhos:** `size` de texto no ggplot é em mm. Use `tamanho_texto(perfil)` em vez de números soltos.
- **ggplot2 antigo:** no ggplot2 < 3.5, `legend.position = c(x, y)` funciona; no 3.5+, use `legend.position = "inside"` + `legend.position.inside = c(x, y)`.
- **Aviso "Vectorized input to element_text()"** ao colorir cada rótulo do eixo (tabela de risco): é esperado e funciona. Para evitar o aviso, use `ggtext::element_markdown()` com rótulos coloridos em HTML.
