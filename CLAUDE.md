@AGENTS.md

## Específico do Claude Code

- Um hook em `.claude/settings.json` bloqueia `Edit`/`Write` na zona do aprendiz quando o modo implementação está desligado. Não tente contorná-lo (por exemplo, escrevendo arquivos via Bash). Se precisar, peça ao usuário para rodar `just modo-implementacao on`.
- Para confirmar que as instruções carregaram, use `/context`.
