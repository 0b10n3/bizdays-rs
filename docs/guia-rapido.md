# Guia rápido

!!! warning "Em construção — fase 1"
    Instalação e primeiros passos entram quando a API escalar existir.

*API prevista:*

=== "Rust"

    ```toml
    [dependencies]
    bizdays = "0.1"
    ```

    ```rust
    use bizdays::{Adjustment, Calendar, Date};

    let cal = Calendar::anbima();
    let d = Date::from_ymd(2026, 10, 12)?;
    assert!(!cal.is_bizday(d)?);
    assert_eq!(cal.adjust(d, Adjustment::Following)?, Date::from_ymd(2026, 10, 13)?);
    ```

=== "Python"

    ```bash
    pip install bizdays-rs
    ```

    ```python
    import datetime as dt
    from bizdays_rs import Calendar

    cal = Calendar.anbima()
    assert not cal.is_bizday(dt.date(2026, 10, 12))
    assert cal.adjust(dt.date(2026, 10, 12), "following") == dt.date(2026, 10, 13)
    ```
