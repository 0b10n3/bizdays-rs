# Calendários

!!! warning "Em construção — fase 2"
    Calendários embutidos, compostos e personalizados.

| Calendário | Fonte | Faixa | Status |
|---|---|---|---|
| ANBIMA | python-bizdays 1.0.19 | 2000–2099 | dados importados |
| B3 | python-bizdays 1.0.19 | 2000–2026 | dados importados |
| NY | a definir (ADR-0002) | — | pendente |

Detalhes de origem, hashes e política de atualização em
`crates/bizdays/data/README.md`.

*API prevista:*

=== "Rust"

    ```rust
    use bizdays::Calendar;

    let fx = Calendar::anbima().union(Calendar::ny())?; // feriado em qualquer um
    ```

=== "Python"

    ```python
    from bizdays_rs import Calendar

    fx = Calendar.anbima() | Calendar.ny()
    ```
