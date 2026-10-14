# Estratégia

!!! note "Documento a importar"
    O plano completo (`estrategia.md`) não estava no repositório durante a
    Fase 0. Substitua esta página pelo documento original quando possível.
    Até lá, ficam aqui as decisões já tomadas.

| Tema | Decisão |
|---|---|
| Semântica de contagem | `bizdays(de, até)` = dias úteis em `[de, até)`; negativo se `de > até`; sem flags (ADR-0001) |
| Divergência conhecida | python-bizdays devolve 1 a menos quando `até` não é útil (~31% dos pares); intencional, documentada |
| Oráculos de teste | NumPy para contagem e ajustes; python-bizdays para `offset` e `getdate` |
| Tipo de data interno | `Date(i32)`, dias desde 1970-01-01 (Arrow `date32`, Polars `Date`, Spark `DateType`) |
| Índice | `cum: Vec<u32>` e `bizlist: Vec<i32>`, consultas O(1) |
| Escopo v1 | núcleo, calendários embutidos (ANBIMA, B3, NY), compostos, convenções BUS/252, ACT/360, ACT/365F, 30/360; regras de datas da B3 na v0.2 |
| Integrações | Polars nativo, depois NumPy/pandas, depois PySpark via Arrow |
| Documentação | Material for MkDocs, paleta Syntaxis, abas Rust \| Python |
| Fluxo | TDD; IA como tutora e revisora; 5 a 10 h por semana |
