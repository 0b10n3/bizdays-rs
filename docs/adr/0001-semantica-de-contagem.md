# 0001 — Semântica de contagem

- **Status:** Aceito
- **Data:** 2026-10-13

## Contexto

Bibliotecas de dias úteis divergem sobre incluir as pontas. A B3 define o
BUS/252 com dias úteis entre a liquidação (inclusive) e o vencimento
(exclusive); NumPy `busday_count` e Polars `business_day_count` usam o mesmo
intervalo semiaberto. O python-bizdays, fonte de inspiração e dos dados, devolve
1 a menos quando `até` não é dia útil (~31% de 100 mil pares aleatórios).

Para `de > até`, NumPy e Polars contam `(até, de]` com sinal trocado, não
`[até, de)`: `bizdays(2026-10-12, 2026-10-09) = 0` (ANBIMA), mas
`bizdays(2026-10-09, 2026-10-12) = 1`. Assim, eles não são antissimétricos
quando uma ponta é dia útil e a outra não.

## Decisão

`bizdays(de, até)` = número de dias úteis em `[de, até)`. Se `de > até`, o
resultado é `-bizdays(até, de)`: os dias úteis em `[até, de)` com sinal
trocado. Em termos do índice, `bizdays(de, até) = cum[até] - cum[de]` para
quaisquer datas. Não há flags para mudar a semântica.

Oráculo de teste: NumPy `busday_count` para `de ≤ até` e
`-busday_count(até, de)` para `de > até`. A divergência do python-bizdays é
intencional, documentada e **não** é imitada.

Alternativa descartada (decisão do mantenedor em 2026-10-14): seguir o
NumPy/Polars também nos pares invertidos. Compatível com os dois, mas quebra a
antissimetria e a aditividade para cadeias em sentidos mistos.

## Consequências

- Antissimetria para quaisquer datas: `bizdays(a,b) == -bizdays(b,a)`.
- Aditividade para quaisquer `a, b, c`:
  `bizdays(a,b) + bizdays(b,c) == bizdays(a,c)`.
- A implementação é uma diferença no índice `cum`, O(1), sem ramo para o sinal.
- Para `de > até`, diverge do NumPy `busday_count` e do Polars
  `business_day_count` quando exatamente uma das pontas é dia útil. O
  adaptador do Polars **não** pode delegar ao `business_day_count`.
- Usuários vindos do python-bizdays verão resultados diferentes quando a data
  mais tarde do par não for útil; a página de semântica e o CSV de divergências
  explicam.
