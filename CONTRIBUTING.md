# Contribuindo

Obrigado pelo interesse! Este projeto é também um projeto de aprendizado de
Rust, então o fluxo tem algumas regras próprias.

- **Leia o `AGENTS.md`** na raiz: ele define o contrato semântico, as
  convenções, o modo tutor e as zonas do repositório. Vale para pessoas e
  agentes de IA.
- **Comandos:** tudo passa pelo `justfile`. `just setup` prepara o ambiente e
  `just ci` roda o mesmo que o CI. Veja `just --list`.
- **TDD:** escreva o teste antes do código. Fixtures em
  `crates/bizdays/tests/fixtures/` só mudam via `just fixtures`.
- **Semântica:** mudou a semântica? Escreva um ADR em `docs/adr/` antes.
- **Dados de feriados:** só com fonte oficial citada (seção 8 do `AGENTS.md`).
- **Branches:** Git Flow, descrito em `docs/desenvolvimento/fluxo-git.md`.
  Crie a branch com `just branch <tipo> <descrição>` a partir de `develop`; o
  CI recusa nomes e PRs fora do padrão.
- **Commits:** Conventional Commits em inglês.
- **Pull requests:** para `develop` (squash), seguindo o template
  (`.github/pull_request_template.md`) e atualizando o `CHANGELOG.md`.
