# Semântica de contagem

## A regra

`bizdays(de, até)` conta os dias úteis no intervalo **semiaberto** `[de, até)`:
inclui `de` e exclui `até`. Não há flags para mudar isso (ADR-0001).

- `bizdays(d, d) == 0`, para qualquer `d`.
- Para `de ≤ até`, é o número de dias úteis `u` com `de ≤ u < até`.
- Para `de > até`, o resultado é negativo. O oráculo (NumPy `busday_count`,
  que é também o comportamento do Polars `business_day_count`) conta, nesse
  caso, os dias úteis em `(até, de]` com sinal trocado — veja
  [o ponto em aberto](#ponto-em-aberto-pares-invertidos).

É a definição usada pela B3 no BUS/252 e por NumPy e Polars.

## Por que `[de, até)`

**BUS/252.** No Brasil, a fração de ano de um título pós ou prefixado é
`DU/252`, onde `DU` é o número de dias úteis entre a liquidação (inclusive) e o
vencimento (exclusive). Um título que liquida numa sexta e vence na segunda
seguinte rende **um** dia útil: o da sexta.

**Acumulação do CDI.** A taxa DI de um dia útil remunera do fechamento desse
dia até o próximo dia útil. O fator acumulado entre `de` e `até` é o produto
dos fatores diários dos dias úteis em `[de, até)`:

$$
F(de, até) = \prod_{u \in [de,\, até)} \left(1 + \mathrm{DI}_u\right)^{1/252}
$$

**Composição de prazos.** Para `a ≤ b ≤ c`, o intervalo semiaberto é aditivo:
`bizdays(a, b) + bizdays(b, c) == bizdays(a, c)`. Com intervalo fechado o dia
`b` seria contado duas vezes.

## Exemplos com o feriado de 12/10/2026

Calendário ANBIMA. Sexta 09/10, sábado 10/10, domingo 11/10, segunda 12/10
(Nossa Senhora Aparecida, feriado), terça 13/10. Valores calculados com os
oráculos (NumPy e python-bizdays 1.0.19).

| `de` | `até` | `bizdays` | Dias contados | python-bizdays |
|---|---|---|---|---|
| 09/10 (sex) | 09/10 (sex) | 0 | — | 0 |
| 09/10 (sex) | 10/10 (sáb) | 1 | 09/10 | **0** |
| 09/10 (sex) | 12/10 (seg, feriado) | 1 | 09/10 | **0** |
| 09/10 (sex) | 13/10 (ter) | 1 | 09/10 | 1 |
| 10/10 (sáb) | 13/10 (ter) | 0 | — | 0 |
| 12/10 (feriado) | 13/10 (ter) | 0 | — | 0 |
| 09/10 (sex) | 16/10 (sex) | 4 | 09, 13, 14, 15/10 | 4 |
| 01/10 (qui) | 31/10 (sáb) | 21 | todos os DU de outubro | **20** |
| 13/10 (ter) | 09/10 (sex) | −1 | 13/10 | −1 |
| 12/10 (feriado) | 09/10 (sex) | 0 | — | 0 |

## Divergência em relação ao python-bizdays

O [python-bizdays](https://github.com/wilsonfreitas/python-bizdays) (fonte de
inspiração e dos dados) devolve **1 a menos** (em módulo) quando `até` não é
dia útil. Em uma amostra de 100 mil pares, isso ocorreu em ~31% deles; nas
fixtures deste projeto (20 mil pares por calendário) a proporção é a mesma, e
a divergência aparece **exatamente** nos pares em que `até` não é útil.

A divergência é **intencional**: seguimos BUS/252, NumPy e Polars. Os pares
divergentes ficam registrados em
`crates/bizdays/tests/fixtures/divergences_python_bizdays.csv`, com o resumo em
`manifest.json`.

## Ponto em aberto: pares invertidos

!!! question "A confirmar no ADR-0001"
    Para `de > até`, NumPy e Polars **não** são antissimétricos:
    `bizdays(12/10, 09/10) = 0`, mas `bizdays(09/10, 12/10) = 1`. Eles contam
    `(até, de]`, isto é, incluem a ponta de partida e excluem a de chegada no
    sentido do percurso.

    O `AGENTS.md` lista como invariantes a antissimetria
    (`bizdays(a,b) == -bizdays(b,a)`) e a aditividade para quaisquer `a, b, c`,
    que valem para a definição `cum[até] - cum[de]` (índice da
    [arquitetura](../desenvolvimento/arquitetura.md)), mas **não** para o
    NumPy quando as pontas diferem em ser ou não dia útil. As fixtures atuais
    seguem o NumPy. O mantenedor decide qual das duas vale antes da Fase 1.
