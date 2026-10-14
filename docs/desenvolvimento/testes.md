# Testes

## Camadas

| Camada | Onde | Ferramenta |
|---|---|---|
| Unitários | `#[cfg(test)]` em cada módulo | `cargo test` |
| Integração | `crates/bizdays/tests/` | `cargo test` |
| Propriedades | `crates/bizdays/tests/` | `proptest` (Fase 1) |
| Golden | `crates/bizdays/tests/fixtures/*.csv` | `csv` (Fase 1) |
| Python | `py-bizdays/tests/` | `pytest` + `hypothesis` |
| Ferramentas | `tools/tests/` | `pytest` |

Invariantes para testes de propriedade: `AGENTS.md`, seção 3.

## Oráculos

- **NumPy** (`busday_count`, `is_busday`, `busday_offset`): contagem, dia útil
  e ajustes (rolls).
- **python-bizdays**: `offset` e `getdate`, com as divergências documentadas.

O gerador (`tools/oracle/generate_fixtures.py`) lê os feriados de
`crates/bizdays/data/` e aborta se o python-bizdays carregar algo diferente.
Os valores esperados são sempre calculados pelos oráculos.

## Regenerar fixtures

```bash
just fixtures        # regenera crates/bizdays/tests/fixtures/
just fixtures-check  # regenera e falha se algum CSV mudou (o CI roda este)
```

O gerador é determinístico (seed `20261013`, saída ordenada, sem timestamps);
`tools/tests/test_oracle.py` garante isso. Esquema de cada CSV:
`crates/bizdays/tests/fixtures/README.md`.

Fixtures nunca são editadas à mão, nem para fazer teste passar.
