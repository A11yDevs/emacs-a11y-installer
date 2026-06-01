# Tasks: Interactive CLI Context Mode

**Input**: Design documents from `/specs/002-interactive-cli-context/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Validation tasks are REQUIRED for primary user journeys and risk-critical flows.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare interactive CLI scaffolding and test harness entry points.

- [X] T001 Define interactive command surface and context scope in specs/002-interactive-cli-context/contracts/interactive-cli-contract.md
- [X] T002 Create interactive session module skeleton in src/emacs_a11y/cli/interactive.py
- [X] T003 [P] Create interactive data model module skeleton in src/emacs_a11y/models/interactive_cli.py
- [X] T004 [P] Create interactive unit test module skeleton in tests/unit/test_interactive_cli_models.py and tests/unit/test_interactive_cli_router.py
- [X] T005 [P] Create interactive integration test module skeleton in tests/integration/test_interactive_root_cli.py and tests/integration/test_interactive_doctor_cli.py
- [X] T006 [P] Create interactive contract test module skeleton in tests/contract/test_interactive_cli_contract.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build shared interactive infrastructure that blocks all user stories.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T007 Implement NavigationAction/CommandResult/InteractiveSessionState dataclasses in src/emacs_a11y/models/interactive_cli.py
- [X] T008 Implement CommandContext and CommandDefinition structures with validation helpers in src/emacs_a11y/models/interactive_cli.py
- [X] T009 Implement context tree builder for root and doctor contexts in src/emacs_a11y/cli/interactive.py
- [X] T010 [P] Implement global command router (`help`, `back`, `exit`) in src/emacs_a11y/cli/interactive.py
- [X] T011 [P] Implement invalid-command suggestion helper using difflib in src/emacs_a11y/cli/interactive.py
- [X] T012 Wire Typer entrypoint to start interactive mode when no subcommand is provided in src/emacs_a11y/cli/doctor.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Navegar no modo interativo raiz (Priority: P1) 🎯 MVP

**Goal**: Entrar em `emacs-a11y>` sem argumentos, receber ajuda automática e navegar com comandos globais acessíveis.

**Independent Test**: Executar `emacs-a11y` e validar prompt raiz, ajuda inicial, `help`, `back`, `exit` e encerramento limpo por EOF/interrupção.

### Tests (US1)

- [X] T013 [P] [US1] Write failing integration test for no-args entry showing `emacs-a11y>` and automatic help in tests/integration/test_interactive_root_cli.py
- [X] T014 [P] [US1] Write failing integration test for global commands `help`, `back`, `exit` in root context in tests/integration/test_interactive_root_cli.py
- [X] T015 [P] [US1] Write failing unit test for linear help rendering (`comando - descrição`) without color dependency in tests/unit/test_interactive_cli_router.py
- [X] T016 [P] [US1] Write failing integration test for EOF and KeyboardInterrupt clean exit semantics in tests/integration/test_interactive_root_cli.py

### Core (US1)

- [X] T017 [US1] Implement root prompt loop and line-reader abstraction for keyboard-only flow in src/emacs_a11y/cli/interactive.py
- [X] T018 [US1] Implement automatic contextual help rendering at session start in src/emacs_a11y/cli/interactive.py
- [X] T019 [US1] Implement root command catalog including `doctor` description and global command visibility in src/emacs_a11y/cli/interactive.py
- [X] T020 [US1] Implement root `back` behavior to terminate session with clear message in src/emacs_a11y/cli/interactive.py

### Integration (US1)

- [X] T021 [US1] Integrate interactive session bootstrap with existing CLI app lifecycle in src/emacs_a11y/cli/doctor.py
- [X] T022 [US1] Validate US1 flow by running targeted tests in tests/integration/test_interactive_root_cli.py and tests/unit/test_interactive_cli_router.py

**Checkpoint**: User Story 1 is independently functional and testable.

---

## Phase 4: User Story 2 - Navegar e executar ações no contexto doctor (Priority: P2)

**Goal**: Entrar em `emacs-a11y doctor>` e executar `run`, `json`, `explain` mantendo paridade com o modo direto não interativo.

**Independent Test**: Entrar em `doctor` via modo interativo, executar ações locais, retornar com `back` e validar equivalência com `emacs-a11y doctor` e `emacs-a11y doctor --json`.

### Tests (US2)

- [X] T023 [P] [US2] Write failing contract test for root/doctor context command availability from interactive-cli contract in tests/contract/test_interactive_cli_contract.py
- [X] T024 [P] [US2] Write failing integration test for `doctor` navigation (`root` -> `doctor` -> `back`) in tests/integration/test_interactive_doctor_cli.py
- [X] T025 [P] [US2] Write failing integration test for `run`, `json`, and `explain` actions inside doctor context in tests/integration/test_interactive_doctor_cli.py
- [X] T026 [P] [US2] Write failing compatibility tests to preserve direct mode behavior in tests/integration/test_doctor_text_cli.py and tests/integration/test_doctor_json_cli.py

### Core (US2)

- [X] T027 [US2] Implement doctor context command catalog with `run`, `json`, and `explain` definitions in src/emacs_a11y/cli/interactive.py
- [X] T028 [US2] Implement interactive `run` action reusing existing doctor text path in src/emacs_a11y/cli/interactive.py and src/emacs_a11y/doctor/orchestrator.py
- [X] T029 [US2] Implement interactive `json` action reusing existing doctor JSON path in src/emacs_a11y/cli/interactive.py and src/emacs_a11y/doctor/renderers/json.py
- [X] T030 [US2] Implement interactive `explain` action for checks metadata in src/emacs_a11y/cli/interactive.py and src/emacs_a11y/doctor/registry.py

### Integration (US2)

- [X] T031 [US2] Integrate doctor context transitions with shared stack-based navigation state in src/emacs_a11y/cli/interactive.py
- [X] T032 [US2] Validate US2 contract and integration scenarios in tests/contract/test_interactive_cli_contract.py and tests/integration/test_interactive_doctor_cli.py

**Checkpoint**: User Story 2 is independently functional and preserves direct doctor compatibility.

---

## Phase 5: User Story 3 - Receber feedback claro para comandos inválidos (Priority: P3)

**Goal**: Exibir mensagens claras para comando inválido com sugestões contextuais e manter a sessão estável.

**Independent Test**: Enviar comandos inválidos nos contextos raiz e doctor, verificar mensagem clara + sugestão, permanência de contexto e continuidade do loop.

### Tests (US3)

- [X] T033 [P] [US3] Write failing unit tests for invalid-command message normalization and suggestion cap (max 3) in tests/unit/test_interactive_cli_router.py
- [X] T034 [P] [US3] Write failing integration test for invalid command in root context with `help` guidance in tests/integration/test_interactive_root_cli.py
- [X] T035 [P] [US3] Write failing integration test for invalid command in doctor context preserving prompt/context in tests/integration/test_interactive_doctor_cli.py
- [X] T036 [P] [US3] Write failing accessibility-focused test for concise, linear error wording in tests/unit/test_interactive_cli_router.py

### Core (US3)

- [X] T037 [US3] Implement contextual invalid-command formatter with action-oriented guidance in src/emacs_a11y/cli/interactive.py
- [X] T038 [US3] Implement command similarity ranking and deterministic suggestion ordering in src/emacs_a11y/cli/interactive.py
- [X] T039 [US3] Implement non-fatal error handling to keep interactive session alive after invalid input in src/emacs_a11y/cli/interactive.py

### Integration (US3)

- [X] T040 [US3] Integrate invalid-command behavior across root and doctor command dispatch paths in src/emacs_a11y/cli/interactive.py
- [X] T041 [US3] Validate US3 behavior with targeted root/doctor integration tests in tests/integration/test_interactive_root_cli.py and tests/integration/test_interactive_doctor_cli.py

**Checkpoint**: User Story 3 is independently functional and robust for exploratory usage.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final quality, documentation, PlantUML updates, and regression validation across stories.

- [X] T042 [P] Update interactive usage documentation and command reference in docs/doctor-cli.md
- [X] T043 [P] Update quickstart validation steps for interactive mode in specs/002-interactive-cli-context/quickstart.md
- [X] T044 [P] Update architecture diagram for contextual command tree in docs/plantuml/doctor-architecture.puml
- [X] T045 [P] Update functional flow diagram for `help/back/exit` transitions in docs/plantuml/doctor-functional-flow.puml
- [X] T046 [P] Update interactive text sequence diagram in docs/plantuml/doctor-sequence-text.puml
- [X] T047 [P] Update interactive JSON sequence diagram in docs/plantuml/doctor-sequence-json.puml
- [X] T048 Run full regression for unit/integration/contract suites and record evidence in specs/002-interactive-cli-context/quickstart.md
- [X] T049 Run script-boundary regression ensuring no business logic migration to wrappers in tests/unit/test_script_boundary.py
- [X] T050 Final consistency pass across spec/plan/contracts/tasks documentation in specs/002-interactive-cli-context/spec.md, specs/002-interactive-cli-context/plan.md, specs/002-interactive-cli-context/contracts/interactive-cli-contract.md, and specs/002-interactive-cli-context/tasks.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational completion.
- **Polish (Phase 6)**: Depends on completion of all targeted user stories.

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2; no dependency on other stories.
- **US2 (P2)**: Starts after Phase 2; reuses shared interactive/session infrastructure and existing doctor domain logic.
- **US3 (P3)**: Starts after Phase 2; depends on established routing behavior from US1/US2 for full-context invalid handling.

### Within Each User Story

- Tests MUST be authored first and fail before implementation when testable.
- Core tasks implement business behavior after failing tests exist.
- Integration tasks connect flow end-to-end and validate independent completion.

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel.
- Foundational tasks T010 and T011 can run in parallel after model definitions.
- In each story, test tasks marked [P] can run in parallel.
- In Polish, documentation and PlantUML tasks marked [P] can run in parallel.

---

## Parallel Example: User Story 2

```bash
# Launch validation tasks for US2 together:
Task: "T023 [US2] Contract test for command availability in tests/contract/test_interactive_cli_contract.py"
Task: "T024 [US2] Navigation integration test in tests/integration/test_interactive_doctor_cli.py"
Task: "T025 [US2] Doctor actions integration test in tests/integration/test_interactive_doctor_cli.py"

# Launch implementation tasks for doctor actions in parallel after routing baseline:
Task: "T028 [US2] Interactive run action in src/emacs_a11y/cli/interactive.py"
Task: "T029 [US2] Interactive json action in src/emacs_a11y/cli/interactive.py"
Task: "T030 [US2] Interactive explain action in src/emacs_a11y/cli/interactive.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: User Story 1.
4. Stop and validate US1 independently before progressing.

### Incremental Delivery

1. Deliver US1 (interactive root navigation).
2. Deliver US2 (doctor context actions + non-interactive compatibility).
3. Deliver US3 (invalid-command clarity and resilience).
4. Finalize Polish (docs, PlantUML, and regression).

### Suggested MVP Scope

- Include T001-T022 (Setup + Foundational + US1).
- Defer US2/US3 and Polish for subsequent increments if needed.

---

## Notes

- [P] tasks indicate file-level parallelism with low merge conflict risk.
- [USx] labels provide end-to-end traceability to spec user stories.
- Every task includes explicit file path(s) for direct execution by an LLM agent.