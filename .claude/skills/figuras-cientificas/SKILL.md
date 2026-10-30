---
name: figuras-cientificas
description: Cria, refaz e avalia figuras científicas (gráficos, mapas, curvas de sobrevida, forest plots, heatmaps, fluxogramas) em Python ou R, ajustadas ao destino - artigo em revista, resumo de congresso, pôster impresso, e-pôster ou slide. Use sempre que o usuário pedir um gráfico, figura, plot ou mapa de dados de pesquisa, quiser melhorar uma figura existente, adaptar uma figura para pôster/slide/revista, ou perguntar qual gráfico usar. Python é o padrão; R só quando o usuário pedir R ("em R", "código R", "versão em R", "ggplot", "RStudio").
---

# Figuras científicas

Uma figura boa diz uma coisa só, com os dados à mostra, no tamanho em que vai ser vista. Esta skill faz a figura passar por triagem, curadoria, construção e avaliação antes de ser entregue.

## 0. Linguagem

- **Python é o padrão.** Use `assets/estilo_pub.py` e `references/python.md`.
- **R só com gatilho do usuário**: "em R", "código R", "versão em R", "ggplot", "rodar no R/RStudio". Use `assets/tema_pub.R` e `references/r.md`.
- Se o usuário pediu R e o R não estiver disponível (`Rscript --version` falha) ou um pacote necessário não instalar, entregue o script `.R` completo e uma prévia feita em Python, dizendo com clareza que a figura final é a que sair do R. Nunca apresente a prévia como se fosse a saída do R.

## 1. Triagem do destino

Descubra para onde a figura vai e leia `references/destinos.md`. Os seis perfis são `revista-alto`, `revista-nacional`, `resumo`, `poster`, `eposter` e `slide`.

1. Se o destino não estiver claro, pergunte. É a primeira pergunta, porque muda tudo.
2. Peça o edital do evento ou as normas da revista (link ou PDF) e leia. Extraia: número máximo de figuras, formato de arquivo, tamanho em pixels ou mm, resolução, limite de MB, cor ou escala de cinza, fonte, idioma.
3. Se o usuário não tiver as normas, busque a página oficial de instruções aos autores ou o edital na internet.
4. Se não encontrar, aplique o padrão do perfil e registre no relatório o que foi presumido.

**O que o edital ou a norma mandar vale mais que qualquer padrão desta skill.**

## 2. Entender os dados e a mensagem

- Leia os dados de verdade (cabeçalho, tipos, n por grupo, ausentes, unidades) antes de escolher o gráfico.
- Escreva em uma frase a mensagem da figura ("o grupo B teve mortalidade menor em 30 dias"). Se não couber em uma frase, provavelmente são duas figuras ou uma figura em painéis.
- Confirme qual análise estatística sustenta a figura. Se não houver, pergunte antes de inventar teste.

## 3. Curadoria do tipo de gráfico

Consulte `references/catalogo.md`.

- **Quando há escolha real**, proponha de 1 a 3 opções, cada uma com uma linha dizendo por que serve para esses dados e esse destino, e espere a escolha do usuário.
- **Quando o tipo é óbvio** (tempo até evento → Kaplan–Meier; meta-análise → forest plot), siga direto e diga qual foi a escolha.
- Ajuste ao destino: pôster e slide pedem menos elementos e mensagem mais forte; artigo pede os dados completos e a incerteza à mostra.

## 4. Construção

- Comece **sempre** pelo estilo da casa (`assets/estilo_pub.py` ou `assets/tema_pub.R`), com o perfil do destino. Nunca use o tema cinza padrão do ggplot nem o estilo padrão do matplotlib.
- Siga `references/estilo-e-estatistica.md` para cor, tipografia, rótulos e estatística.
- Idioma e números conforme o destino: português com vírgula decimal para eventos e revistas brasileiras em português; inglês com ponto decimal para publicações internacionais. Pergunte se não estiver claro.
- O script precisa rodar sozinho, do zero, a partir do CSV: sem passos manuais e com semente fixa quando houver aleatoriedade (jitter, simulação).

## 5. Renderizar e olhar

- Exporte no **tamanho final** do perfil (`salvar_pub`). Nunca redimensione depois.
- Abra o PNG com a ferramenta de leitura de imagem e **olhe**: textos cortados, sobreposições, legenda tapando dados, rótulos ilegíveis, cores que se confundem.
- Para pôster e slide, imagine a figura vista a 2 m ou no fundo da sala. Na dúvida, aumente o texto e remova elementos.

## 6. Avaliação

Preencha o relatório de `references/avaliacao.md`: seis critérios, cada um aprovado ou reprovado, com o motivo.

- **Nada é entregue com critério reprovado.** Corrija e avalie de novo.
- Se um critério não puder ser cumprido (o edital exige algo que piora a figura, ou os dados não sustentam a mensagem), diga isso ao usuário em vez de esconder.

## 7. Entrega

Cada figura ganha uma pasta dentro do projeto de trabalho:

```
figuras/<nome-da-figura>/
├── <nome>.py  ou  <nome>.R   # script que gera tudo
├── dados.csv                  # dados usados (ou caminho do original)
├── <nome>.pdf                 # vetorial
├── <nome>.tiff                # 600 dpi (revistas) ou conforme a norma
├── <nome>.png                 # para conferência e slides
└── avaliacao.md               # relatório da avaliação + legenda pronta
```

Formatos e resolução seguem o perfil e a norma; tire os que o destino não usa. Na resposta, diga em poucas linhas qual foi o perfil, a escolha de gráfico, o que foi presumido e o resultado da avaliação. Termine com a legenda pronta.

## Outras skills

- Montar o pôster: `pptx-posters`. Montar slides: `frontend-slides` ou `pptx`. Texto do resumo ou artigo: `escrita-academica`.
- Texto alternativo da figura (exigido por algumas revistas): `alt-text`.
- Diagrama causal (DAG): `dag-development`.
- Tamanho de amostra: `statistical-power`.
