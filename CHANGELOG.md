# Changelog

Todas as mudanças relevantes deste projeto são registradas aqui.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adota o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added

- Configuração inicial (Fase 0): workspace Cargo, esqueleto da crate `bizdays`
  e do pacote Python `bizdays-rs`, `justfile`, CI, site de documentação, ADRs
  0001–0005 e configuração de agentes (modo tutor).
- Calendários ANBIMA e B3 importados do python-bizdays 1.0.19
  (dados `2026.10.0`).
- Gerador de fixtures do oráculo (NumPy e python-bizdays). Pares invertidos
  seguem `-busday_count(até, de)` (ADR-0001, opção antissimétrica).

### Fixed

- Dados `2026.10.1`: removida a duplicata `2079-04-21` do `ANBIMA.cal`
  (Tiradentes coincide com a Sexta-feira Santa). Nenhum dia útil muda.
