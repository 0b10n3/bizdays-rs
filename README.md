# bizdays

Business-day calendars for financial applications, focused on the Brazilian market (ANBIMA and B3 holidays).
A Rust core (`bizdays` on crates.io) with a Python package (`bizdays-rs`), a native Polars plugin and pandas/PySpark support.
**Status: pre-alpha, phase 0** — infrastructure only, the API is not implemented yet. Documentation below is in Portuguese.

---

## O que é e por quê

`bizdays` calcula dias úteis para renda fixa e derivativos brasileiros:
contagem BUS/252, ajustes (following, preceding, modified), deslocamentos
(T+n, D-1) e convenções de contagem, com os calendários ANBIMA e B3.

- **Rápido:** índice pré-computado e consultas O(1); kernels vetorizados.
- **Onde os dados estão:** Polars, NumPy/pandas e Spark (via Arrow) sem
  conversões, porque o tipo de data interno é o mesmo `date32`.
- **Correto por construção:** testes contra oráculos (NumPy e python-bizdays)
  e testes de propriedade.

É também o projeto de aprendizado de Rust do mantenedor, desenvolvido com IA
em [modo tutor](docs/adr/0004-modo-tutor.md).

## Status

**Fase 0 concluída** — workspace, dados, oráculo de testes, CI, documentação e
configuração de agentes. Próxima: Fase 1, o núcleo escalar
([roadmap](docs/desenvolvimento/roadmap.md)).

## Semântica: `[de, até)`

`bizdays(de, até)` conta os dias úteis de `de` (inclusive) até `até`
(exclusive), como o BUS/252 da B3, NumPy e Polars. Com o feriado de
12/10/2026 (segunda):

```text
bizdays(2026-10-09, 2026-10-13) = 1   # só a sexta, 09/10
bizdays(2026-10-09, 2026-10-12) = 1   # python-bizdays devolve 0
```

Se `de > até`, o resultado é `-bizdays(até, de)`. O python-bizdays devolve 1 a
menos quando `até` não é dia útil; a divergência é intencional ([ADR-0001](docs/adr/0001-semantica-de-contagem.md)).

## Integrações previstas

- **Rust:** crate `bizdays`.
- **Python:** `pip install bizdays-rs` (wheels `abi3`, Python ≥ 3.10).
- **Polars:** plugin nativo.
- **NumPy / pandas:** entrada e saída do mesmo tipo.
- **PySpark / Databricks:** via Arrow (`mapInArrow`).

## Desenvolvimento local

Requer `rustup`, [`uv`](https://docs.astral.sh/uv/) e
[`just`](https://just.systems/).

```bash
just setup   # ambiente Python (uv) e toolchain Rust fixada
just ci      # tudo o que o CI roda
just --list  # demais receitas
```

Veja o [`CONTRIBUTING.md`](CONTRIBUTING.md) e o [`AGENTS.md`](AGENTS.md).

## Links

- Site: <https://0b10n3.github.io/bizdays-rs/>
- ADRs: [`docs/adr/`](docs/adr/)

## Licença

Licenciado sob a licença MIT ([`LICENSE-MIT`](LICENSE-MIT)).

## Agradecimentos

- [python-bizdays](https://github.com/wilsonfreitas/python-bizdays), de
  Wilson Freitas: inspiração e dados de feriados, sob licença MIT.
- Referências: Carreira, M. C. & Brostowicz, R. J. (2016), *Brazilian
  Derivatives and Securities*; Manual da Calculadora de Renda Fixa (CALC) da B3.
