# Benchmarks

!!! warning "Em construção — fase 3"
    Benchmarks reproduzíveis com `divan` (Rust) e `pytest-benchmark` (Python).

## Linha de base

Medida antes do projeto, para dar a ordem de grandeza a superar.

| Implementação (100 mil pares, ANBIMA) | Por par |
|---|---|
| python-bizdays | ~6.800 ns |
| NumPy | ~113 ns |
| Polars nativo | ~50 ns |

Meta da Fase 3: o kernel do núcleo no mesmo patamar do Polars nativo, com
consultas O(1) pelo índice `cum`.
