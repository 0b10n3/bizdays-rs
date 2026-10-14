# 0004 — Modo tutor

- **Status:** Aceito
- **Data:** 2026-10-13

## Contexto

O projeto é biblioteca de produção e, ao mesmo tempo, o projeto de aprendizado
de Rust do mantenedor. Se agentes de IA escreverem a lógica, o aprendizado não
acontece.

## Decisão

- **Zonas** (`AGENTS.md`, seção 2.1): aprendiz (código e testes do domínio),
  gerada (fixtures, CSS da marca) e infraestrutura (o resto).
- **Escada de dicas** de 4 níveis: conceito → API → exemplo em outro domínio →
  trecho do próprio código (só com pedido explícito).
- **Modo implementação:** agentes só editam a zona do aprendiz quando
  `.agent-implementation-mode` existe na raiz (`just modo-implementacao on`).
  O arquivo é ignorado pelo git.
- **Hook do Claude Code:** `.claude/settings.json` roda
  `tools/agents/guard_learner_zone.py` antes de `Edit`/`Write`/`NotebookEdit`
  e bloqueia (código 2) edições na zona do aprendiz sem o modo ligado.

## Consequências

- O mantenedor escreve a lógica; agentes ensinam, revisam e mantêm a
  infraestrutura.
- O hook não cobre escrita via shell; isso é regra do `AGENTS.md`, não
  barreira técnica.
- Outros agentes (Gemini etc.) dependem só das instruções do `AGENTS.md`.
