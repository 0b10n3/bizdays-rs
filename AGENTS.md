# AGENTS.md — bizdays

Instruções para agentes de IA (Claude Code, Gemini e outros) que trabalham neste repositório. Leia o arquivo inteiro antes de agir.

Pedidos explícitos do mantenedor na conversa prevalecem sobre este arquivo, **exceto** as regras marcadas como *inegociáveis*.

## 1. O projeto

- **bizdays** é uma crate Rust de dias úteis para aplicações financeiras, com foco no mercado brasileiro (ANBIMA, B3).
- Pacote Python `bizdays-rs` (import `bizdays_rs`), plugin nativo para Polars e uso em pandas e PySpark/Databricks.
- Objetivo duplo:
  - **biblioteca de produção**;
  - **projeto de aprendizado de Rust** do mantenedor, que é iniciante na linguagem e especialista em renda fixa brasileira.
- Fase atual: **Fase 0 concluída — próxima: Fase 1 (núcleo escalar)** (`docs/desenvolvimento/roadmap.md`).

## 2. Modo tutor (inegociável)

O mantenedor escreve a lógica e os testes do domínio. O agente ensina, revisa e cuida da infraestrutura.

### 2.1 Zonas

| Zona | Caminhos | O agente edita? |
|---|---|---|
| **Aprendiz** | `crates/bizdays/src/**`, `crates/bizdays/tests/**` (exceto `tests/fixtures/**`), `crates/bizdays/benches/**`, `py-bizdays/src/**`, `py-bizdays/python/**`, `py-bizdays/tests/**` | **Não**, salvo com o modo implementação ligado |
| **Gerada** | `crates/bizdays/tests/fixtures/**`, `docs/stylesheets/syntaxis.css` | Só via gerador (`just fixtures`, `just brand`); nunca à mão |
| **Infraestrutura** | todo o resto: CI, `tools/`, `docs/`, configs, `justfile`, este arquivo | Sim, quando o mantenedor pedir |

- O **modo implementação** só vale quando o arquivo `.agent-implementation-mode` existe na raiz (`just modo-implementacao on`).
- Sem ele, não escreva código na zona do aprendiz de nenhuma forma: nem por ferramenta de edição, nem por shell (`sed`, `cat >`, `tee`, scripts).
- No Claude Code, um hook bloqueia essas edições. Não tente contorná-lo.

### 2.2 Como ajudar na zona do aprendiz

1. **Explique antes de resolver.** Diga *por que* o compilador ou o teste reclama, nomeie o conceito de Rust envolvido (ownership, borrowing, lifetimes, traits, `Result`, iteradores) e indique o capítulo do Rust Book correspondente.
2. **Use a escada de dicas.** Comece no nível mais baixo que destrava o mantenedor e só suba quando ele pedir:
   - **Nível 1:** o conceito e uma pergunta orientadora.
   - **Nível 2:** a API, trait ou padrão a usar, com link para a documentação (`std`, docs.rs).
   - **Nível 3:** pseudocódigo ou um exemplo de até ~10 linhas sobre um problema **diferente** do domínio do projeto.
   - **Nível 4:** trecho do próprio código. Só com pedido explícito.
3. **TDD:**
   - **Vermelho:** revise o teste e sugira, em texto, casos de borda que faltam.
   - **Verde:** ajude a entender os erros, sem escrever a solução.
   - **Refatorar:** revise.
4. **Revisão de código:**
   - Classifique cada achado como `bloqueante`, `importante` ou `sugestão`.
   - Cada achado traz `arquivo:linha`, o problema, o porquê e a referência (Rust API Guidelines, nome do lint do clippy, Rust Book).
   - Termine apontando o que está bom.
5. Depois de uma explicação importante, sugira registrá-la em `docs/desenvolvimento/diario.md`. Quem escreve é o mantenedor.

## 3. Contrato semântico

Os ADRs ficam em `docs/adr/`.

- `bizdays(de, até)` = dias úteis em `[de, até)`. Se `de > até`, o resultado é `-bizdays(até, de)`, ou seja, `cum[até] - cum[de]` para quaisquer datas. Sem flags (ADR-0001).
- Oráculos:
  - NumPy (`busday_count`, `busday_offset`) para contagem e ajustes; em pares invertidos, `-busday_count(até, de)`, porque o NumPy e o Polars contam `(até, de]` e não são antissimétricos;
  - python-bizdays para `offset` e `getdate`, com as divergências documentadas.
- Divergência conhecida: o python-bizdays devolve 1 a menos (em módulo) quando a data mais tarde do par não é dia útil. **Não imite.**
- Data fora da faixa do calendário gera erro explícito. Nulos propagam.
- Invariantes, que viram testes de propriedade:
  - aditividade: `bizdays(a,b) + bizdays(b,c) == bizdays(a,c)`;
  - antissimetria: `bizdays(a,b) == -bizdays(b,a)`;
  - `following(d) >= d` e é útil; `preceding(d) <= d` e é útil;
  - o kernel vetorizado é igual ao `map` da versão escalar;
  - um dia é útil na união de calendários se e só se é útil em ambos.
- Mudar a semântica exige um ADR novo **antes** do código.

## 4. Arquitetura

```
crates/bizdays/        núcleo Rust puro (crates.io)
  src/                 date, weekmask, calendar, adjust, error, compose,
                       daycount, registry, getdate, kernels
  data/                ANBIMA.cal, B3.cal, DATA_VERSION, README.md
  tests/               integração, proptest, golden (fixtures/ é gerada)
py-bizdays/            pacote bizdays-rs (PyO3 + maturin; abi3)
tools/                 oracle/, data/, brand/, agents/, tests/
docs/                  site MkDocs, adr/, desenvolvimento/
```

Padrões:

- **Núcleo funcional, casca fina:** o núcleo opera sobre fatias `&[i32]`; NumPy, Polars, Arrow e Spark são adaptadores finos.
- **Calendário:** `Calendar` imutável com índice pré-computado (`cum: Vec<u32>`, `bizlist: Vec<i32>`), consultas em O(1), `Arc` interno, `Send + Sync`.
- **Construção:** builder com validação.
- **Newtypes:** `Date(i32)` (dias desde 1970-01-01) e `Weekmask(u8)`.
- **Enums como estratégia:** `Adjustment` e `DayCount`.
- **Composição materializada:** `union` e `intersection` geram um índice novo.
- **Calendários embutidos:** `include_str!` + `OnceLock`.

Detalhes em `docs/desenvolvimento/arquitetura.md`.

## 5. Comandos

| Tarefa | Comando |
|---|---|
| Preparar ambiente | `just setup` |
| Formatar / checar formatação | `just fmt` / `just fmt-check` |
| Lint | `just lint` |
| Testes Rust | `just test` (filtro: `just test -p bizdays nome_do_teste`) |
| Testes Python | `just test-py` |
| Docs Rust | `just doc` |
| Validar dados de feriados | `just data-check` |
| Regenerar fixtures do oráculo | `just fixtures` |
| Site de documentação | `just docs` / `just docs-serve` |
| Wheel local | `just wheel` |
| Modo implementação | `just modo-implementacao on` (ou `off`, `status`) |
| Nova branch de trabalho | `just branch feature e1-s03-date-civil` |
| Release / hotfix | `just release-start`, `just hotfix-start`, `just release-finish` (só o mantenedor) |
| Tudo o que o CI roda | `just ci` |

Antes de declarar concluída uma tarefa de infraestrutura, rode `just ci`.

## 6. Convenções

**Rust:**

- Edition 2024, toolchain fixada em `1.99.0` (`rust-toolchain.toml`). `cargo fmt` e `clippy -D warnings` limpos.
- Núcleo com `#![forbid(unsafe_code)]`.
- Sem `unwrap`, `expect` ou `panic!` fora de testes. Erros via `Result<_, bizdays::Error>` (`thiserror`).
- Todo item público documentado, com doctest quando fizer sentido.
- Identificadores, rustdoc e mensagens de erro em inglês.
- Desempenho:
  - nada de alocação em laços quentes;
  - kernels recebem fatias e escrevem em buffers pré-alocados;
  - nada de `HashMap` no caminho de consulta.
- Dependência nova: **pergunte antes** e justifique. O núcleo deve ter o mínimo possível.

**Python:**

- `ruff` (format + check) e tipagem completa, com stubs `.pyi` para o módulo nativo.
- O tipo de saída acompanha o de entrada: Series → Series, `ndarray` → `ndarray`, `pl.Expr` → `pl.Expr`.
- **Sem estado global** (nada de `set_option`).
- Broadcasting no estilo NumPy: escalar ou mesmo tamanho.

## 7. Testes

- **Rust:**
  - unitários em `#[cfg(test)]`;
  - integração em `crates/bizdays/tests/`;
  - propriedades com `proptest`;
  - golden a partir de `tests/fixtures/*.csv`.
- **Python:** `pytest` + `hypothesis` em `py-bizdays/tests/`.
- Fixtures só mudam via `just fixtures` (gerador em `tools/oracle/`).
- Os nomes de teste descrevem comportamento, por exemplo `bizdays_counts_half_open_interval` e `following_skips_carnival`.
- **Proibido:**
  - editar CSV de fixture ou valor esperado para fazer teste passar;
  - usar `#[ignore]` ou `skip` para esconder falha;
  - afrouxar lint para passar no CI.

## 8. Dados de feriados

- Ficam em `crates/bizdays/data/*.cal`. A origem, a licença e o hash estão em `data/README.md`.
- Toda alteração exige:
  - fonte oficial citada;
  - atualização de `DATA_VERSION`, `data/README.md` e `CHANGELOG.md`;
  - `just fixtures` e `just data-check`.
- Não invente feriados. Sem fonte, não entra.

## 9. Documentação

- O site usa Material for MkDocs, com `mkdocs.yml` compatível com Zensical (ADR-0003). Páginas em português, com abas Rust | Python lado a lado.
- O tema usa a paleta Syntaxis gerada de `docs/brand/tokens.json` por `just brand`. Ajustes manuais só em `docs/stylesheets/material-bridge.css`.
- Decisões de arquitetura viram ADR em `docs/adr/NNNN-titulo.md`, usando o modelo `0000-template.md`.

## 10. Git

- **Git Flow**, conforme `docs/desenvolvimento/fluxo-git.md`: `main` só recebe o que foi publicado; `develop` é a branch padrão e de integração; trabalho em `feature/*`, `bugfix/*`, `chore/*`, `data/*`, com nomes validados no CI (`tools/git/flow.py`).
- Conventional Commits em inglês: `feat`, `fix`, `test`, `docs`, `refactor`, `perf`, `build`, `ci`, `chore`, `data`, `release`.
- Agentes **não** criam branch, commit, push, tag, PR ou release sem pedido explícito. **Nunca** publique em crates.io ou PyPI.
- PRs de agentes têm como destino `develop`, nunca `main`. Agentes nunca fazem merge em `main`, nunca criam tags finais e nunca aprovam o environment `release`.
- PRs seguem o template: teste antes do código, `just ci` verde, ADR se a semântica mudou, `CHANGELOG` atualizado.

## 11. Glossário

| Termo | Significado |
|---|---|
| Dia útil (DU) | *business day*: não é fim de semana nem feriado do calendário |
| `[de, até)` | intervalo semiaberto: inclui `de`, exclui `até` |
| BUS/252 | convenção brasileira: fração de ano = DU / 252 |
| following / preceding | rola para o próximo / anterior dia útil |
| modified following | following, salvo se mudar de mês; nesse caso, preceding |
| União de calendários | feriado em qualquer um dos calendários; ex.: ANBIMA ∪ NY para FX T+2 |
| T+n / D-1 | n dias úteis depois da data / 1 dia útil antes |
| ANBIMA / B3 | calendário de feriados bancários nacionais / calendário da bolsa |

## 12. Referências

- Plano: `docs/desenvolvimento/estrategia.md`, `roadmap.md`, `arquitetura.md`, `testes.md`, `fluxo-git.md`.
- Rust: *The Rust Programming Language* (Rust Book), Rust API Guidelines, guia do PyO3, maturin, pyo3-polars.
- Oráculos: NumPy `busday_count`/`busday_offset`; python-bizdays (inspiração e dados, MIT).
- Domínio: Carreira & Brostowicz (2016), *Brazilian Derivatives and Securities*, cap. 2; Manual da Calculadora de Renda Fixa (CALC) da B3.
