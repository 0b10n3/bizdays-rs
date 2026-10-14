# Arquitetura

## Layout

```
crates/bizdays/        núcleo Rust puro (crates.io)
  src/                 date, weekmask, calendar, adjust, error, compose,
                       daycount, registry, getdate, kernels
  data/                ANBIMA.cal, B3.cal, DATA_VERSION, README.md
  tests/               integração, proptest, golden (fixtures/ é gerada)
py-bizdays/            pacote bizdays-rs (PyO3 + maturin; abi3)
  src/lib.rs           módulo nativo bizdays_rs._bizdays_rs
  python/bizdays_rs/   código Python, stubs .pyi, py.typed
tools/                 oracle/, data/, brand/, agents/, tests/
docs/                  site MkDocs, adr/, desenvolvimento/
```

O workspace Cargo tem `default-members = ["crates/bizdays"]`: `cargo build` e
`cargo test` na raiz não compilam o binding. O binding entra em
`cargo clippy --workspace` e é construído pelo maturin (`just wheel`).

## Padrões

- **Núcleo funcional, casca fina:** o núcleo opera sobre fatias `&[i32]`;
  NumPy, Polars, Arrow e Spark são adaptadores finos.
- **Newtypes:** `Date(i32)` (dias desde 1970-01-01, layout de Arrow `date32`,
  Polars `Date` e Spark `DateType`) e `Weekmask(u8)`.
- **Calendário imutável** com índice pré-computado, `Arc` interno,
  `Send + Sync`; construção por builder com validação.
- **Enums como estratégia:** `Adjustment`, `DayCount`.
- **Composição materializada:** `union`/`intersection` geram índice novo.
- **Calendários embutidos:** `include_str!` + `OnceLock`.

## O índice `cum` / `bizlist`

Seja \(s\) a primeira data da faixa e \(i = d - s\) a posição da data \(d\).
Defina \(b(d) = 1\) se \(d\) é dia útil e \(0\) caso contrário.

- `cum: Vec<u32>`, com tamanho (nº de dias da faixa + 1):

    $$
    \mathrm{cum}[i] = \sum_{k=0}^{i-1} b(s + k)
    $$

    isto é, quantos dias úteis existem em \([s, s+i)\).

- `bizlist: Vec<i32>`: os dias úteis em ordem, `bizlist[j]` = o \(j\)-ésimo
  dia útil (base 0).

Consultas, todas O(1):

| Operação | Fórmula |
|---|---|
| `is_bizday(d)` | \(\mathrm{cum}[i+1] - \mathrm{cum}[i] = 1\) |
| `bizdays(a, b)` | \(\mathrm{cum}[i_b] - \mathrm{cum}[i_a]\) — dias úteis em \([a, b)\); negativo se \(a > b\) |
| `following(d)` | \(\mathrm{bizlist}[\mathrm{cum}[i]]\) |
| `preceding(d)` | \(\mathrm{bizlist}[\mathrm{cum}[i+1] - 1]\) |
| `offset(d, n)`, \(d\) útil | \(\mathrm{bizlist}[\mathrm{cum}[i] + n]\) |

A mesma fórmula vale para \(a > b\) e é antissimétrica (ADR-0001). O NumPy
daria \(-(\mathrm{cum}[i_a+1] - \mathrm{cum}[i_b+1])\); veja
[pares invertidos](../conceitos/semantica.md#pares-invertidos).

Índices fora de `0..len` viram `Error`, nunca `panic`. Memória: ~4 bytes por
dia da faixa + 4 por dia útil; 100 anos ≈ 240 KB.
