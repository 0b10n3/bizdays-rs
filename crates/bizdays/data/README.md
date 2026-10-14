# Dados de feriados

Calendários de feriados embutidos na crate `bizdays`.

## Origem

| Campo | Valor |
|---|---|
| Projeto | [python-bizdays](https://github.com/wilsonfreitas/python-bizdays), de Wilson Freitas |
| Pacote | `bizdays` 1.0.19 (PyPI) |
| Licença | MIT — texto em [`LICENSE-python-bizdays.txt`](LICENSE-python-bizdays.txt) |
| Importação | 2026-10-13 |
| Versão dos dados | `2026.10.1` (arquivo [`DATA_VERSION`](DATA_VERSION)) |

Os arquivos foram copiados de dentro do pacote instalado
(`pathlib.Path(bizdays.__file__).parent`). O `B3.cal` está idêntico ao
original; o `ANBIMA.cal` difere só pela remoção de uma duplicata (abaixo).

| Arquivo | SHA-256 | Feriados | Primeiro | Último |
|---|---|---|---|---|
| `ANBIMA.cal` | `1c385197308a55de5d0731c6059e73651dd66c63bbdb0872f572978c5cff1e12` | 1.275 | 2000-01-01 | 2099-12-25 |
| `B3.cal` | `a3daa3f6511eee0cd2ff941bf7c3a9c86475bb415b2ccef8f4641761b9f550d7` | 427 | 2000-01-01 | 2026-12-31 |

**Duplicata removida (dados `2026.10.1`):** o `ANBIMA.cal` do upstream lista
`2079-04-21` duas vezes, porque Tiradentes coincide com a Sexta-feira Santa
(Páscoa em 23/04/2079). A segunda linha foi removida. Isso não muda nenhum dia
útil, só a lista. O original tinha SHA-256
`052b79fd79496024d6f00b5672c6dac05473ff2850938e83d726a70b22bc0b96`. Agora o
validador recusa qualquer duplicata.

**Atenção à faixa do B3:** ele termina em 2026-12-31. Datas a partir de 2027
ficam fora da faixa e geram erro explícito até os dados serem atualizados.

## Formato `.cal`

Texto UTF-8, um item por linha, linhas em branco ignoradas:

1. primeiro, os nomes em inglês dos dias da semana não úteis (`Saturday`, `Sunday`);
2. depois, os feriados em ISO 8601 (`AAAA-MM-DD`), em ordem crescente.

Validação: `just data-check`.

## Política de atualização

Segue a seção 8 do [`AGENTS.md`](../../../AGENTS.md):

- toda alteração cita uma fonte oficial;
- atualize `DATA_VERSION` (versionamento por data, `AAAA.MM.N`), este README
  (hashes, contagens, faixa) e o `CHANGELOG.md`;
- rode `just fixtures` e `just data-check`;
- não invente feriados: sem fonte, não entra.

## Pendência: calendário NY

O calendário **NY** ainda não existe. A fonte será definida no ADR-0002: o
calendário bancário dos EUA (Federal Reserve), usado em FX T+2 — **não** o da
NYSE. Não crie `NY.cal` sem fonte.
