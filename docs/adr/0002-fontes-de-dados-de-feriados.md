# 0002 — Fontes de dados de feriados

- **Status:** Proposto
- **Data:** 2026-10-13

## Contexto

A lib embute calendários de feriados. Não há uma API oficial estável e
licenciada para todos eles; o python-bizdays mantém arquivos `.cal` para
ANBIMA e B3 sob licença MIT há mais de uma década.

## Decisão

1. **ANBIMA e B3:** importados sem alteração do python-bizdays 1.0.19
   (MIT, licença copiada em `data/LICENSE-python-bizdays.txt`). Hash, faixa e
   contagens em `crates/bizdays/data/README.md`.
2. **NY:** pendente. A fonte deve ser o calendário bancário dos EUA
   (Federal Reserve), usado na liquidação de FX T+2 — **não** o calendário da
   NYSE. Nenhum `NY.cal` entra sem fonte.
3. **Versão dos dados:** versionamento por data em `data/DATA_VERSION`
   (`AAAA.MM.N`, hoje `2026.10.0`), independente da versão da crate. Toda
   alteração cita fonte oficial e atualiza `DATA_VERSION`, o README dos dados,
   o `CHANGELOG.md` e as fixtures.

## Pendências

- Escolher a fonte do NY (Federal Reserve: *Holidays Observed by the Federal
  Reserve System*) e a regra de feriados no fim de semana.
- O B3 termina em 2026-12-31: definir fonte para estender (calendário oficial
  da B3).
- O `ANBIMA.cal` do upstream lista 2079-04-21 duas vezes (Tiradentes e
  Sexta-feira Santa); reportar ao python-bizdays.

## Consequências

- Proveniência auditável por hash; atualizações viram diffs revisáveis.
- Dependemos do ritmo de atualização do upstream ou de fontes oficiais.
