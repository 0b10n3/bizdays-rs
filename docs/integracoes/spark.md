# PySpark / Databricks

!!! warning "Em construção — fase 5"
    Via Arrow com `mapInArrow`: o `DateType` do Spark já é `date32`.

*API prevista:*

=== "Python"

    ```python
    from bizdays_rs.spark import with_bizdays

    df = with_bizdays(df, "liquidacao", "vencimento", out="du", calendar="ANBIMA")
    ```

=== "Rust"

    ```rust
    // Sem código específico: o lado Python entrega batches Arrow ao kernel.
    ```
