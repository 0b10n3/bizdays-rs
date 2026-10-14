# 0005 — Semântica de `offset`

- **Status:** Proposto
- **Data:** 2026-10-13

## Contexto

`offset(d, n)` desloca `d` por `n` dias úteis. Quando `d` é dia útil não há
dúvida: `bizlist[cum[i] + n]`. Quando `d` **não** é útil, há escolhas. As
fixtures de `offset.csv` usam o python-bizdays e são **provisórias** até esta
decisão.

## Opções

**(a) Semântica do python-bizdays.** Para `n > 0`, conta a partir do dia útil
anterior a `d`; para `n < 0`, a partir do seguinte; `n = 0` devolve `d`
inalterado.

- Prós: compatível com o oráculo e com usuários do python-bizdays.
- Contras: implícita; `offset(d, 0)` pode devolver dia não útil.

**(b) Erro se `d` não for útil.**

- Prós: explícita, sem surpresa; força o usuário a decidir.
- Contras: menos ergonômica em lote (um dia não útil derruba a série; exige
  ajuste prévio).

**(c) Ajuste explícito via `Adjustment` antes do deslocamento**
(`offset(d, n, adj)`).

- Prós: explícita e ergonômica; casa com convenções de mercado
  (ex.: `following` antes de somar D+n).
- Contras: assinatura maior; precisa de um padrão ou de parâmetro obrigatório.

## Decisão

Pendente. O mantenedor decide na Fase 1. Se a escolha não for (a), o gerador
de `offset.csv` passa a usar NumPy `busday_offset` com o `roll` equivalente.

## Consequências

A definir com a decisão.
