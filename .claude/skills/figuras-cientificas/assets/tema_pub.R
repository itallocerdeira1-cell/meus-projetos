# Estilo da casa para figuras científicas em ggplot2.
#
# Uso:
#   source("<pasta da skill>/assets/tema_pub.R")
#   p <- ggplot(...) + ... + theme_pub("revista-alto") + scale_colour_okabe()
#   salvar_pub(p, "figuras/minha-figura/minha-figura", "revista-alto", largura = "1col", altura_mm = 60)
#
# Pacotes: ggplot2, scales, ragg (systemfonts vem com ragg).

library(ggplot2)

# Sem UTF-8, acentos viram ".." nas figuras. Rode com LANG=C.UTF-8 (ou en_US.UTF-8).
if (!isTRUE(l10n_info()[["UTF-8"]])) {
  invisible(Sys.setlocale("LC_CTYPE", "C.UTF-8"))
  if (!isTRUE(l10n_info()[["UTF-8"]])) {
    warning("A sessão do R não está em UTF-8: acentos vão sair errados. Rode com LANG=C.UTF-8.")
  }
}

# Perfis de destino (references/destinos.md). Fontes em pt no tamanho final.
perfis_pub <- list(
  "revista-alto"     = list(largura_mm = 89,  largura2_mm = 183, fonte = 7,  fonte_min = 5,  linha = 0.5,  dpi = 600, formatos = c("pdf", "tiff", "png")),
  "revista-nacional" = list(largura_mm = 85,  largura2_mm = 175, fonte = 8,  fonte_min = 6,  linha = 0.5,  dpi = 600, formatos = c("pdf", "tiff", "png")),
  "resumo"           = list(largura_mm = 160, largura2_mm = 160, fonte = 9,  fonte_min = 7,  linha = 0.75, dpi = 300, formatos = c("png", "jpg", "pdf")),
  "poster"           = list(largura_mm = 280, largura2_mm = 560, fonte = 28, fonte_min = 24, linha = 1.5,  dpi = 300, formatos = c("pdf", "png")),
  "eposter"          = list(largura_mm = 290, largura2_mm = 290, fonte = 18, fonte_min = 14, linha = 1.25, dpi = 200, formatos = c("png", "pdf")),
  "slide"            = list(largura_mm = 290, largura2_mm = 290, fonte = 20, fonte_min = 18, linha = 1.5,  dpi = 200, formatos = c("png", "pdf"))
)

# Okabe & Ito (2008): segura para daltonismo. Amarelo por último (pouco contraste em fundo branco).
okabe_ito <- c("#0072B2", "#D55E00", "#009E73", "#E69F00", "#56B4E9", "#CC79A7", "#000000", "#F0E442")
cinza_pub <- "#9A9A9A"
tinta_pub <- "#333333"

fonte_pub <- function() {
  candidatas <- c("Arial", "Helvetica", "Liberation Sans", "DejaVu Sans")
  if (requireNamespace("systemfonts", quietly = TRUE)) {
    disponiveis <- unique(systemfonts::system_fonts()$family)
    achada <- candidatas[candidatas %in% disponiveis]
    if (length(achada)) return(achada[1])
  }
  "sans"
}

# Espessuras: o perfil está em pt; o ggplot2 usa mm (1 mm = .pt pontos).
linha_eixo <- function(perfil) perfis_pub[[perfil]]$linha / .pt
linha_dados <- function(perfil) perfis_pub[[perfil]]$linha * 2.5 / .pt
tamanho_ponto <- function(perfil) perfis_pub[[perfil]]$fonte * 0.6 / .pt
tamanho_texto <- function(perfil, fator = 1) perfis_pub[[perfil]]$fonte * fator / .pt  # para geom_text/annotate

theme_pub <- function(perfil = "revista-alto", grade = c("nenhuma", "y", "x", "xy")) {
  grade <- match.arg(grade)
  p <- perfis_pub[[perfil]]
  f <- p$fonte
  tick <- max(f * 0.9, p$fonte_min)
  lw <- p$linha / .pt
  linha_grade <- element_line(colour = "#E5E5E5", linewidth = lw * 0.8)

  theme_classic(base_size = f, base_family = fonte_pub()) +
    theme(
      axis.line = element_line(colour = tinta_pub, linewidth = lw),
      axis.ticks = element_line(colour = tinta_pub, linewidth = lw),
      axis.ticks.length = unit(f * 0.4, "pt"),
      axis.text = element_text(colour = tinta_pub, size = tick),
      axis.title = element_text(colour = tinta_pub, size = f),
      legend.text = element_text(colour = tinta_pub, size = tick),
      legend.title = element_text(colour = tinta_pub, size = f),
      legend.background = element_blank(),
      legend.key = element_blank(),
      legend.key.height = unit(f * 1.3, "pt"),
      legend.key.width = unit(f * 1.8, "pt"),
      plot.title = element_text(face = "bold", size = f * 1.15, hjust = 0),
      plot.title.position = "plot",
      plot.subtitle = element_text(size = f, colour = tinta_pub, hjust = 0),
      plot.caption = element_text(size = tick, colour = tinta_pub, hjust = 0),
      plot.caption.position = "plot",
      plot.tag = element_text(face = "bold", size = f * 1.15),
      strip.background = element_blank(),
      strip.text = element_text(face = "bold", size = f, hjust = 0, colour = tinta_pub),
      panel.grid.major.y = if (grade %in% c("y", "xy")) linha_grade else element_blank(),
      panel.grid.major.x = if (grade %in% c("x", "xy")) linha_grade else element_blank(),
      plot.margin = margin(f * 0.5, f * 0.8, f * 0.5, f * 0.5)
    )
}

# geom_text/annotate não herdam a fonte do tema: alinhar os padrões com o estilo da casa.
update_geom_defaults("text", list(family = fonte_pub(), colour = tinta_pub))
update_geom_defaults("label", list(family = fonte_pub(), colour = tinta_pub))

# Transforma uma curva em degrau para geom_ribbon (que interpola em diagonal).
# Use nas faixas de IC de Kaplan–Meier e incidência acumulada: d precisa das colunas x e grupo.
degraus <- function(d, x = "t", grupo = "grupo") {
  partes <- lapply(split(d, d[[grupo]], drop = TRUE), function(g) {
    g <- g[order(g[[x]]), ]
    n <- nrow(g)
    if (n < 2) return(g)
    idx <- c(rbind(seq_len(n - 1), seq_len(n - 1)), n)
    out <- g[idx, ]
    out[[x]] <- c(rbind(g[[x]][-n], g[[x]][-1]), g[[x]][n])
    out
  })
  do.call(rbind, partes)
}

scale_colour_okabe <- function(...) scale_colour_manual(values = okabe_ito, ...)
scale_fill_okabe <- function(...) scale_fill_manual(values = okabe_ito, ...)

# Números com vírgula decimal (destinos em português) ou ponto (inglês).
# Atenção: `casas` arredonda as marcações. Defina `breaks` compatíveis com as casas
# (ex.: breaks = seq(0, 1, 0.2) com casas = 1); senão 0,25 vira "0,2" e o eixo mente.
rotulo_num <- function(idioma = "pt", casas = NULL) {
  acc <- if (is.null(casas)) NULL else 10^-casas
  if (idioma == "pt") {
    scales::label_number(accuracy = acc, decimal.mark = ",", big.mark = ".", style_negative = "minus")
  } else {
    scales::label_number(accuracy = acc, big.mark = ",", style_negative = "minus")
  }
}

# Arredonda a metade para longe do zero (5,25 -> 5,3), igual ao arredondar() do estilo_pub.py.
# Tira antes o ruído de ponto flutuante (5,2500000001), para os dois lados darem o mesmo número.
arredondar <- function(v, casas = 1) {
  m <- 10^casas
  limpo <- as.numeric(formatC(abs(v), digits = 15, format = "g"))
  sign(v) * floor(limpo * m + 0.5) / m
}

fmt_num <- function(v, casas = 1, idioma = "pt") {
  s <- formatC(arredondar(v, casas), format = "f", digits = casas)
  s <- sub("-", "−", s, fixed = TRUE)
  if (idioma == "pt") chartr(".", ",", s) else s
}

# Exporta no tamanho final em todos os formatos do perfil. Devolve os caminhos.
salvar_pub <- function(plot, caminho_base, perfil = "revista-alto", largura = "1col",
                       altura_mm = NULL, formatos = NULL) {
  p <- perfis_pub[[perfil]]
  w <- switch(as.character(largura), "1col" = p$largura_mm, "2col" = p$largura2_mm, as.numeric(largura))
  h <- if (is.null(altura_mm)) w * 0.62 else altura_mm
  dir.create(dirname(caminho_base), recursive = TRUE, showWarnings = FALSE)
  formatos <- if (is.null(formatos)) p$formatos else formatos
  feitos <- character()
  for (fmt in formatos) {
    arq <- paste0(caminho_base, ".", fmt)
    switch(fmt,
      pdf  = ggsave(arq, plot, width = w, height = h, units = "mm", device = grDevices::cairo_pdf),
      tiff = ggsave(arq, plot, width = w, height = h, units = "mm", dpi = p$dpi,
                    device = ragg::agg_tiff, compression = "lzw"),
      png  = ggsave(arq, plot, width = w, height = h, units = "mm", dpi = p$dpi, device = ragg::agg_png),
      jpg  = ggsave(arq, plot, width = w, height = h, units = "mm", dpi = p$dpi,
                    device = ragg::agg_jpeg, quality = 95),
      stop("Formato não suportado: ", fmt)
    )
    feitos <- c(feitos, arq)
  }
  invisible(feitos)
}
