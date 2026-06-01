# Tasks: Doctor CLI Acessivel

**Input**: Design documents from `/specs/001-doctor-cli/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Validation tasks are REQUIRED for primary user journeys and risk-critical flows.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Define canonical Python packaging metadata and CLI entrypoint `emacs-a11y` in pyproject.toml
- [ ] T002 Configure core runtime and test dependencies (`typer`, `pytest`) in pyproject.toml
- [ ] T003 Create canonical package layout stubs in src/emacs_a11y/cli/doctor.py and src/emacs_a11y/models/diagnostic.py
- [ ] T004 [P] Create doctor module layout stubs in src/emacs_a11y/doctor/orchestrator.py, src/emacs_a11y/doctor/registry.py, src/emacs_a11y/doctor/exit_codes.py, and src/emacs_a11y/doctor/logging.py
- [ ] T005 [P] Create check adapter module stubs in src/emacs_a11y/doctor/checks/common.py, src/emacs_a11y/doctor/checks/windows.py, src/emacs_a11y/doctor/checks/macos.py, and src/emacs_a11y/doctor/checks/linux.py
- [ ] T006 [P] Create renderer module stubs in src/emacs_a11y/doctor/renderers/text.py and src/emacs_a11y/doctor/renderers/json.py
- [ ] T007 [P] Create test package skeleton and placeholders in tests/unit/.gitkeep, tests/integration/.gitkeep, and tests/contract/.gitkeep
- [ ] T008 Document pipx installation and entrypoint smoke-check procedure in specs/001-doctor-cli/quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Implement diagnostic domain dataclasses/enums (`Severity`, `Status`, `EnvironmentState`, `DiagnosticResult`, `DiagnosticReport`) in src/emacs_a11y/models/diagnostic.py
- [ ] T010 Implement exit code mapping policy (0/1/2/3) in src/emacs_a11y/doctor/exit_codes.py
- [ ] T011 Implement check registry contract and execution ordering in src/emacs_a11y/doctor/registry.py
- [ ] T012 Implement orchestrator backbone that builds one source-of-truth report in src/emacs_a11y/doctor/orchestrator.py
- [ ] T013 [P] Implement structured logging with sensitive-data redaction hooks in src/emacs_a11y/doctor/logging.py
- [ ] T014 [P] Implement CLI command wiring and `--help` baseline in src/emacs_a11y/cli/doctor.py
- [ ] T015 [P] Create foundational unit tests for model, registry, and exit code policy in tests/unit/test_registry.py and tests/unit/test_exit_codes.py
- [ ] T016 [P] Create foundational integration smoke test for CLI boot in tests/integration/test_doctor_text_cli.py
- [ ] T017 Create/align CLI behavioral contract in specs/001-doctor-cli/contracts/doctor-cli-contract.md
- [ ] T018 Create/align JSON schema contract in specs/001-doctor-cli/contracts/doctor-report.schema.json
- [ ] T019 [P] Create contract validation harness in tests/contract/test_doctor_json_schema.py
- [ ] T020 Create script-boundary compliance checks ensuring no diagnostic business rules in scripts/bootstrap-doctor.ps1 and scripts/bootstrap-doctor.sh
- [ ] T021 [P] Define and document multiplatform verification matrix (Windows/macOS/Linux) in docs/doctor-cli.md
- [ ] T022 Define command-surface roadmap and acceptance boundaries for `install`, `update`, and `remove` aligned with constitution in docs/doctor-cli.md and specs/001-doctor-cli/quickstart.md

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Diagnosticar o ambiente antes da instalacao (Priority: P1) 🎯 MVP

**Goal**: Entregar `emacs-a11y doctor` textual acessivel, somente leitura, com checks essenciais e proximos passos acionaveis.

**Independent Test**: Executar `emacs-a11y doctor` em ambiente com dependencias faltantes e validar severidades explicitas, secoes lineares, proximos passos e ausencia de alteracao no sistema.

### Validation for User Story 1 (REQUIRED for primary and risk-critical flows) ⚠️

> **NOTE: Write these validations FIRST, ensure they FAIL before implementation**

- [ ] T023 [P] [US1] Specify textual acceptance scenarios and check-to-severity mapping in tests/integration/test_doctor_text_cli.py
- [ ] T024 [P] [US1] Write failing integration test asserting ordered sections (`Resumo`, `Criticos`, `Avisos`, `Info`, `Proximos passos`) in tests/integration/test_doctor_text_cli.py
- [ ] T025 [P] [US1] Write failing accessibility test asserting explicit severity tokens (`CRITICAL`, `WARNING`, `INFO`) without color dependence in tests/unit/test_render_text.py
- [ ] T026 [P] [US1] Write failing read-only guard tests (no file writes, no downloads, no dependency installs, no admin prompts) in tests/integration/test_doctor_text_cli.py
- [ ] T027 [P] [US1] Write failing multiplatform monkeypatch tests for inconclusive checks, multiple Emacs binaries, and permission-denied paths in tests/unit/test_checks_common.py

### Implementation for User Story 1

- [ ] T028 [US1] Implement common environment probes for OS and architecture in src/emacs_a11y/doctor/checks/common.py
- [ ] T029 [US1] Implement common probes for Emacs detection/version and Python availability in src/emacs_a11y/doctor/checks/common.py
- [ ] T030 [US1] Implement common probe for Git availability as optional non-blocking check in src/emacs_a11y/doctor/checks/common.py
- [ ] T031 [US1] Implement common probes for Emacs Acessivel profile state and personal Emacs configuration discovery in src/emacs_a11y/doctor/checks/common.py
- [ ] T032 [P] [US1] Implement Windows TTS initial-signal checks in src/emacs_a11y/doctor/checks/windows.py
- [ ] T033 [P] [US1] Implement macOS TTS initial-signal checks in src/emacs_a11y/doctor/checks/macos.py
- [ ] T034 [P] [US1] Implement Linux TTS initial-signal checks in src/emacs_a11y/doctor/checks/linux.py
- [ ] T035 [US1] Implement Emacspeak signal detection and integrate with common checks in src/emacs_a11y/doctor/checks/common.py
- [ ] T036 [US1] Register common and platform-specific checks with deterministic order in src/emacs_a11y/doctor/registry.py
- [ ] T037 [US1] Implement textual renderer with linear accessible output and deduplicated next steps in src/emacs_a11y/doctor/renderers/text.py
- [ ] T038 [US1] Integrate orchestrator execution path for text mode in src/emacs_a11y/doctor/orchestrator.py
- [ ] T039 [US1] Integrate CLI `doctor` command with text mode and exit code propagation in src/emacs_a11y/cli/doctor.py

### Validate and Document for User Story 1

- [ ] T040 [US1] Validate MVP textual flow by running US1 integration and unit tests in tests/integration/test_doctor_text_cli.py and tests/unit/test_render_text.py
- [ ] T041 [US1] Document textual diagnostic UX examples and troubleshooting guidance in docs/doctor-cli.md

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Consumir o diagnostico em automacao e suporte (Priority: P2)

**Goal**: Entregar `emacs-a11y doctor --json` com paridade semantica ao modo textual e conformidade de contrato.

**Independent Test**: Executar `emacs-a11y doctor --json` e validar schema, paridade com texto (mesmos achados/severidades/proximos passos) e exit code correspondente.

### Validation for User Story 2 (REQUIRED for primary and risk-critical flows) ⚠️

- [ ] T042 [P] [US2] Specify JSON acceptance scenarios and parity criteria in tests/integration/test_doctor_json_cli.py
- [ ] T043 [P] [US2] Write failing contract test for JSON payload against schema in tests/contract/test_doctor_json_schema.py
- [ ] T044 [P] [US2] Write failing integration test for semantic parity between text and JSON outputs in tests/integration/test_doctor_json_cli.py
- [ ] T045 [P] [US2] Write failing test for JSON exit-code determinism with critical/warning/ready scenarios in tests/integration/test_doctor_json_cli.py

### Implementation for User Story 2

- [ ] T046 [US2] Align JSON data model field names with schema contract in src/emacs_a11y/models/diagnostic.py and specs/001-doctor-cli/contracts/doctor-report.schema.json
- [ ] T047 [US2] Implement JSON renderer serialization preserving report semantics in src/emacs_a11y/doctor/renderers/json.py
- [ ] T048 [US2] Implement orchestrator JSON rendering branch with shared source-of-truth report in src/emacs_a11y/doctor/orchestrator.py
- [ ] T049 [US2] Integrate CLI `doctor --json` output path and error handling in src/emacs_a11y/cli/doctor.py
- [ ] T050 [US2] Finalize CLI contract wording for structured output and exit behavior in specs/001-doctor-cli/contracts/doctor-cli-contract.md
- [ ] T051 [US2] Define packaged-channel parity harness and scenario matrix (package vs standalone) in tests/integration/test_doctor_json_cli.py and specs/001-doctor-cli/quickstart.md

### Validate and Document for User Story 2

- [ ] T052 [US2] Validate JSON contract and parity suite in tests/contract/test_doctor_json_schema.py and tests/integration/test_doctor_json_cli.py
- [ ] T053 [US2] Document JSON usage examples for automation/support in docs/doctor-cli.md

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Proteger configuracao pessoal existente do Emacs (Priority: P3)

**Goal**: Reforcar protecao nao destrutiva da configuracao pessoal existente e tornar a orientacao de preservacao explicita.

**Independent Test**: Executar `emacs-a11y doctor` com configuracoes pessoais existentes e validar deteccao/report sem escrita, sem sugestoes destrutivas implicitas e com orientacao de preservacao.

### Validation for User Story 3 (REQUIRED for primary and risk-critical flows) ⚠️

- [ ] T054 [P] [US3] Specify preservation-focused acceptance scenarios in tests/integration/test_doctor_text_cli.py
- [ ] T055 [P] [US3] Write failing integration test for detection/report of multiple personal Emacs paths in tests/integration/test_doctor_text_cli.py
- [ ] T056 [P] [US3] Write failing integration test for inaccessible profile path (permission denied) classified without creating directories in tests/integration/test_doctor_text_cli.py
- [ ] T057 [P] [US3] Write failing no-overwrite guidance test for personal config findings in tests/unit/test_checks_common.py

### Implementation for User Story 3

- [ ] T058 [US3] Implement personal-config protection messaging and preservation next-steps in src/emacs_a11y/doctor/checks/common.py
- [ ] T059 [US3] Implement explicit profile-absence and profile-inaccessible reporting in src/emacs_a11y/doctor/checks/common.py
- [ ] T060 [US3] Refine text renderer wording to avoid destructive implications in src/emacs_a11y/doctor/renderers/text.py
- [ ] T061 [US3] Integrate preservation-focused result aggregation for next steps in src/emacs_a11y/doctor/orchestrator.py

### Validate and Document for User Story 3

- [ ] T062 [US3] Validate US3 preservation test suite in tests/integration/test_doctor_text_cli.py and tests/unit/test_checks_common.py
- [ ] T063 [US3] Document preservation guidance and safe follow-up actions in docs/doctor-cli.md

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T064 [P] Run full unit/integration/contract regression suite and record results in specs/001-doctor-cli/quickstart.md
- [ ] T065 [P] Validate `--help` and `doctor` linear readability and accessibility wording in src/emacs_a11y/cli/doctor.py and docs/doctor-cli.md
- [ ] T066 [P] Validate script-boundary compliance for `.ps1`/`.sh` wrappers in scripts/bootstrap-doctor.ps1 and scripts/bootstrap-doctor.sh
- [ ] T067 [P] Validate PlantUML diagrams against implemented flow in docs/plantuml/doctor-use-cases.puml, docs/plantuml/doctor-sequence-text.puml, docs/plantuml/doctor-sequence-json.puml, docs/plantuml/doctor-architecture.puml, and docs/plantuml/doctor-functional-flow.puml
- [ ] T068 [P] Update quickstart examples for `emacs-a11y doctor`, `emacs-a11y doctor --json`, and `pipx install .` in specs/001-doctor-cli/quickstart.md
- [ ] T069 [P] Define SC-004 measurement protocol (sample size, baseline, pass threshold >=90%) and record evidence format in specs/001-doctor-cli/quickstart.md and tests/integration/test_doctor_text_cli.py
- [ ] T070 [P] Define SC-006 cross-channel equivalence protocol and acceptance matrix in specs/001-doctor-cli/quickstart.md and tests/integration/test_doctor_json_cli.py
- [ ] T071 Final consistency pass for docs/spec/contracts alignment in docs/doctor-cli.md and specs/001-doctor-cli/contracts/doctor-cli-contract.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 (MVP) first for initial delivery
  - US2 after US1 baseline to reuse report model/orchestrator
  - US3 after US1 baseline to harden preservation behavior
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational completion; no dependency on other stories
- **User Story 2 (P2)**: Depends on US1 shared report pipeline for semantic parity
- **User Story 3 (P3)**: Depends on US1 core checks/text flow and extends protection semantics

### Within Each User Story

- Specification and validation tasks MUST be written first
- Tests MUST fail before implementation when applicable
- Check implementation before renderer integration
- Renderer integration before CLI integration
- Story-specific validation and documentation close the story

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel
- Foundational tasks marked [P] can run in parallel
- In US1, platform adapters (Windows/macOS/Linux) can be implemented in parallel
- In US2, contract/parity tests can run in parallel
- In US3, scenario-specific tests can run in parallel
- In Phase 6, docs/diagram/quickstart validations can run in parallel

---

## Parallel Example: User Story 1

```bash
# Run US1 failing validations together:
Task: "T023 [US1] ordered sections test in tests/integration/test_doctor_text_cli.py"
Task: "T024 [US1] severity accessibility test in tests/unit/test_render_text.py"
Task: "T025 [US1] read-only guard test in tests/integration/test_doctor_text_cli.py"
Task: "T026 [US1] multiplatform monkeypatch tests in tests/unit/test_checks_common.py"

# Implement platform adapters in parallel:
Task: "T031 [US1] Windows TTS checks in src/emacs_a11y/doctor/checks/windows.py"
Task: "T032 [US1] macOS TTS checks in src/emacs_a11y/doctor/checks/macos.py"
Task: "T033 [US1] Linux TTS checks in src/emacs_a11y/doctor/checks/linux.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate US1 independently with textual accessibility and read-only guarantees

### Incremental Delivery

1. Deliver US1 (`emacs-a11y doctor` textual accessible MVP)
2. Deliver US2 (`--json` contract + parity)
3. Deliver US3 (protection hardening for personal configs)
4. Execute Polish phase for documentation, PlantUML, and cross-cutting validations

### Suggested MVP Scope

- Include only Phase 1 + Phase 2 + Phase 3 (through T041) for first releasable increment
- Defer JSON and advanced preservation hardening to Phase 4 and Phase 5
