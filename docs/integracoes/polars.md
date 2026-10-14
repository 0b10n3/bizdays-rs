# Polars

!!! warning "Em construção — fase 4"
    Plugin nativo (pyo3-polars) operando direto sobre a coluna `Date`
    (`i32`, mesmo layout do núcleo).

*API prevista:*

=== "Python"

    ```python
    import polars as pl
    import bizdays_rs.polars as bz

    df.with_columns(du=bz.bizdays("liquidacao", "vencimento", calendar="ANBIMA"))
    ```

=== "Rust"

    ```rust
    // O plugin chama o kernel vetorizado do núcleo:
    bizdays::kernels::bizdays(&cal, from, to, &mut out)?;
    ```
