# Quickstart: Doctor CLI Acessivel

## Prerequisites
- Python 3.11+
- Ambiente local em Windows, macOS ou Linux

## Install (development)
```bash
python -m pip install -U pip
python -m pip install -e .[dev]
```

## Install (development, minimal runtime)
```bash
python -m pip install -e .
```

## Install (preferred technical user path)
```bash
pipx install .
```

## Run textual diagnostic
```bash
emacs-a11y doctor
```

## Read command help
```bash
emacs-a11y --help
emacs-a11y doctor --help
```

## Run JSON diagnostic
```bash
emacs-a11y doctor --json
```

## Validate read-only behavior
- Confirmar que nao houve criacao/alteracao de arquivos de configuracao apos execucao.
- Confirmar ausencia de instalacao de pacotes e de comandos de elevacao.
- Confirmar que wrappers `scripts/bootstrap-doctor.sh` e `scripts/bootstrap-doctor.ps1`
	apenas delegam para `emacs-a11y doctor`.

## Run tests
```bash
pytest -q
```

## Run focused suites
```bash
pytest tests/unit -q
pytest tests/integration -q
pytest tests/contract -q
```

## Contract validation (JSON)
- Executar testes de contrato que validam o JSON contra `contracts/doctor-report.schema.json`.

## SC-004 measurement protocol (>=90%)

1. Definir um conjunto de pelo menos 10 cenarios com dependencias ausentes.
2. Executar `emacs-a11y doctor` em cada cenario.
3. Marcar cada cenario como sucesso quando os proximos passos forem acionaveis
	sem suporte adicional imediato.
4. Calcular taxa de sucesso: `sucessos / total`.
5. Critério de aprovacao: taxa >= 0.90.

## SC-006 cross-channel parity protocol (paridade)

Comparar os mesmos cenarios entre canais quando o standalone existir, garantindo paridade funcional:

1. Pacote Python (`pipx` ou `pip`).
2. Executavel standalone.

Para cada cenario, validar equivalencia de:

- checks presentes;
- severidades;
- proximos passos;
- codigo de saida.

Critério de aprovacao: 100% de equivalencia para a matriz definida.

## Distribution parity matrix template

| Scenario | Package channel | Standalone channel | Equivalent |
|---------|------------------|--------------------|------------|
| Missing Python | TBD | TBD | TBD |
| Missing Git | TBD | TBD | TBD |
| Profile inaccessible | TBD | TBD | TBD |
| TTS inconclusive | TBD | TBD | TBD |

## Expected exit codes
- `0`: ambiente pronto
- `1`: ambiente com avisos
- `2`: ambiente com bloqueios criticos
- `3`: erro interno de execucao
