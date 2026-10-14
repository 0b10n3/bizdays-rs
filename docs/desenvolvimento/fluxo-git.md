# Fluxo Git e padrão de branches

## 1. Modelo: Git Flow

O projeto segue **Git Flow** desde o primeiro dia, com a dinâmica de um pacote em produção:

- `main` contém **apenas o que foi publicado**. Cada commit nela corresponde a uma versão no crates.io ou no PyPI e tem uma tag.
- `develop` é a linha de integração. O trabalho da semana entra nela, sempre verde, e ela representa a próxima versão.
- Versões são **preparadas** em `release/*`, **corrigidas em produção** em `hotfix/*` e, depois da primeira versão incompatível, **mantidas** em `support/*`.

### Branches permanentes e temporárias

| Branch | Vida | Nasce de | Entra em | Para que serve |
|---|---|---|---|---|
| `main` | permanente | — | — | código publicado; só recebe `release/*` e `hotfix/*` |
| `develop` | permanente | `main` (uma vez) | `release/*` | integração; branch padrão do GitHub |
| `support/<pacote>-<X.Y>.x` | permanente | tag de uma versão | — | manutenção de uma linha antiga (ex.: `0.1.x` depois da 0.2) |
| `feature/*` | até 1 semana | `develop` | `develop` | funcionalidade, testes, refatoração, desempenho |
| `bugfix/*` | dias | `develop` ou `release/*` | a mesma de origem | correção de algo **ainda não publicado** |
| `chore/*` | dias | `develop` | `develop` | infraestrutura: CI, build, dependências, docs |
| `data/*` | dias | `develop` | `develop` | dados de feriados e fixtures derivadas |
| `release/<pacote>-<versão>` | até 1 semana | `develop` | `main` **e** `develop` | congelar, estabilizar e publicar uma versão |
| `hotfix/<pacote>-<versão>` | horas a dias | `main` (ou `support/*`) | `main` **e** `develop` (ou só `support/*`) | correção urgente de algo **já publicado** |
| `spike/*` | livre | `develop` | **nunca** | experimento descartável |

Sobre o nome "`release/*` permanentes": no Git Flow, `release/*` é temporária. Ela existe enquanto a versão é estabilizada e é apagada depois do merge. A linha permanente para manter uma versão antiga é `support/*`, que este documento já prevê.

### Diagrama

```
                    (squash)                (merge commit)         (tag + aprovação)
feature/* ─────────────────▶ develop ──▶ release/* ─────────────▶ main ──────────────▶ crates.io / PyPI
bugfix/*, chore/*, data/*      ▲          (congela)                 │
                               │                                    │
                               └──────────── back-merge ────────────┘
                                                                    │
                     main ──▶ hotfix/* ───── merge commit ─────────▶ main ──▶ tag ──▶ publicação ──▶ back-merge em develop
```

## 2. Nome das branches

### Formato

| Tipo | Formato | Exemplos |
|---|---|---|
| Trabalho do plano | `<tipo>/<épico>-s<semana>-<descrição>` | `feature/e1-s03-date-civil`, `data/e4-s14-ny-calendar` |
| Trabalho fora do plano | `<tipo>/<descrição>` | `bugfix/csv-header-parsing`, `chore/ci-cache-uv` |
| Release | `release/<pacote>-<versão>` | `release/bizdays-0.1.0`, `release/bizdays-rs-0.1.0` |
| Hotfix | `hotfix/<pacote>-<versão nova>` | `hotfix/bizdays-0.1.1` |
| Support | `support/<pacote>-<X.Y>.x` | `support/bizdays-0.1.x` |

**Regras:**
- `<tipo>` é um de `feature`, `bugfix`, `chore`, `data` ou `spike`.
- O épico vai de `e0` a `e9` e a semana tem 2 dígitos (`s03`), ambos do `plano-semanal.md`.
- A descrição tem de 1 a 6 palavras, em kebab-case e em inglês, sem acentos.
- `<pacote>` é `bizdays` (crate) ou `bizdays-rs` (Python).

### Regex validada no CI

Sintaxe PCRE (use `grep -P` ou Python; o `[[ =~ ]]` do bash não aceita lookahead):

```
^((feature|bugfix|chore|data|spike)/(e[0-9]-s[0-9]{2}-|(?!e[0-9]-s))[a-z0-9]+(-[a-z0-9]+){0,5}|(release|hotfix)/bizdays(-rs)?-[0-9]+\.[0-9]+\.[0-9]+|support/bizdays(-rs)?-[0-9]+\.[0-9]+\.x)$
```

Isentas: `main`, `develop` e `dependabot/**`.

### Origem e destino permitidos nos PRs

Um job do CI (`pr-flow`) recusa PRs fora desta tabela:

| Destino (base) | Origens aceitas |
|---|---|
| `main` | `release/*`, `hotfix/*` |
| `develop` | `feature/*`, `bugfix/*`, `chore/*`, `data/*`, `dependabot/**`, `main` (back-merge), `release/*` (back-merge) |
| `release/*` | `bugfix/*` |
| `support/*` | `hotfix/*` |

## 3. Estratégia de merge

O Git Flow só funciona se `main` e `develop` compartilham a história. Por isso, cada caminho tem seu método:

| Caminho | Método | Por quê |
|---|---|---|
| `feature/*`, `bugfix/*`, `chore/*`, `data/*` → `develop` | **squash** | um commit limpo por entrega semanal |
| `bugfix/*` → `release/*` | **squash** | idem |
| `release/*` → `main` | **merge commit** (`--no-ff`) | preserva os commits de `develop`; squash aqui faria `main` e `develop` divergirem |
| `hotfix/*` → `main` | **merge commit** | idem |
| `main` → `develop` (back-merge) | **merge commit** | traz versão, CHANGELOG e hotfixes de volta |
| `hotfix/*` → `support/*` | **merge commit** | idem |

Nunca use rebase nem squash em `release/*` e `hotfix/*` depois de abrir o PR para `main`.

## 4. Fluxos

### 4.1 Semana normal (feature)

1. Sincronize e crie a branch:

   ```bash
   git switch develop && git pull --ff-only
   just branch feature e1-s03-date-civil       # valida o nome e cria a partir de develop
   ```

2. Trabalhe em ciclos TDD, com commits pequenos. Dentro da branch, as mensagens podem ser granulares:

   ```
   test: add failing test for 1970-01-01 epoch
   feat: implement days_from_civil
   ```

3. Mantenha a branch atualizada:

   ```bash
   git fetch origin && git rebase origin/develop
   git push --force-with-lease
   ```

   Rebase só na sua própria branch, nunca em `develop`, `main`, `release/*` ou `support/*`.

4. Quando `just ci` estiver verde, abra o PR para `develop`:

   ```bash
   gh pr create --base develop --fill
   ```

5. Peça a revisão da IA, corrija os bloqueantes e faça squash merge. O título do PR vira o commit (seção 5).

Regras:
- Uma branch de feature vive no máximo uma semana; se passar disso, divida o trabalho.
- Cada PR tem idealmente até ~400 linhas, sem contar as fixtures geradas.
- `develop` nunca fica vermelha.

### 4.2 Release

A release congela `develop`, estabiliza o resultado e publica.

| Passo | Onde | Ação |
|---|---|---|
| 1 | `develop` | Confirme que o épico está fechado e o CI verde. `just release-start bizdays 0.1.0` cria `release/bizdays-0.1.0` |
| 2 | `release/*` | **Congelamento:** a partir daqui, só entram correções, documentação e bump de versão, via `bugfix/*` → `release/*`. O trabalho novo continua em `develop` |
| 3 | `release/*` | Atualize a versão no `Cargo.toml` (ou `py-bizdays/Cargo.toml`) e mova `Unreleased` → `## bizdays 0.1.0 — AAAA-MM-DD` no `CHANGELOG.md` |
| 4 | `release/*` | **Release candidate:** tag `bizdays-v0.1.0-rc.1`. O CI roda `cargo publish --dry-run`; para o pacote Python, publica `0.1.0rc1` no **TestPyPI**. Teste a instalação num projeto limpo. Se houver problema, corrija e gere `rc.2` |
| 5 | GitHub | PR `release/bizdays-0.1.0` → `main`, título `release: bizdays 0.1.0`, **merge commit** |
| 6 | `main` | `just release-finish bizdays 0.1.0` cria a tag anotada `bizdays-v0.1.0` e faz push. A tag dispara o `release.yml`, que espera **sua aprovação** no environment `release` e publica |
| 7 | GitHub | PR `main` → `develop`, título `chore: back-merge bizdays-v0.1.0`, **merge commit** |
| 8 | — | Apague a branch de release, confira crates.io, docs.rs e PyPI, e publique as notas de versão do GitHub a partir do CHANGELOG |

Só pode existir **uma** `release/*` aberta por vez.

### 4.3 Hotfix

Use hotfix quando há um defeito numa versão **publicada** que não pode esperar a próxima release. Exemplos: um feriado errado ou faltando, uma contagem incorreta, um pânico.

1. `just hotfix-start bizdays 0.1.1` cria `hotfix/bizdays-0.1.1` a partir de `main`.
2. Escreva primeiro o **teste que reproduz o defeito**, depois a correção, o bump do *patch* e a entrada no CHANGELOG.
3. Abra o PR para `main` com merge commit. O título é o da correção, por exemplo `fix(core): include 2027 carnival in ANBIMA calendar`.
4. Rode `just release-finish bizdays 0.1.1` (tag + publicação com aprovação).
5. Faça o back-merge `main` → `develop`. Se houver uma `release/*` aberta, leve a correção também para ela, via `bugfix/*`.

Atualização de feriados após uma mudança legal é o caso típico de hotfix de dados: `hotfix/bizdays-0.1.2`, com `DATA_VERSION` atualizado e fonte oficial citada.

### 4.4 Support (manutenção de versões antigas)

- Crie `support/bizdays-0.1.x` a partir da tag `bizdays-v0.1.x` mais recente **somente** quando a 0.2 já estiver publicada e alguém precisar de correção na 0.1.
- Hotfixes para essa linha nascem do `support/*`, entram nele por merge commit e são marcados com tags lá (ex.: `bizdays-v0.1.3`).
- Se a correção também valer para a versão atual, ela segue o fluxo normal de hotfix em `main`.

### 4.5 Spike

`spike/*` sai de `develop` e **nunca** recebe merge. O que se aprende vira um ADR ou uma `feature/*` nova. Apague a branch depois de registrar o resultado.

## 5. Mensagens de commit e títulos de PR

O título do PR vira a mensagem do commit na branch de destino. Ele segue [Conventional Commits](https://www.conventionalcommits.org/), em inglês:

```
<tipo>(<escopo opcional>): <descrição no imperativo, minúscula, sem ponto>
```

| Tipo | Uso típico | Branch de origem |
|---|---|---|
| `feat` | funcionalidade nova | `feature/*` |
| `fix` | correção de bug | `bugfix/*`, `hotfix/*` |
| `test`, `refactor`, `perf` | testes, estrutura, desempenho | `feature/*` |
| `docs`, `build`, `ci`, `chore` | documentação e infraestrutura | `chore/*` |
| `data` | feriados | `data/*`, `hotfix/*` |
| `release` | preparação de versão | `release/*` |

**Escopos:** `core`, `py`, `polars`, `spark`, `data`, `oracle`, `docs`, `ci`, `deps`.

**Mudança incompatível:** acrescente `!` (`feat(core)!: rename adjust to roll`) e explique no corpo, num bloco `BREAKING CHANGE:`. Na série `0.x`, isso força o *minor* (`0.1` → `0.2`).

**Rodapés:** `Closes: #12`, `Refs: #12`, `ClickUp: <id>`, `ADR: 0005`.

## 6. Versões, tags e publicação

- **SemVer** em `0.x` até a API estabilizar.
- O crate e o pacote Python têm **versões independentes**:
  - crate: tag `bizdays-vX.Y.Z`;
  - Python: tag `bizdays-rs-vX.Y.Z`;
  - release candidates: sufixo `-rc.N` na tag (para o Python, isso vira `X.Y.Zrc N` no PyPI, conforme a PEP 440).
- `develop` mantém a versão da última release; o bump acontece **só** em `release/*` e `hotfix/*`.
- Os dados de feriados têm versão própria (`crates/bizdays/data/DATA_VERSION`, `AAAA.MM.N`). Uma mudança de dados publicada gera um *patch* do crate.

| Evento | O CI faz |
|---|---|
| push em `feature/*` e afins, PRs | CI completo |
| push em `develop` | CI completo + wheels de desenvolvimento como artefatos + preview da documentação como artefato |
| tag `*-rc.*` | dry-run no crates.io; TestPyPI para o pacote Python |
| tag final em `main` | `release.yml`: aprovação manual no environment `release` → crates.io / PyPI → GitHub Release → deploy da documentação |

## 7. Proteção das branches (GitHub Rulesets)

| Regra | `main` | `develop` | `release/*`, `hotfix/*` | `support/*` |
|---|---|---|---|---|
| Exigir PR | sim | sim | não (commits do bump vêm por PR `bugfix/*` ou direto) | sim |
| Aprovações | 0 (projeto solo: revisão da IA + checklist) | 0 | — | 0 |
| Status checks obrigatórios | todos + `pr-flow` | todos + `pr-flow` | CI roda em push | todos |
| Métodos de merge | só **merge commit** | **squash** e **merge commit** (back-merges) | — | só merge commit |
| Histórico linear | não | não | — | não |
| Force push / exclusão | bloqueados | bloqueados | force push bloqueado | bloqueados |
| Tags `bizdays-v*`, `bizdays-rs-v*` | só criadas por você; não podem ser apagadas nem movidas | | | |

Outras configurações do repositório:
- **Branch padrão: `develop`.** PRs e clones apontam para ela por padrão.
- O dependabot usa `target-branch: develop`.
- A mensagem padrão de squash e de merge commit é o título do PR.
- Apagar a branch após o merge: ligado (o GitHub não apaga `main`, `develop` nem `support/*` protegidas).

## 8. O plano semanal no Git Flow

| Semanas | Branches | Release |
|---|---|---|
| 1 | `chore/e0-s01-repo-setup` (`main` e `develop` criadas aqui) | — |
| 2–11 | `feature/*`, `data/*`, `chore/*` → `develop` | — |
| **12** | `release/bizdays-0.1.0-alpha.1` | **bizdays 0.1.0-alpha.1** (crates.io; primeira publicação, manual) |
| 13–16 | `feature/*`, `data/*`, `chore/*` → `develop` | — |
| **17** | `release/bizdays-0.1.0` | **bizdays 0.1.0** (crates.io) |
| 18–19 | `feature/e7-*` → `develop`; `spike/e7-s20-cum-u16` | — |
| **20** | `release/bizdays-0.2.0` (kernels vetorizados) | **bizdays 0.2.0** |
| **21** | `feature/e8-*` → `develop`; no fim, `release/bizdays-rs-0.1.0-alpha.1` | **bizdays-rs 0.1.0a1** (PyPI) |
| 22–24 | `feature/e8-*` → `develop` | — |
| **25** | `release/bizdays-rs-0.1.0` | **bizdays-rs 0.1.0** (PyPI) |
| 26–27 | `feature/e9-*`, `chore/e9-*` → `develop` | — |
| **28** | `release/bizdays-rs-0.2.0` (Arrow/Spark) | **bizdays-rs 0.2.0** + lançamento |
| a qualquer momento | `hotfix/*` a partir de `main` | patch |

Ritual da semana de release:
- o trabalho do épico seguinte **não para**: ele continua em `develop` enquanto a release estabiliza;
- reserve de 1 a 2 h para o RC, o teste de instalação limpa e o back-merge.

## 9. Agentes de IA no fluxo

- Agentes **não** criam branch, commit, push, tag, PR ou release sem pedido explícito (`AGENTS.md`, seção 10).
- PRs de agentes têm como destino **`develop`**, nunca `main`. Agentes nunca fazem merge em `main`, nunca criam tags finais e nunca aprovam o environment `release`.
- Quando pedido, seguem este documento: nome de branch, título de PR, método de merge e rodapés. Commits de agentes levam o rodapé de coautoria da ferramenta.
- O modo implementação (`.agent-implementation-mode`) é local e ignorado pelo Git. Desligue-o (`just modo-implementacao off`) antes de abrir o PR.

## 10. Referência rápida

```bash
# semana normal
git switch develop && git pull --ff-only
just branch feature e2-s06-calendar-index
#   ... TDD, commits ...
git fetch origin && git rebase origin/develop && git push --force-with-lease
just ci && gh pr create --base develop --fill            # squash merge

# release
just release-start bizdays 0.1.0                          # release/bizdays-0.1.0 a partir de develop
#   bump + CHANGELOG; tag bizdays-v0.1.0-rc.1; testar
gh pr create --base main --title "release: bizdays 0.1.0" # merge commit
just release-finish bizdays 0.1.0                          # tag na main → publicação com aprovação
gh pr create --base develop --head main --title "chore: back-merge bizdays-v0.1.0"

# hotfix
just hotfix-start bizdays 0.1.1                            # a partir de main
#   teste que reproduz → correção → bump → CHANGELOG
gh pr create --base main --title "fix(core): <descrição>"  # merge commit
just release-finish bizdays 0.1.1 && gh pr create --base develop --head main --title "chore: back-merge bizdays-v0.1.1"
```
