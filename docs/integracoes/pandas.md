# pandas e NumPy

!!! warning "Em construção — fase 4"
    Funções que aceitam `ndarray` e `Series` e devolvem o mesmo tipo de entrada.

*API prevista:*

=== "Python"

    ```python
    import pandas as pd
    from bizdays_rs import Calendar

    cal = Calendar.anbima()
    df["du"] = cal.bizdays(df["liquidacao"], df["vencimento"])  # Series -> Series
    ```

=== "Rust"

    ```rust
    // Mesmo kernel sobre fatias &[i32] (datetime64[D] convertido para date32).
    bizdays::kernels::bizdays(&cal, from, to, &mut out)?;
    ```
