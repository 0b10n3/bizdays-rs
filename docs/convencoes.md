# Convenções de contagem

!!! warning "Em construção — fase 2"
    `enum DayCount` com as convenções abaixo.

Notação: \(d_1\) é a data inicial e \(d_2\) a final.

**BUS/252** — dias úteis do calendário, semântica `[d₁, d₂)`:

$$
\tau = \frac{\mathrm{DU}(d_1, d_2)}{252}
$$

**ACT/360** — dias corridos:

$$
\tau = \frac{d_2 - d_1}{360}
$$

**ACT/365F** (*fixed*):

$$
\tau = \frac{d_2 - d_1}{365}
$$

**30/360** — com \(D_1, D_2\) ajustados pela variante escolhida
(a definir na Fase 2, por exemplo 30/360 ISDA ou 30E/360):

$$
\tau = \frac{360\,(Y_2 - Y_1) + 30\,(M_2 - M_1) + (D_2 - D_1)}{360}
$$

*API prevista:*

=== "Rust"

    ```rust
    use bizdays::{Calendar, DayCount};

    let tau = DayCount::Bus252.year_fraction(d1, d2, Calendar::anbima())?;
    ```

=== "Python"

    ```python
    from bizdays_rs import Calendar, DayCount

    tau = DayCount.BUS252.year_fraction(d1, d2, Calendar.anbima())
    ```
