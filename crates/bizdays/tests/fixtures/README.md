# Fixtures do oráculo

**Zona gerada.** Nada aqui é editado à mão: tudo sai de
`tools/oracle/generate_fixtures.py` (`just fixtures`). Os valores esperados
são **sempre** calculados pelos oráculos.

- Feriados: `crates/bizdays/data/{ANBIMA,B3}.cal`, os mesmos da lib, usados
  pelos dois oráculos. O gerador aborta se os calendários que vêm com o
  python-bizdays diferirem deles (ignorando duplicatas do upstream).
- Faixa: anos completos cobertos pelos dados (ANBIMA 2000–2099, B3 2000–2026).
  Os arquivos que usam o python-bizdays ficam dentro da faixa dele
  (do primeiro ao último feriado).
- Seed fixa `20261013`, linhas ordenadas, sem timestamps: rodar de novo não
  produz diff (`just fixtures-check`).
- Todos os CSVs têm cabeçalho, coluna `calendar` (`ANBIMA` ou `B3`), datas ISO
  e booleanos `true`/`false`.

| Arquivo | Colunas | Oráculo | Conteúdo |
|---|---|---|---|
| `bizdays.csv` | `calendar,from,to,expected` | NumPy `busday_count`; pares invertidos: `-busday_count(to, from)` (ADR-0001) | 5.000 pares aleatórios por calendário, 1.000 pares invertidos (valor negativo, antissimétrico), casos de borda (mesma data útil/não útil, sexta→sábado, sábado→domingo, sábado→segunda, feriado de 12/10/2026, Carnaval 2026, 20/11/2024, virada 2025→2026) e primeiro↔último dia útil da faixa. Semântica `[from, to)` |
| `isbizday.csv` | `calendar,date,expected` | NumPy `is_busday` | todos os dias de 2024-01-01 a 2026-12-31 |
| `roll.csv` | `calendar,date,convention,expected` | NumPy `busday_offset(d, 0, roll=…)` | mesmas datas do `isbizday.csv`; `convention` ∈ `following`, `preceding`, `modified_following`, `modified_preceding`. Linhas cujo resultado cairia fora da faixa são omitidas (ex.: B3 `following` de 2026-12-31) |
| `offset.csv` | `calendar,date,n,expected` | python-bizdays `cal.offset(d, n)` | 300 datas aleatórias por calendário (úteis ou não), `n` de −30 a 30. **Provisório:** a semântica de `offset` a partir de dia não útil depende do ADR-0005 |
| `getdate.csv` | `calendar,expr,year,month,expected` | python-bizdays `getdate` | 10 expressões × anos 2024–2027 × meses 1–12, mais a variante anual (`month` vazio) das quatro primeiras. Expressões que lançam erro (ex.: B3 em 2027, fora da faixa) são puladas e contadas no manifesto |
| `divergences_python_bizdays.csv` | `calendar,from,to,expected,python_bizdays,from_is_biz,to_is_biz` | `expected` (como em `bizdays.csv`) × python-bizdays | até 250 linhas por calendário em que os dois diferem. Documenta a **divergência intencional** (ADR-0001): o python-bizdays conta 1 a menos (em módulo) quando a data mais tarde do par não é dia útil (`to` em pares diretos, `from` em invertidos). **Não é valor esperado da lib** |
| `manifest.json` | — | — | seed, versão do gerador, versões dos oráculos, SHA-256 dos `.cal`, faixas, linhas por arquivo, linhas puladas e resumo das divergências por direção e tipo de ponta |
