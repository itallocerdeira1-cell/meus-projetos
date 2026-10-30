# Exemplo testado: mesma figura do km_raincloud.py, só com ggplot2 + survival + patchwork (sem ggsurvfit/ggdist).
# Rode a partir da pasta assets/exemplos/:  LANG=C.UTF-8 Rscript km_raincloud.R
source("../tema_pub.R")
library(survival); library(patchwork)
perfil <- "revista-alto"
df <- read.csv("dados_exemplo.csv")
df$grupo <- factor(df$grupo, levels = c("Controle", "Intervenção"))
set.seed(1)

# A: pontos + boxplot + n no eixo
n_por <- table(df$grupo)
rot <- setNames(paste0(names(n_por), "\n(n = ", n_por, ")"), names(n_por))
ic <- t.test(pas ~ grupo, data = df)$conf.int * -1
dif <- diff(tapply(df$pas, df$grupo, mean))
pA <- ggplot(df, aes(grupo, pas, colour = grupo)) +
  geom_jitter(width = 0.12, alpha = 0.7, size = tamanho_ponto(perfil), shape = 16) +
  geom_boxplot(aes(group = grupo), width = 0.18, fill = "white", colour = tinta_pub, outlier.shape = NA,
               linewidth = linha_eixo(perfil), position = position_nudge(x = 0.28)) +
  scale_x_discrete(labels = rot) + scale_y_continuous(labels = rotulo_num("pt"), expand = expansion(0.04)) +
  scale_colour_okabe(guide = "none") +
  labs(x = NULL, y = "Pressão arterial sistólica (mmHg)",
       subtitle = paste0("Diferença: ", fmt_num(dif), " mmHg (IC 95% ", fmt_num(min(ic)), " a ", fmt_num(max(ic)), ")")) + theme_pub(perfil)

# B: Kaplan–Meier com survival + ggplot (sem ggsurvfit)
fit <- survfit(Surv(tempo, evento) ~ grupo, data = df, conf.type = "log-log")
s <- summary(fit, censored = TRUE)
km <- data.frame(tempo = s$time, sobrev = s$surv, lo = s$lower, hi = s$upper,
                 cens = s$n.event == 0, grupo = sub("grupo=", "", s$strata))
inicio <- data.frame(tempo = 0, sobrev = 1, lo = 1, hi = 1, cens = FALSE, grupo = levels(df$grupo))
km <- rbind(inicio, km); km$grupo <- factor(km$grupo, levels(df$grupo))
cox <- coxph(Surv(tempo, evento) ~ grupo, data = df)
hr <- exp(c(coef(cox), confint(cox)))
p_lr <- 1 - pchisq(survdiff(Surv(tempo, evento) ~ grupo, data = df)$chisq, 1)
quebras <- seq(0, 36, 6)
pB <- ggplot(km, aes(tempo, sobrev, colour = grupo, fill = grupo)) +
  geom_ribbon(data = degraus(km, x = "tempo"), aes(ymin = lo, ymax = hi), alpha = 0.15, colour = NA) +
  geom_step(linewidth = linha_dados(perfil)) +
  geom_point(data = subset(km, cens), shape = 124, size = tamanho_ponto(perfil) * 0.9, show.legend = FALSE) +
  annotate("text", x = 36, y = 1, hjust = 1, vjust = 1, colour = tinta_pub, size = tamanho_texto(perfil),
           label = paste0("HR ", fmt_num(hr[1], 2), " (IC 95% ", fmt_num(hr[2], 2), "–", fmt_num(hr[3], 2),
                          ")\nlog-rank p = ", fmt_num(p_lr, 3))) +
  scale_x_continuous(breaks = quebras, limits = c(0, 36), expand = expansion(0)) +
  scale_y_continuous(limits = c(0, 1.02), breaks = seq(0, 1, 0.2), labels = rotulo_num("pt", 1), expand = expansion(0)) +
  scale_colour_okabe(name = NULL) + scale_fill_okabe(guide = "none") +
  labs(x = "Meses desde a randomização", y = "Sobrevida livre de evento") +
  theme_pub(perfil) + theme(legend.position = c(0.02, 0.05), legend.justification = c(0, 0))

risco <- do.call(rbind, lapply(levels(df$grupo), function(g)
  data.frame(grupo = g, tempo = quebras, n = sapply(quebras, function(x) sum(df$tempo[df$grupo == g] >= x)))))
risco$grupo <- factor(risco$grupo, rev(levels(df$grupo)))
pR <- ggplot(risco, aes(tempo, grupo, label = n, colour = grupo)) +
  geom_text(size = tamanho_texto(perfil, 0.9)) + coord_cartesian(clip = "off") +
  scale_x_continuous(limits = c(0, 36), expand = expansion(0)) +
  scale_colour_manual(values = setNames(okabe_ito[1:2], levels(df$grupo)), guide = "none") +
  labs(title = "Número em risco", x = NULL, y = NULL) + theme_pub(perfil) +
  theme(axis.line = element_blank(), axis.ticks = element_blank(), axis.text.x = element_blank(),
        axis.text.y = element_text(colour = rev(okabe_ito[1:2]), margin = margin(r = perfis_pub[[perfil]]$fonte)),
        plot.title = element_text(face = "plain", size = perfis_pub[[perfil]]$fonte * 0.9))

fig <- (pA | (pB / pR + plot_layout(heights = c(4, 1)))) +
  plot_layout(widths = c(1, 1.35)) + plot_annotation(tag_levels = list(c("A", "B", "")))
print(salvar_pub(fig, "saida/km_raincloud_r", perfil, largura = "2col", altura_mm = 78))
