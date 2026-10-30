# Exemplo testado: painel A (pontos + boxplot + diferença com IC 95%) e painel B (Kaplan–Meier com tabela de risco),
# perfil revista-alto, 2 colunas. Dados simulados. Rode de qualquer pasta: python3 km_raincloud.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # pasta assets/
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.duration.survfunc import SurvfuncRight, survdiff
from statsmodels.duration.hazard_regression import PHReg
from estilo_pub import aplicar_estilo, figura, letra_painel, salvar_pub, raincloud, virgula_decimal, fmt_num, kaplan_meier, OKABE_ITO, TINTA

df = pd.read_csv(Path(__file__).with_name("dados_exemplo.csv"))
grupos = ["Controle", "Intervenção"]
p = aplicar_estilo("revista-alto")
fig, ax = figura(p, largura="2col", altura_mm=78,
                 mosaic=[["A", "B"], ["A", "R"]], height_ratios=[4, 1], width_ratios=[1, 1.35])

# A: raincloud + diferença de médias (IC 95%)
a = ax["A"]
vals = [df.loc[df.grupo == g, "pas"].to_numpy() for g in grupos]
raincloud(a, grupos, vals)
dif = vals[1].mean() - vals[0].mean()
t = stats.ttest_ind(vals[1], vals[0], equal_var=False)
ic = t.confidence_interval(0.95)
a.set_ylabel("Pressão arterial sistólica (mmHg)")
virgula_decimal(a, "y")
a.text(0.5, 1.0, f"Diferença: {fmt_num(dif)} mmHg\n(IC 95% {fmt_num(ic.low)} a {fmt_num(ic.high)})",
       transform=a.transAxes, ha="center", va="top", color=TINTA)
letra_painel(a, "A", p)

# B: Kaplan–Meier
b, r = ax["B"], ax["R"]
kaplan_meier(b, r, df.tempo, df.evento, df.grupo, ordem=grupos, ticks=np.arange(0, 37, 6))
chi, pval = survdiff(df.tempo, df.evento, df.grupo)
cox = PHReg(df.tempo, (df.grupo == "Intervenção").astype(float).to_frame(), status=df.evento).fit()
hr, (hl, hh) = np.exp(cox.params[0]), np.exp(cox.conf_int()[0])
b.set_ylabel("Sobrevida livre de evento"); b.set_xlabel("Meses desde a randomização")
virgula_decimal(b, "y", casas=1)
b.legend(loc="lower left")
p_txt = "p < 0,001" if pval < 0.001 else f"p = {fmt_num(pval, 3)}"
b.text(0.98, 0.98, f"HR {fmt_num(hr, 2)} (IC 95% {fmt_num(hl, 2)}–{fmt_num(hh, 2)})\nlog-rank {p_txt}",
       transform=b.transAxes, ha="right", va="top", color=TINTA)
letra_painel(b, "B", p)
print(salvar_pub(fig, "saida/km_raincloud_py", p))
