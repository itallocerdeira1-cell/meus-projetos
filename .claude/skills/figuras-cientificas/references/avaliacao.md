# Avaliação antes da entrega

Toda figura passa pelos seis critérios abaixo. Cada um é **aprovado** ou **reprovado**, com uma linha de motivo. Uma figura com qualquer critério reprovado **não é entregue**: corrija, renderize de novo, olhe de novo e reavalie.

Avalie **olhando o PNG renderizado no tamanho final**, não o código. Os defeitos mais comuns só aparecem na imagem: texto cortado, sobreposição, acento quebrado, marcação arredondada errada.

## Os seis critérios

### 1. Fidelidade aos dados
- Todo número na figura (médias, IC, HR, n, p) sai do script, a partir dos dados. Nada digitado à mão.
- Os n batem com os dados (contar de novo).
- Eixos sem cortes enganosos; barras começam em 0; razões em escala log.
- Marcações de eixo corretas depois da formatação (0,25 não pode ter virado "0,2").

### 2. Estatística correta
- Efeito com IC 95% presente quando há comparação.
- As barras de erro estão identificadas (DP, EP ou IC) na legenda.
- p-valor só para teste pré-especificado, com valor exato e correção para múltiplas comparações quando couber.
- Teste adequado ao desenho (pareado × independente, normalidade, censura).
- Taxas em vez de contagens quando os denominadores diferem.

### 3. Conformidade com o destino
- Formato, dimensões, resolução, limite de MB, cor ou P&B e número de figuras conforme o edital ou a norma.
- Se não houve edital ou norma: perfil padrão aplicado e presunção registrada.
- Conferir o arquivo final: `python3 -c "from PIL import Image; im = Image.open('x.tiff'); print(im.size, im.info.get('dpi'))"` e o tamanho em MB.

### 4. Legibilidade no tamanho final
- Nenhum texto abaixo da fonte mínima do perfil.
- Nada cortado, nada sobreposto (rótulos, legenda sobre dados, anotações).
- Acentos e caracteres especiais corretos (ç, ã, −, –, ≥).
- `poster` e `slide`: a mensagem principal é entendida em 5 segundos, de longe.

### 5. Acessibilidade
- Paleta segura para daltônicos (Okabe–Ito, viridis, cividis); sem vermelho × verde como único contraste; sem arco-íris.
- Grupos distinguíveis também sem cor, quando o destino pode imprimir em P&B (forma, tipo de linha ou rótulo direto).
- Contraste de texto suficiente (texto escuro em fundo claro ou o inverso).

### 6. Adequação ao nível do destino
- `revista-*`: dados completos e incerteza à mostra; painéis coerentes; sem título interno; vetorial limpo.
- `resumo`: entendida sozinha e em tamanho pequeno; uma mensagem; funciona em P&B.
- `poster` / `eposter`: hierarquia clara; elementos reduzidos ao essencial; modo editorial sem distorcer escala nem incerteza.
- `slide`: uma mensagem; texto ≥ 18 pt; funciona no fundo do slide.
- Pergunta final: **esta figura estaria à altura do evento ou da revista ao lado das melhores figuras publicadas ali?** Se não, diga o que falta.

## Modelo do `avaliacao.md` (salvar na pasta da figura)

```markdown
# Avaliação — <nome da figura>

- **Destino:** <perfil> — <evento/revista>
- **Normas usadas:** <link ou "padrão do perfil; presumido: ...">
- **Linguagem:** Python | R (<motivo>)
- **Arquivos:** <nome>.pdf, <nome>.tiff (W × H px, 600 dpi, X MB), <nome>.png

| Critério | Resultado | Observação |
|---|---|---|
| 1. Fidelidade aos dados | ✅ Aprovado | |
| 2. Estatística correta | ✅ Aprovado | |
| 3. Conformidade com o destino | ✅ Aprovado | |
| 4. Legibilidade no tamanho final | ✅ Aprovado | |
| 5. Acessibilidade | ✅ Aprovado | |
| 6. Adequação ao nível do destino | ✅ Aprovado | |

**Correções feitas durante a avaliação:** <lista do que estava errado na primeira versão e foi corrigido>

## Legenda pronta

**Figura N.** <Título-frase com a conclusão.> (A) <descrição do painel, n, o que os pontos, caixas e barras representam>. (B) <...>. <Teste usado, IC, software e versão.>
```
