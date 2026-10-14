# Roadmap

| Fase | Tema | Marcos | Dependências previstas |
|---|---|---|---|
| **0** | Infraestrutura | workspace, dados ANBIMA/B3, oráculo e fixtures, CI, site, ADRs, modo tutor | — (núcleo sem dependências); PyO3 no binding |
| **1** | Núcleo escalar | `Date`, `Weekmask`, `CalendarBuilder` + índice, `bizdays`, `is_bizday`, `Adjustment`, `offset` (após ADR-0005), `Error`; golden + proptest | `thiserror`; dev: `proptest`, `csv` |
| **2** | Calendários e convenções | `registry` (ANBIMA, B3, NY), `union`/`intersection`, `DayCount`, `getdate`; ADR-0002 fechado | — |
| **3** | Vetorização e desempenho | `kernels` sobre `&[i32]` com nulos; benchmarks | dev: `divan` |
| **4** | Python | API `bizdays-rs` completa, NumPy/pandas, plugin Polars; primeira publicação | `pyo3-polars`, `numpy` (crate) |
| **5** | Spark / Databricks | `mapInArrow`, guia de uso, regras de datas da B3 (v0.2) | `arrow` (se necessário) |

Fase atual: **Fase 0 concluída — próxima: Fase 1 (núcleo escalar)**.

O cronograma por semana, com os épicos E0–E9, está no
[plano semanal](plano-semanal.md).

Primeiro exercício da Fase 1: teste vermelho de `Date::from_ymd` /
`Date::to_ymd` (Rust Book, cap. 5 e 11).
