# Perfis de destino

O que a norma ou o edital mandar vale mais que esta tabela. Os valores abaixo são o **padrão** para quando não há norma, e o ponto de partida para checar a norma quando há.

## Tabela de perfis

| Perfil | Largura padrão | Fonte base | Fonte mínima | Linhas | Resolução | Formatos |
|---|---|---|---|---|---|---|
| `revista-alto` | 89 mm (1 coluna) ou 183 mm (2 colunas) | 7 pt | 5 pt | 0,5 pt | 600 dpi | PDF, TIFF, PNG |
| `revista-nacional` | 85 mm ou 175 mm | 8 pt | 6 pt | 0,5 pt | 600 dpi | PDF, TIFF, PNG |
| `resumo` | 160 mm | 9 pt | 7 pt | 0,75 pt | 300 dpi | PNG, JPG, PDF |
| `poster` | 280 mm (ajustar ao espaço no pôster) | 28 pt | 24 pt | 1,5 pt | 300 dpi | PDF, PNG |
| `eposter` | 290 mm | 18 pt | 14 pt | 1,25 pt | 200 dpi | PNG, PDF |
| `slide` | 290 mm | 20 pt | 18 pt | 1,5 pt | 200 dpi | PNG, PDF |

Os tamanhos em pt valem **no tamanho final impresso ou projetado**. Por isso a figura é sempre exportada já na largura final. Para `eposter` e `slide`, 290 mm é cerca de 85% da largura de um slide 16:9 do PowerPoint (338,7 × 190,5 mm), então as fontes em pt correspondem às do próprio slide.

A altura é decidida por figura. Ponto de partida: largura × 0,62 para um painel único; para painéis empilhados, some as alturas. Revistas costumam limitar a altura à página (em geral 170–240 mm).

## O que muda em cada perfil

### `revista-alto` (Nature, Cell, Lancet, NEJM, JAMA, BMJ, PLOS e similares)
- Mostrar os dados completos e a incerteza: pontos individuais quando n for pequeno, IC 95%, n por grupo.
- Painéis com letras (A, B, C…) em negrito, alinhados à esquerda.
- Sem título dentro da figura: o título vai na legenda.
- Várias revistas médicas de topo (NEJM, JAMA, Lancet) **redesenham as figuras** na produção e pedem arquivos editáveis (PDF/EPS vetorial) e, às vezes, os dados. Entregue o vetorial limpo e o CSV.
- Referências de normas (sempre confira a versão atual):
  - Nature: 89 mm / 183 mm, texto de 5 a 7 pt, fonte sem serifa. https://www.nature.com/nature/for-authors/final-submission
  - Cell Press: 85 mm / 114 mm / 174 mm. https://www.cell.com/figureguidelines
  - Elsevier (geral): 90 mm / 140 mm / 190 mm; ≥ 300 dpi para fotos, 500 dpi para figuras mistas, 1000 dpi para traço. https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions
  - PLOS: largura de 789 a 2250 px a 300 dpi; TIFF ou EPS; Arial, Times ou Symbol, de 8 a 12 pt. https://journals.plos.org/plosone/s/figures

### `revista-nacional` (revistas brasileiras e regionais, SciELO)
- Mesma exigência estatística do `revista-alto`. A diferença costuma ser só de formato.
- Muitas pedem TIFF ou JPG a 300 dpi e figuras em escala de cinza ou que funcionem em cinza. Confira.
- Idioma da figura = idioma do artigo, com vírgula decimal em português.

### `resumo` (submissão de resumo para congresso)
- Em geral cabe **uma** figura ou tabela, às vezes nenhuma. Confira no edital antes de fazer.
- A figura precisa ser entendida sozinha, em tamanho pequeno, dentro da página de submissão ou dos anais. Mensagem única, poucos elementos, rótulos diretos nas séries em vez de legenda.
- Limites comuns nas plataformas: JPG ou PNG, de 1 a 2 MB, largura de 600 a 1500 px. Se o edital der pixels, converta: px = mm ÷ 25,4 × dpi.
- Os anais costumam sair em PDF ou impressos em preto e branco: a figura precisa funcionar em escala de cinza (use formas e tipos de linha, não só cor).

### `poster` (pôster impresso)
- Lido a 1,5–2 m de distância, em segundos. A figura carrega a mensagem; o texto só apoia.
- Texto da figura ≥ 24 pt no tamanho impresso; título do pôster de 72 a 100 pt; corpo de 24 a 32 pt.
- Formatos comuns: A0 (841 × 1189 mm) e banners de 90 × 120 cm. O edital define. A largura da figura depende de quantas colunas o pôster tem: em A0 com 3 colunas, cada coluna tem ~260–270 mm úteis.
- Pode usar o modo **editorial**: cor de destaque para o achado principal, anotação direta ("−32% de mortalidade"), menos eixos e grades. Sem perder a escala nem a incerteza.
- Exportar em PDF vetorial para a gráfica, ou PNG a 300 dpi no tamanho físico real.

### `eposter` (pôster em tela)
- Visto numa TV ou num totem, mais de perto que o pôster impresso, às vezes navegável por toque.
- Formato definido pelo edital: em geral 16:9 horizontal (1920 × 1080) ou vertical (1080 × 1920), em PDF de uma página ou em PPTX.
- Mesma lógica do pôster, com texto ≥ 14 pt no tamanho do slide.

### `slide` (apresentação oral)
- Uma figura, uma mensagem, um slide. O título do slide é a conclusão ("Mortalidade caiu 32% no grupo B"), não o nome da variável.
- Texto ≥ 18 pt, linhas grossas, no máximo 4–5 cores.
- Fundo do slide: a figura precisa funcionar no fundo escolhido. Em fundo escuro, refaça as cores de texto e eixos; não cole uma figura de fundo branco num slide escuro.
- Pense em revelar em etapas: primeiro os eixos, depois o grupo controle, depois o tratamento. Gere uma versão por etapa se for útil.

## Perguntas para extrair do edital ou da norma

1. Quantas figuras são permitidas? Figura e tabela contam juntas?
2. Formato de arquivo? Tamanho máximo em MB?
3. Dimensões em pixels ou mm? Resolução mínima?
4. Cor permitida, ou só preto e branco ou escala de cinza?
5. Fonte e tamanho exigidos?
6. Idioma?
7. Para pôster: tamanho físico, orientação, impresso ou digital?
8. A figura vai inserida no texto ou enviada como arquivo à parte?
