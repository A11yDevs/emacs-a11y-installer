# Quickstart: Doctor CLI Acessivel

## Prerequisites
- Python 3.11+
- Ambiente local em Windows, macOS ou Linux

## Install (development)
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

## Run JSON diagnostic
```bash
emacs-a11y doctor --json
```

## Validate read-only behavior
- Confirmar que nao houve criacao/alteracao de arquivos de configuracao apos execucao.
- Confirmar ausencia de instalacao de pacotes e de comandos de elevacao.

## Run tests
```bash
pytest -q
```

## Contract validation (JSON)
- Executar testes de contrato que validam o JSON contra `contracts/doctor-report.schema.json`.

## Expected exit codes
- `0`: ambiente pronto
- `1`: ambiente com avisos
- `2`: ambiente com bloqueios criticos
- `3`: erro interno de execucao
