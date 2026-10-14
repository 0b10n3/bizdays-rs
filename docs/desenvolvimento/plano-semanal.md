# bizdays — Plano semanal por épicos

*Versão 1 · 13/10/2026 · derivado de `estrategia.md`*

**Premissas:**
- 5 a 10 h por semana.
- Modo tutor: você escreve o código e os testes do domínio; a IA explica, revisa e cuida da infraestrutura.
- TDD sempre: teste vermelho → implementação mínima → refatoração.
- 28 semanas, de **19/10/2026** a **30/04/2027**, já contando as festas de fim de ano e o Carnaval como semanas leves.

---

## Visão geral

| Épico | Semanas | Período | Marco |
|---|---|---|---|
| **E0** Fundação | 1–2 | 19/10 – 01/11 | Repositório com CI verde e primeiro teste seu passando |
| **E1** O tipo `Date` | 3–4 | 02/11 – 15/11 | `Date` completo, com round-trip garantido por proptest |
| **E2** Calendário e contagem | 5–7 | 16/11 – 06/12 | `bizdays` e `isbizday` batendo com o NumPy em todas as fixtures |
| **E3** Ajustes e navegação | 8–9 | 07/12 – 20/12 | `following`, `modified_*`, `offset` e `seq` prontos (ADR-0005 decidido) |
| — Festas (folga) | 10–11 | 21/12 – 03/01 | Revisão, diário, primeira rodada de `cargo-mutants` |
| **E4** Calendários embutidos e compostos | 12–14 | 04/01 – 24/01 | `Calendar::load("ANBIMA")`, `union`, NY com fonte oficial; **`bizdays` 0.1.0-alpha.1** (semana 12) |
| **E5** Convenções e `getdate` | 15–16 | 25/01 – 07/02 | `DayCount` completo; `getdate` (ou adiado para a 0.2) |
| **E6** Release do crate | 17 | 08/02 – 14/02 (Carnaval) | **`bizdays` 0.1.0 no crates.io** |
| **E7** Kernels e benchmarks Rust | 18–20 | 15/02 – 07/03 | Kernels vetorizados; **`bizdays` 0.2.0** |
| **E8** Python e Polars | 21–25 | 08/03 – 11/04 | **`bizdays-rs` 0.1.0a1** (semana 21); **`bizdays-rs` 0.1.0 no PyPI**, com plugin Polars |
| **E9** Spark, docs e lançamento | 26–28 | 12/04 – 30/04 | Receita Databricks, site completo, **`bizdays-rs` 0.2.0** e anúncio |

O caminho crítico é E1 → E2 → E3 → E7 → E8. Quando o prazo apertar, o que pode ser adiado é `getdate` (E5), o experimento `u16` (E7) e o acessor pandas (E8). Testes nunca são adiados.

---

## Ritual de cada semana

| Quando | O quê | Tempo |
|---|---|---|
| **Início** | Ler o bloco da semana, `git switch develop && git pull`, abrir a branch da semana (`just branch feature e1-s03-…`, ver `fluxo-git.md`), escrever no diário o objetivo | 15 min |
| **Estudo** | Os capítulos indicados, antes de codar. Tente os exemplos do livro no Rust Playground | 1–3 h |
| **Ciclos TDD** | Um teste vermelho por vez. Travou por mais de 20 min? Peça à IA a **dica de nível 1** | 3–6 h |
| **Fim** | `just ci` verde → pedir revisão à IA (prompt abaixo) → corrigir os bloqueantes → PR para `develop` com squash merge → diário | 1 h |

**Prompt de revisão semanal** (cole no Claude Code ou no Gemini):

> Revise o diff desta branch contra `develop` seguindo o AGENTS.md, seção 2.2, item 4. Classifique os achados como bloqueante, importante ou sugestão, com `arquivo:linha`, o porquê e a referência. Depois me faça 3 perguntas para verificar se entendi os conceitos de Rust usados nesta semana. Não escreva código na zona do aprendiz.

**Regra de atraso:** se uma semana não fechar, ela continua na seguinte. A cada 2 semanas de atraso acumulado, corte um item da lista de adiáveis acima, em vez de pular testes.

---

## E0 — Fundação (semanas 1–2)

### Semana 1 · 19/10 – 25/10 · Repositório de pé

- **Estudo:** Rust Book, caps. 1–3 (instalação, Cargo, variáveis, tipos, funções, controle de fluxo).
- **Infra (IA):**
  - rodar o `prompt-setup-fase0.md` no Claude Code;
  - revisar o relatório e as pendências;
  - fazer o push e conferir o CI no GitHub.
- **Você:**
  - ler o `AGENTS.md`, o ADR-0001 e o README de fixtures;
  - rodar cada receita do `justfile`;
  - testar o hook: pedir ao Claude Code para editar `src/date.rs` e ver o bloqueio.
- **Pronto quando:** CI verde em `main` e `develop`, `develop` como branch padrão, rulesets do `fluxo-git.md` (seção 7) aplicados, `just ci` passando na sua máquina e no RustRover.

### Semana 2 · 26/10 – 01/11 · Ownership e o primeiro teste seu

- **Estudo:** caps. 4 (ownership, borrowing, slices) e 11 (testes). É o capítulo mais importante do livro: não pule.
- **Você:**
  - escrever, à mão, um teste de integração que lê `tests/fixtures/bizdays.csv` e só conta as linhas (sem `csv` crate ainda: `std::fs` + `lines()`);
  - adicionar a dependência `thiserror` (decisão sua, com a IA explicando o porquê);
  - decidir e registrar no diário: `Date` vai guardar `i32` puro e nunca exporá o inteiro publicamente?
- **Pronto quando:** você consegue explicar a diferença entre `&str` e `String` sem consultar nada, e o teste de contagem de linhas passa.

---

## E1 — O tipo `Date` (semanas 3–4)

### Semana 3 · 02/11 – 08/11 · Conversão civil

- **Estudo:** caps. 5 (structs), 6 (enums e `match`), 9 (erros e `Result`).
- **Você (TDD):**
  - `Date::from_ymd(y, m, d) -> Result<Date, Error>` e `Date::to_ymd()`, via algoritmo de Howard Hinnant (`days_from_civil` / `civil_from_days`);
  - testes vermelhos primeiro:
    - `1970-01-01` = 0;
    - `2000-02-29` válido e `2001-02-29` inválido;
    - `2100-02-28` → `2100-03-01`, porque 2100 não é bissexto.
  - `enum Error` com `InvalidDate`.
- **Pronto quando:** os testes de calendário gregoriano passam, e você implementou o algoritmo entendendo cada linha (explique no diário a "era" de 400 anos).

### Semana 4 · 09/11 – 15/11 · Ergonomia e propriedades

- **Estudo:** cap. 10.2 (traits) e a doc de `std::fmt::Display` e `std::str::FromStr`.
- **Você (TDD):**
  - `impl FromStr for Date` (ISO `YYYY-MM-DD`) e `impl Display`;
  - `weekday()`;
  - `derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)` e por que cada um;
  - adicionar `proptest` (dev) e a propriedade **round-trip**: `from_ymd(to_ymd(d)) == d` para qualquer `d` em 1900–2200;
  - propriedade: `weekday` avança 1 a cada dia.
- **Pronto quando:** o proptest roda 10.000 casos sem falha, e a cobertura (`just cov`) de `date.rs` está acima de 95%.

---

## E2 — Calendário e contagem (semanas 5–7)

### Semana 5 · 16/11 – 22/11 · `Weekmask` e o builder

- **Estudo:** cap. 8 (coleções: `Vec`, `HashSet`); padrão builder nas Rust API Guidelines (C-BUILDER).
- **Você (TDD):**
  - `Weekmask(u8)` com `SAT_SUN` e `contains(weekday)`;
  - `CalendarBuilder::new().weekmask(..).holidays(..).range(..).build() -> Result<Calendar, Error>`;
  - erros `InvalidRange` e `HolidayOutOfRange`.
- **Pronto quando:** o builder rejeita faixas invertidas e aceita feriados duplicados sem quebrar. Defina e teste o comportamento: deduplicar ou rejeitar?

### Semana 6 · 23/11 – 29/11 · O índice O(1)

- **Estudo:** cap. 10.1 (genéricos), cap. 13.2 (iteradores) e `Vec::with_capacity`.
- **Você (TDD):**
  - construção de `cum: Vec<u32>` e `bizlist: Vec<i32>` em O(n), numa única passada;
  - `is_bizday(d)` = `cum[i+1] - cum[i] == 1`;
  - `bizdays(a, b)` = `cum[b] - cum[a]`;
  - erro `OutOfRange` para datas fora da faixa.
- **Pronto quando:** os casos de borda escritos à mão passam: feriado de 12/10/2026, Carnaval e virada de ano.

### Semana 7 · 30/11 – 06/12 · Golden tests e invariantes

- **Estudo:** a doc do `proptest` (strategies, `prop_assume!`) e a doc do crate `csv`.
- **Você (TDD):**
  - adicionar `csv` (dev);
  - golden tests contra `bizdays.csv` e `isbizday.csv` (ANBIMA e B3);
  - propriedades **aditividade** e **antissimetria**;
  - um teste que documenta a divergência do python-bizdays (lê `divergences_python_bizdays.csv` e confirma que você bate com a coluna `expected`).
- **Pronto quando:** 100% das linhas das fixtures passam. **Primeira grande vitória: a contagem está correta.**

---

## E3 — Ajustes e navegação (semanas 8–9)

### Semana 8 · 07/12 – 13/12 · Ajustes de data

- **Estudo:** cap. 6 de novo (enums com `match` exaustivo), cap. 19 (padrões).
- **Você (TDD):**
  - `following`, `preceding` em O(1) via `cum` e `bizlist`;
  - `enum Adjustment { Unadjusted, Following, Preceding, ModifiedFollowing, ModifiedPreceding }` e `adjust(d, Adjustment)`;
  - golden contra `roll.csv`;
  - propriedades: `following(d) >= d` e é útil; `preceding(d) <= d` e é útil.
- **Pronto quando:** `roll.csv` 100%, incluindo modified following no fim de mês.

### Semana 9 · 14/12 – 20/12 · `offset`, `seq` e ADR-0005

- **Estudo:** cap. 13 (closures e iteradores), trait `Iterator` e `impl Iterator<Item = Date>`.
- **Você:**
  - **decidir o ADR-0005** (semântica de `offset` a partir de dia não útil) e mudar o status para Aceito;
  - TDD de `offset(d, n)`, golden contra `offset.csv` (ajuste as fixtures se escolher outra semântica: peça à IA para alterar o gerador);
  - `seq(a, b)` retornando um iterador, sem alocar `Vec`;
  - propriedade: `bizdays(d, offset(d, n)) == n` para `d` útil.
- **Pronto quando:** o núcleo escalar está completo. Atualize `docs/conceitos/semantica.md` com `offset`.

---

## Folga de festas (semanas 10–11)

### Semana 10 · 21/12 – 27/12 · Leve

- Reler o diário e consolidar dúvidas.
- Rodar `cargo-mutants` no núcleo (a IA instala e explica): cada mutante sobrevivente é um teste que falta.

### Semana 11 · 28/12 – 03/01 · Leve

- Escrever os testes que matam os mutantes sobreviventes.
- **Estudo** opcional: cap. 7 (módulos) e cap. 14 (Cargo e crates.io), em preparação para E4 e E6.

---

## E4 — Calendários embutidos e compostos (semanas 12–14)

### Semana 12 · 04/01 – 10/01 · Parser de `.cal` e registro

- **Estudo:** cap. 7 (módulos e visibilidade), `include_str!`, `std::sync::OnceLock`.
- **Você (TDD):**
  - `Calendar::from_cal_str(&str)`, que lê o formato `.cal`;
  - erros com número de linha;
  - `Calendar::load("ANBIMA")` e `Calendar::load("B3")` com cache via `OnceLock`;
  - a função `available()` lista os nomes.
- **Fim da semana — pré-release `bizdays` 0.1.0-alpha.1:** o núcleo escalar (E1–E3) com ANBIMA e B3 embutidos.
  - `release/bizdays-0.1.0-alpha.1` → PR para `main` (merge commit);
  - na `main`, **primeira publicação manual** (`cargo publish`, token `publish-new` de 1 dia), que cria a crate e garante o nome;
  - **Infra (IA):** configurar o trusted publishing no crates.io; depois `just release-finish bizdays 0.1.0-alpha.1` (o workflow pula a versão já publicada e cria o GitHub Release) e back-merge em `develop`.
- **Pronto quando:** os golden tests passam com calendários carregados do registro, não mais construídos à mão, e `cargo add bizdays@0.1.0-alpha.1` funciona num projeto novo.

### Semana 13 · 11/01 – 17/01 · `Arc`, `Send + Sync` e composição

- **Estudo:** cap. 15 (smart pointers: `Box`, `Rc`, `Arc`) e cap. 16 (concorrência, `Send`/`Sync`).
- **Você (TDD):**
  - `Calendar` com `Arc` interno (clone barato);
  - teste que compila só se `Calendar: Send + Sync`;
  - `union(&a, &b)` e `intersection(&a, &b)` materializados;
  - propriedade: útil na união ⇔ útil em ambos.
- **Pronto quando:** `ANBIMA ∪ B3` passa nas propriedades e você consegue explicar por que `Rc` não serviria.

### Semana 14 · 18/01 – 24/01 · Calendário NY (ADR-0002)

- **Infra (IA):** pesquisar a fonte oficial dos feriados bancários dos EUA (Federal Reserve), montar `NY.cal` com fonte citada, atualizar `DATA_VERSION`, gerador e fixtures.
- **Você:**
  - revisar os dados e aceitar o ADR-0002;
  - TDD de um caso de FX T+2 no calendário `ANBIMA ∪ NY`: `offset(d, 2)` cruzando o feriado de Thanksgiving.
- **Pronto quando:** três calendários embutidos, todos com fonte, hash e fixtures.

---

## E5 — Convenções e `getdate` (semanas 15–16)

### Semana 15 · 25/01 – 31/01 · `DayCount`

- **Estudo:** os tipos `f64` e as armadilhas de ponto flutuante; a doc de `approx` (ou faça comparações com tolerância à mão).
- **Você (TDD):**
  - `enum DayCount { Bus252(Calendar), Act360, Act365F, Thirty360(Thirty360Variant) }`;
  - `year_fraction(from, to) -> Result<f64, Error>`;
  - testes com exemplos do manual da CALC (BUS/252) e casos conhecidos de 30/360 (dia 31, fevereiro).
- **Pronto quando:** as quatro convenções têm testes de exemplo e uma propriedade de aditividade (onde ela vale).

### Semana 16 · 01/02 – 07/02 · `getdate` (adiável)

- **Estudo:** cap. 6 de novo e parsing manual com `split_whitespace`; opcional, o crate `winnow`.
- **Você (TDD):**
  - AST como `enum`, parser `&str -> Result<Expr, Error>` e avaliador;
  - golden contra `getdate.csv`.
- **Se a semana apertar:** mova `getdate` para a 0.2 e use a semana para polir a documentação do rustdoc.
- **Pronto quando:** `getdate.csv` 100%, ou a decisão de adiar registrada no CHANGELOG.

---

## E6 — Release do crate (semana 17)

### Semana 17 · 08/02 – 14/02 · `bizdays` 0.1.0 (semana do Carnaval, leve)

- **Estudo:** cap. 14 (publicar no crates.io) e a Rust API Guidelines checklist.
- **Você:**
  - revisar a API pública inteira contra a checklist (nomes, `#[must_use]`, `Debug` em tudo);
  - exemplos de rustdoc em cada item público;
  - `CHANGELOG` 0.1.0.
- **Fluxo (Git Flow):** `just release-start bizdays 0.1.0` no início da semana; o que acima for ajuste entra via `bugfix/*` → `release/bizdays-0.1.0`; tag `bizdays-v0.1.0-rc.1` e teste; PR para `main` (merge commit); `just release-finish`; back-merge em `develop`.
- **Infra (IA):** conferir o dry-run do RC (o trusted publishing já foi configurado na alpha, semana 12) e, depois da sua aprovação no environment `release`, a página no docs.rs.
- **Pronto quando:** `cargo add bizdays` funciona num projeto novo. **Marco: primeira publicação.**

---

## E7 — Kernels e benchmarks Rust (semanas 18–20)

### Semana 18 · 15/02 – 21/02 · Kernels vetorizados

- **Estudo:** slices (`&[T]`, `&mut [T]`), `zip`, `chunks`, e por que evitar alocação em laço quente.
- **Você (TDD):**
  - `kernels::bizdays(from: &[i32], to: &[i32], out: &mut [i32])` e equivalentes para `is_bizday` e `offset`;
  - nulos via `Option<&[bool]>` de validade (ou bitmap);
  - propriedade-chave: **kernel == `map` do escalar**, para vetores aleatórios com nulos.
- **Pronto quando:** a propriedade passa com 10.000 casos e vetores de até 10⁴ elementos.

### Semana 19 · 22/02 – 28/02 · Benchmarks

- **Estudo:** a doc do `divan` e noções de medição (warm-up, variância, `black_box`).
- **Você:** benchmarks de construção do calendário, de consultas escalares e dos kernels em 10³, 10⁵ e 10⁷.
- **Infra (IA):** integrar o CodSpeed no CI para detectar regressão.
- **Pronto quando:** você tem uma tabela de ns por par e comparou com a linha de base (Polars ~50 ns, NumPy ~113 ns).

### Semana 20 · 01/03 – 07/03 · Otimização guiada por medida (parcialmente adiável)

- **Estudo:** cap. 10 (genéricos) aplicado: o experimento `cum: Vec<u16>` vs `Vec<u32>`.
- **Você:** rodar o experimento, medir e decidir com dados (ADR curto). Se não houver ganho, registre e mantenha `u32`.
- **Fim da semana — release:** `release/bizdays-0.2.0` com os kernels (o experimento só entra se virou `feature/*`), RC, PR para `main`, tag e back-merge.
- **Pronto quando:** existe um ADR com os números (meta: < 10 ns por par no kernel) e **`bizdays` 0.2.0** está no crates.io.

---

## E8 — Python e Polars (semanas 21–25)

### Semana 21 · 08/03 – 14/03 · Fundamentos do PyO3

- **Estudo:** guia do PyO3 (módulos, `#[pyclass]`, `#[pymethods]`, conversão de erros, GIL).
- **Você (TDD em Python com `pytest`):**
  - classe `Calendar` exposta (`load`, `is_bizday`, `bizdays`, `following`, `offset`);
  - `datetime.date` ↔ `Date`;
  - erros Rust viram exceções Python (`ValueError`, `bizdays_rs.OutOfRangeError`);
  - stubs `.pyi`.
- **Fim da semana — pré-release `bizdays-rs` 0.1.0a1:** só a API escalar, marcada como alpha.
  - ensaio no TestPyPI e teste num venv limpo;
  - `release/bizdays-rs-0.1.0-alpha.1` → PR para `main`, `just release-finish bizdays-rs 0.1.0-alpha.1`, aprovação no environment `release` e back-merge;
  - o pending publisher do PyPI cria o projeto `bizdays-rs` nessa publicação.
- **Pronto quando:** `pytest` reproduz em Python os golden tests escalares (lendo as mesmas fixtures) e `pip install --pre bizdays-rs` funciona num venv limpo.

### Semana 22 · 15/03 – 21/03 · Plugin Polars (1/2)

- **Estudo:** o tutorial de plugins de expressão do Polars e a doc do `pyo3-polars` (`#[polars_expr]`).
- **Você:**
  - expressão `bz.bizdays(from, to, cal=...)` chamando o kernel;
  - colunas `Date` lidas sem cópia (`i32`);
  - nulos propagando.
- **Pronto quando:** `df.select(bz.bizdays("a", "b", cal=anbima))` bate com `pl.business_day_count` em 10⁵ linhas.

### Semana 23 · 22/03 – 28/03 · Plugin Polars (2/2)

- **Você:**
  - `offset`, `adjust` e `is_bizday` como expressões;
  - namespace `pl.col("d").bz`;
  - calendário serializado nos kwargs, com cache por hash no Rust;
  - testes com `LazyFrame` e modo streaming.
- **Pronto quando:** as expressões funcionam em lazy e streaming, com teste de propriedade via `hypothesis`.

### Semana 24 · 29/03 – 04/04 · NumPy e pandas

- **Estudo:** a doc do crate `numpy` (rust-numpy) e os dtypes `datetime64` e `date32[pyarrow]`.
- **Você:**
  - funções que aceitam `ndarray` e `Series` e devolvem o mesmo tipo de contêiner, preservando o índice;
  - broadcasting estilo NumPy;
  - liberar o GIL em lotes grandes.
- **Adiável:** o acessor `.bz` do pandas.
- **Pronto quando:** `datetime64[ns]`, `datetime64[D]` e `date32[pyarrow]` funcionam, e `NaT` vira nulo.

### Semana 25 · 05/04 – 11/04 · Benchmarks comparativos e PyPI

- **Você:** benchmarks com `pytest-benchmark`: python-bizdays, NumPy, Polars nativo, `bizdays-rs` NumPy e `bizdays-rs` plugin, sempre conferindo o resultado antes de medir.
- **Fluxo (Git Flow):** `release/bizdays-rs-0.1.0`; tag `bizdays-rs-v0.1.0-rc.1` publica `0.1.0rc1` no TestPyPI; teste num venv limpo; PR para `main`, tag final, back-merge.
- **Infra (IA):** conferir o RC no TestPyPI (o trusted publishing já foi usado na alpha, semana 21).
- **Pronto quando:** `pip install bizdays-rs` funciona. **Marco: segunda publicação.**

---

## E9 — Spark, documentação e lançamento (semanas 26–28)

### Semana 26 · 12/04 – 18/04 · Databricks

- **Estudo:** `mapInArrow` e `pandas_udf` na documentação do PySpark; instalação de wheels no Databricks.
- **Você:**
  - função `bz.arrow.bizdays(...)` sobre arrays `pyarrow` (`date32`, sem cópia);
  - receita testada num cluster Databricks real e em Spark local, no CI;
  - calendário cacheado por worker.
- **Pronto quando:** um notebook de exemplo roda no Databricks com 10⁷ linhas e o tempo está documentado.

### Semana 27 · 19/04 – 25/04 · Documentação completa

- **Você:**
  - guia rápido;
  - páginas de calendários, convenções e integrações com exemplos reais em abas Rust | Python;
  - página de benchmarks com seus números.
- **Infra (IA):** tema Syntaxis (`just brand` com o `tokens.json`), revisão de links e build `--strict`.
- **Pronto quando:** alguém que nunca viu o projeto consegue, só com o site, calcular DU entre duas datas em Rust, Polars e pandas.

### Semana 28 · 26/04 – 30/04 · Lançamento

- **Você:** retrospectiva no diário (o que aprendeu de Rust, o que faria diferente) e a lista da próxima versão do crate (regras de datas da B3, `getdate` se adiado, acessor pandas).
- **Fluxo (Git Flow):** `release/bizdays-rs-0.2.0` com `bz.arrow` e a receita Spark; RC no TestPyPI, PR para `main`, tag, back-merge.
- **Infra (IA):** revisão final de README, CHANGELOG, badges e issues abertas para a próxima versão.
- **Pronto quando:** anúncio publicado. Material natural para um post e para uma aula da Syntaxis.

---

## Checklist de conceitos de Rust por épico

| Épico | Conceitos que você vai dominar |
|---|---|
| E0–E1 | ownership, borrowing, structs, enums, `match`, `Result`, `?`, traits `Display`/`FromStr`, derives, testes |
| E2–E3 | `Vec`, iteradores, closures, genéricos, `impl Iterator`, builder, erros com `thiserror` |
| E4 | módulos, visibilidade, `OnceLock`, `include_str!`, `Arc`, `Send`/`Sync` |
| E5 | `f64` e precisão, parsing, AST com enums |
| E6 | publicação, SemVer, API Guidelines |
| E7 | slices mutáveis, desempenho, benchmarks, genéricos sobre tipos inteiros |
| E8–E9 | FFI com PyO3, GIL, zero-cópia com Arrow, plugins Polars |
