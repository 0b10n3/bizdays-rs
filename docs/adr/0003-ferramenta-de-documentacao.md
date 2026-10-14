# 0003 — Ferramenta de documentação

- **Status:** Aceito
- **Data:** 2026-10-13

## Contexto

O Material for MkDocs entrou em modo de manutenção em novembro de 2025; a 9.7 é
a versão final. O mesmo time lançou o Zensical, que lê `mkdocs.yml`.

## Decisão

- Usar `mkdocs==1.6.1` com `mkdocs-material` 9.7.x.
- Manter o `mkdocs.yml` compatível com Zensical: só os plugins `search` e
  `mkdocstrings`, e extensões padrão do Python-Markdown e do PyMdown.
- Tema com a paleta Syntaxis: `tools/brand/tokens_to_css.py` gera
  `docs/stylesheets/syntaxis.css` a partir de `docs/brand/tokens.json` (SSOT);
  ajustes manuais só em `material-bridge.css`.

## Consequências

- Site estável hoje, sem depender de recursos novos do Material.
- Migrar para o Zensical deve ser trocar o comando de build.
- Plugins fora da lista exigem um novo ADR.
