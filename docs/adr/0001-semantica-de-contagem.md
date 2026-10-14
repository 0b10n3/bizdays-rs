# 0001 — Semântica de contagem

- **Status:** Aceito
- **Data:** 2026-10-13

## Contexto

Bibliotecas de dias úteis divergem sobre incluir as pontas. A B3 define o
BUS/252 com dias úteis entre a liquidação (inclusive) e o vencimento
(exclusive); NumPy `busday_count` e Polars `business_day_count` usam o mesmo
intervalo semiaberto. O python-bizdays, fonte de inspiração e dos dados, devolve
1 a menos quando `até` não é dia útil (~31% de 100 mil pares aleatórios).

## Decisão

`bizdays(de, até)` = número de dias úteis em `[de, até)`. Se `de > até`, o
resultado é negativo. Não há flags para mudar a semântica.

Oráculo de teste: NumPy `busday_count`. A divergência do python-bizdays é
intencional, documentada e **não** é imitada.

## Ponto a confirmar (encontrado na Fase 0)

Para `de > até`, NumPy e Polars contam `(até, de]` com sinal trocado, não
`[até, de)`. Exemplo (ANBIMA): `bizdays(2026-10-12, 2026-10-09) = 0`, mas
`bizdays(2026-10-09, 2026-10-12) = 1`. Assim:

- **(a) Seguir NumPy/Polars:** compatível com os oráculos e com o Polars; mas
  `bizdays(a,b) == -bizdays(b,a)` só vale quando as duas pontas são ambas úteis
  ou ambas não úteis, e a aditividade só vale para cadeias no mesmo sentido.
- **(b) `cum[até] - cum[de]`:** antissimétrico e aditivo para quaisquer datas,
  como exigem os invariantes do `AGENTS.md`; diverge do NumPy/Polars em pares
  invertidos com pontas de tipos diferentes. As fixtures de pares invertidos
  passariam a ser `-busday_count(até, de)`.

Para `de ≤ até` as duas opções coincidem. As fixtures atuais seguem (a). O
mantenedor escolhe antes da Fase 1 e atualiza este ADR, o `AGENTS.md` (se
preciso) e o gerador.

## Consequências

- Aditividade para `a ≤ b ≤ c`: `bizdays(a,b) + bizdays(b,c) == bizdays(a,c)`.
- A implementação é uma diferença no índice `cum`, O(1).
- Usuários vindos do python-bizdays verão resultados diferentes quando `até`
  não for útil; a página de semântica e o CSV de divergências explicam.
