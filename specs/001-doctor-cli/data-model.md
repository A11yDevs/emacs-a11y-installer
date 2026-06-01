# Data Model: Doctor CLI Acessivel

## Overview
O modelo combina entidades de dominio simples com fluxo composicional de checks.

## Enums

### Severity
- `CRITICAL`: bloqueia avanco para instalacao.
- `WARNING`: risco ou incompletude que nao bloqueia totalmente.
- `INFO`: informacao contextual.

### Status
- `PASS`: check validado sem problema.
- `FAIL`: check nao atendido.
- `UNKNOWN`: check inconclusivo para a plataforma/ambiente.

## Entities

### DiagnosticCheck
- Purpose: Descrever metadados e funcao executora de um check.
- Fields:
  - `id: str`
  - `name: str`
  - `description: str`
  - `platform_scope: list[str]` (`common`, `windows`, `macos`, `linux`)
  - `run(state: EnvironmentState) -> DiagnosticResult`

### DiagnosticResult
- Purpose: Resultado individual de um check.
- Fields:
  - `check_id: str`
  - `status: Status`
  - `severity: Severity`
  - `summary: str`
  - `evidence: list[str]`
  - `next_steps: list[str]`
  - `is_read_only: bool` (sempre `true`)

### EnvironmentState
- Purpose: Snapshot observado do ambiente local.
- Fields:
  - `os_name: str`
  - `os_version: str | None`
  - `architecture: str`
  - `path_entries: list[str]`
  - `emacs_version: str | None`
  - `git_available: bool`
  - `python_available: bool`
  - `profile_path: str`
  - `profile_exists: bool`
  - `profile_accessible: bool`
  - `user_emacs_paths: list[str]`
  - `tts_signals: list[str]`
  - `emacspeak_signals: list[str]`

### DiagnosticReport
- Purpose: Fonte de verdade para renderizacao textual e JSON.
- Fields:
  - `report_version: str`
  - `generated_at: str` (ISO 8601)
  - `environment: EnvironmentState`
  - `results: list[DiagnosticResult]`
  - `summary_counts: SummaryCounts`
  - `next_steps: list[str]`
  - `exit_code: int`

### SummaryCounts
- Purpose: Agregacao de resultados.
- Fields:
  - `critical: int`
  - `warning: int`
  - `info: int`
  - `pass: int`
  - `fail: int`
  - `unknown: int`

## Relationships
- `DiagnosticReport` contains many `DiagnosticResult`.
- `DiagnosticCheck` produces one `DiagnosticResult` given one `EnvironmentState`.
- `EnvironmentState` e lido por todos os checks e nao e mutado pelos checks.

## Validation Rules
- `is_read_only` MUST ser `true` em todos os resultados.
- `exit_code` MUST seguir o mapeamento:
  - `0`: sem warnings e sem critical.
  - `1`: com warnings e sem critical.
  - `2`: com pelo menos um critical.
  - `3`: erro interno do diagnostico.
- `summary_counts` MUST ser consistente com `results`.
- `next_steps` MUST conter acoes concretas para checks `FAIL` e `UNKNOWN` relevantes.
