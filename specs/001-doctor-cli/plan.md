# Implementation Plan: Doctor CLI Acessível

**Branch**: `main` | **Date**: 2026-06-01 | **Spec**: `/specs/001-doctor-cli/spec.md`

**Input**: Feature specification from `/specs/001-doctor-cli/spec.md`

## Summary

Implementar a feature `emacs-a11y doctor` (texto) e `emacs-a11y doctor --json`
com arquitetura modular em pacote Python canônico (3.11+), em modo estritamente
somente leitura. A solução será composicional e orientada a checks
independentes, com núcleo comum para regras diagnósticas, adaptadores por
plataforma (Windows/macOS/Linux), renderizadores separados (texto/JSON),
mapeador de exit code e contrato JSON estável para suporte remoto e automação.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Typer (CLI), pytest (testes), biblioteca padrão
(`platform`, `pathlib`, `shutil`, `subprocess`, `json`, `dataclasses`, `typing`, `enum`)

**Storage**: N/A (execução efêmera; sem persistência obrigatória)

**Testing**: pytest + testes de snapshot/contrato JSON + integração CLI

**Target Platform**: Windows, macOS, Linux

**Project Type**: pacote Python multiplataforma (CLI)

**Performance Goals**: diagnóstico completo em até 3s em ambiente típico local

**Constraints**: somente leitura; sem criação de diretórios, downloads,
alteração de PATH, instalação de dependências ou elevação de privilégios

**Scale/Scope**: primeira feature do produto, foco em diagnóstico pré-instalação
com checks de ambiente, Emacs, perfil, configuração pessoal, TTS e Emacspeak

## Dependency Choices and Rationale

- **Typer**: escolhido sobre Click por API declarativa com type hints, menor
  boilerplate para subcomandos e opção de manter base simples, estável e legível
  para CLI acessível.
- **pytest**: escolhido por ecossistema consolidado para testes unitários,
  parametrizados e integração de CLI.
- **Biblioteca padrão**: priorizada para reduzir superfície de risco e
  dependências de runtime no pacote canônico.

## Constitution Check (Pre-Design Gate)

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Acessibilidade estrutural**: PASS. Saída textual linear e legível com
  severidade explícita e próximos passos.
- **CLI primária**: PASS. `doctor` e `doctor --json` cobrem jornada essencial.
- **Instalação não destrutiva**: PASS. Modo somente leitura como regra central.
- **Multiplataforma nativa**: PASS. Núcleo + adaptadores por SO.
- **Doctor-first**: PASS. Feature é pré-condição operacional para instalação.
- **Distribuição canônica**: PASS. Pacote Python canônico, compatível com `pipx`.
- **Scripts auxiliares**: PASS. `.ps1`/`.sh` restritos a bootstrap/adaptação.
- **Segurança e consentimento**: PASS. Sem operações sensíveis de escrita.
- **Modularidade por perfis**: PASS. Check explícito do perfil do Emacs Acessível.
- **Documentação operacional**: PASS. Artefatos de quickstart, contrato e docs previstos.

## Project Structure

### Documentation (this feature)

```text
specs/001-doctor-cli/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── doctor-cli-contract.md
│   └── doctor-report.schema.json
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── emacs_a11y/
    ├── cli/
    │   └── doctor.py
    ├── doctor/
    │   ├── orchestrator.py
    │   ├── registry.py
    │   ├── checks/
    │   │   ├── common.py
    │   │   ├── windows.py
    │   │   ├── macos.py
    │   │   └── linux.py
    │   ├── renderers/
    │   │   ├── text.py
    │   │   └── json.py
    │   ├── exit_codes.py
    │   └── logging.py
    └── models/
        └── diagnostic.py

tests/
├── unit/
│   ├── test_registry.py
│   ├── test_checks_common.py
│   ├── test_render_text.py
│   ├── test_render_json.py
│   └── test_exit_codes.py
├── integration/
│   ├── test_doctor_text_cli.py
│   └── test_doctor_json_cli.py
└── contract/
    └── test_doctor_json_schema.py

scripts/
├── bootstrap-doctor.ps1
└── bootstrap-doctor.sh
```

**Structure Decision**: projeto single-package Python, com `src/emacs_a11y`
como núcleo canônico e separação rígida entre orquestração, checks,
renderização e adaptadores de plataforma.

## Functional/Compositional Modeling Strategy

- Estratégia escolhida: **funcional/composicional com OO leve**.
- Cada check é uma função independente que recebe `EnvironmentState` e retorna
  `DiagnosticResult` (sem side effects de escrita).
- OO leve é usado apenas para entidades semânticas (`DiagnosticCheck`,
  `DiagnosticResult`, `DiagnosticReport`, `EnvironmentState`, `Severity`,
  `Status`) e interfaces simples de adaptador.
- Decisão evita hierarquia OO pesada e favorece testabilidade e composição.

## Diagnostic Check Matrix by Platform

| Check | Windows | macOS | Linux |
|------|---------|-------|-------|
| SO e arquitetura | Yes | Yes | Yes |
| Emacs disponível + versão | Yes | Yes | Yes |
| Git disponível | Yes | Yes | Yes |
| Python disponível | Yes | Yes | Yes |
| Perfil Emacs Acessível | Yes | Yes | Yes |
| Configuração pessoal Emacs | Yes | Yes | Yes |
| Sinais iniciais TTS/voz | Yes (SAPI/NVDA/OneCore sinais) | Yes (say/voz do sistema) | Yes (speech-dispatcher/espeak sinais) |
| Indícios Emacspeak | Yes | Yes | Yes |

## Accessible Text Output Strategy

- Ordem fixa e linear por seções: `Resumo`, `Críticos`, `Avisos`, `Info`,
  `Próximos passos`.
- Linhas curtas e sem dependência de cor.
- Marcadores de severidade textuais explícitos (`CRITICAL`, `WARNING`, `INFO`).
- Mensagens acionáveis com instruções concretas por check.
- Coerência 1:1 entre conteúdo textual e payload JSON.

## JSON Contract and Exit Codes

- Contrato JSON formalizado em `specs/001-doctor-cli/contracts/doctor-report.schema.json`.
- Contrato de CLI + semântica de saída em
  `specs/001-doctor-cli/contracts/doctor-cli-contract.md`.
- Exit codes planejados:
  - `0`: ambiente pronto (sem críticos e sem avisos)
  - `1`: ambiente com avisos, sem críticos
  - `2`: ambiente com falhas críticas
  - `3`: erro interno de execução do diagnóstico

## Test Strategy

- **Unitários**: checks isolados, renderizadores, mapeamento de exit code,
  normalização de evidências e regras de severidade/status.
- **Integração**: execução real do CLI em texto e JSON, com monkeypatch de
  ambiente para cenários multiplataforma simulados.
- **Contrato**: validação do JSON contra schema e snapshots para regressão.
- **Não regressão de somente leitura**: testes que garantem ausência de escrita
  em filesystem e ausência de chamadas de instalação/download.

## Technical Risks and Mitigation

- **Detecção TTS heterogênea por plataforma**:
  mitigação por heurísticas transparentes + status WARNING quando inconclusivo.
- **Ambientes com múltiplos Emacs**:
  mitigação com estratégia de priorização explícita (PATH/execução primária)
  e evidência no relatório.
- **Diferenças de PATH/permissão**:
  mitigação com mensagens de próximos passos específicas e sem side effects.
- **Divergência texto vs JSON**:
  mitigação via modelo único `DiagnosticReport` e renderização derivada.

## Documentation Strategy

- `quickstart.md` com fluxo de validação local e por `pipx`.
- Contratos em `contracts/`.
- Índice e casos de uso textuais em `docs/doctor-cli.md`.
- Diagramas PlantUML em `docs/plantuml/`.

## Planned Design Artifacts

- `specs/001-doctor-cli/research.md`
- `specs/001-doctor-cli/data-model.md`
- `specs/001-doctor-cli/quickstart.md`
- `specs/001-doctor-cli/contracts/doctor-cli-contract.md`
- `specs/001-doctor-cli/contracts/doctor-report.schema.json`
- `docs/doctor-cli.md`
- `docs/plantuml/doctor-use-cases.puml`
- `docs/plantuml/doctor-sequence-text.puml`
- `docs/plantuml/doctor-sequence-json.puml`
- `docs/plantuml/doctor-architecture.puml`
- `docs/plantuml/doctor-functional-flow.puml`

## Constitution Check (Post-Design Re-Check)

- **Acessibilidade estrutural**: PASS (renderização textual dedicada).
- **CLI primária**: PASS (comando CLI é ponto de entrada principal).
- **Instalação não destrutiva**: PASS (somente leitura em todos os checks).
- **Multiplataforma nativa**: PASS (adaptadores separados por SO).
- **Doctor-first**: PASS (planejamento centrado em diagnóstico pré-instalação).
- **Python canônico + distribuição em camadas**: PASS (pacote canônico + `pipx`).
- **Scripts como adaptadores**: PASS (sem regra diagnóstica em scripts).
- **Segurança/consentimento/reversibilidade**: PASS (nenhuma ação sensível).
- **Observabilidade**: PASS (JSON + logs sem segredos).
- **Documentação operacional**: PASS (quickstart + contratos + docs + diagramas).

## Complexity Tracking

Sem violações de constituição que exijam exceção.
