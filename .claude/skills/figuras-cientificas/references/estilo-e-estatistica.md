# Estilo da casa e regras estatísticas

## Estilo visual

O padrão é o visual de revista: fundo branco, sem moldura em volta do painel, só os eixos x e y, grade leve só quando ajuda a ler valores, tipografia sem serifa sóbria e uma cor por ideia. É o mesmo em R e Python, garantido por `assets/tema_pub.R` e `assets/estilo_pub.py`.

### Tipografia
- Sem serifa: Arial → Helvetica → Liberation Sans (métrica igual à Arial) → DejaVu Sans. Os helpers escolhem a primeira disponível.
- Hierarquia: letras dos painéis em negrito e 1,15× a fonte base; títulos de eixo na fonte base; marcações de eixo a 0,9× (nunca abaixo da fonte mínima do perfil).
- Unidades no título do eixo, entre parênteses: "Idade (anos)", "Tempo desde a randomização (meses)".
- Sem texto em diagonal. Rótulos longos → barras na horizontal.
- Rótulo direto nas séries (no fim da linha, ao lado do grupo) é melhor que legenda, sempre que couber.

### Cor
- **Categórica:** Okabe–Ito (Okabe & Ito, 2008), segura para daltônicos. Ordem: `#0072B2` azul, `#D55E00` vermelhão, `#009E73` verde-azulado, `#E69F00` laranja, `#56B4E9` azul-céu, `#CC79A7` rosa, `#F0E442` amarelo (só em fundo escuro), `#000000` preto.
- **Sequencial** (uma grandeza que cresce): viridis, cividis (ótima para daltônicos e impressão) ou uma única matiz clara→escura.
- **Divergente** (desvio em torno de um centro, como correlação ou mudança): azul–branco–vermelho (`RdBu` invertido) centrada no valor neutro.
- **Nunca** arco-íris / jet / rainbow: distorce os dados e não funciona para daltônicos (Crameri et al., *Nat Commun* 2020). Nunca vermelho × verde como único contraste.
- Destaque: um grupo em cor forte e o resto em cinza (`#9A9A9A`) quando a mensagem é sobre aquele grupo. Ótimo em pôster e slide.
- Teste em escala de cinza quando o destino puder imprimir em P&B: diferencie também por forma do ponto ou tipo de linha.

### Elementos
- Pontos: transparência 0,5–0,7 quando houver sobreposição; contorno branco fino ajuda em fundo cheio.
- Linhas de dados mais grossas que os eixos. Eixos e marcações em cinza-escuro (`#333333`), não preto puro.
- Linha de referência (nulidade, meta, intervenção) tracejada e cinza.
- Legenda sem título quando o título é óbvio, e dentro da área vazia do gráfico, ou rótulos diretos.
- Nada de 3D, sombra, gradiente decorativo ou fundo com imagem.

### Modo editorial (só `poster`, `eposter`, `slide`)
- Permitido: título-conclusão, anotação com seta apontando o achado, cor de destaque, remoção de grades, números grandes ("−32%").
- Proibido mesmo no modo editorial: cortar o eixo de barras, omitir a incerteza, mudar a escala para exagerar o efeito.

## Estatística na figura

1. **Mostre o tamanho do efeito com IC 95%.** Diferença de médias, OR, HR ou RR, com o intervalo.
2. **Mostre os dados** quando n for pequeno ou moderado: pontos individuais, não só resumos.
3. **Diga o que as barras de erro são**: DP, EP ou IC 95%, na legenda, sempre. Prefira IC 95%; o EP sozinho é enganoso.
4. **p-valor só quando o teste foi pré-especificado**, com o valor exato (p = 0,032; p < 0,001 abaixo disso), e corrigido para comparações múltiplas (Holm ou Bonferroni; Benjamini–Hochberg para muitos testes exploratórios). Sem estrelinhas soltas: se usar, a legenda define o que cada uma significa.
5. **Não teste o que não foi planejado** só para enfeitar a figura. Se a figura mostra um subgrupo post hoc, a legenda diz "exploratório".
6. **n em toda figura**: por grupo, no eixo ("Controle\n(n = 48)") ou na legenda. Em sobrevida, na tabela de risco.
7. **Escalas honestas:** barras começam em 0; razões (OR, HR, RR) em escala log; eixos iguais quando os painéis se comparam.
8. **Taxas, não contagens**, quando os grupos ou áreas têm tamanhos diferentes. Em mapas, sempre.
9. Arredondamento coerente: o mesmo número de casas decimais na figura e no texto; IC com as mesmas casas que a estimativa.
10. **Não invente análise.** Se a análise não foi feita ou não foi informada, pergunte. Nunca coloque um número na figura que não saia dos dados ou da análise do usuário.

## Referências
- Okabe M, Ito K. Color Universal Design (CUD). 2008. https://jfly.uni-koeln.de/color/
- Weissgerber TL et al. Beyond bar and line graphs: time for a new data presentation paradigm. *PLoS Biol*. 2015;13(4):e1002128.
- Crameri F, Shephard GE, Heron PJ. The misuse of colour in science communication. *Nat Commun*. 2020;11:5444.
- Rougier NP, Droettboom M, Bourne PE. Ten simple rules for better figures. *PLoS Comput Biol*. 2014;10(9):e1003833.
- Wilke CO. *Fundamentals of Data Visualization*. O'Reilly; 2019.
