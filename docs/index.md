# bizdays

Dias úteis para aplicações financeiras, com foco no mercado brasileiro
(calendários ANBIMA e B3). Núcleo em Rust, pacote Python `bizdays-rs`, plugin
nativo para Polars e uso em pandas e PySpark/Databricks.

!!! warning "Em construção — fase 0"
    Só a infraestrutura existe. A API abaixo é **prevista**; ela chega na
    [Fase 1](desenvolvimento/roadmap.md).

*API prevista:*

=== "Rust"

    ```rust
    use bizdays::{Calendar, Date};

    let cal = Calendar::anbima();
    let n = cal.bizdays(Date::from_ymd(2026, 10, 9)?, Date::from_ymd(2026, 10, 13)?)?;
    assert_eq!(n, 1); // 12/10/2026 é feriado
    ```

=== "Python"

    ```python
    import datetime as dt
    from bizdays_rs import Calendar

    cal = Calendar.anbima()
    assert cal.bizdays(dt.date(2026, 10, 9), dt.date(2026, 10, 13)) == 1
    ```

## Por onde começar

- [Semântica de contagem](conceitos/semantica.md): o intervalo `[de, até)`.
- [Roadmap](desenvolvimento/roadmap.md): fases e marcos.
- [ADRs](adr/0001-semantica-de-contagem.md): decisões de arquitetura.
