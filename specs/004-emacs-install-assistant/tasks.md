# Tasks: Emacs Install Assistant

**Input**: Design documents from `/specs/004-emacs-install-assistant/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md, contracts/emacs-install-cli-contract.md

**Tests**: Validacoes e testes sao obrigatorios para fluxos primarios e de risco critico desta feature.

**Organization**: Tasks grouped by user story so each story can be implemented and tested independently.

## Phase 1: Setup

**Purpose**: Preparar a estrutura de arquivos, stubs de teste e baseline minimo de artefatos operacionais da feature 004.

- [X] T001 Create feature module stub in src/emacs_a11y/install/emacs.py
- [X] T002 [P] Create environment detection stub in src/emacs_a11y/install/emacs_detector.py
- [X] T003 [P] Create install method recommendation stub in src/emacs_a11y/install/emacs_methods.py
- [X] T004 [P] Create assisted execution stub in src/emacs_a11y/install/emacs_executor.py
- [X] T005 [P] Create version policy stub in src/emacs_a11y/install/emacs_version.py
- [X] T006 [P] Create Emacs text renderer stub in src/emacs_a11y/install/renderers/emacs_text.py
- [X] T007 [P] Create Emacs install models stub in src/emacs_a11y/models/emacs_install.py
- [X] T008 [P] Create contract test stub in tests/contract/test_emacs_install_cli_contract.py
- [X] T009 [P] Create direct CLI integration test stub in tests/integration/test_install_emacs_cli.py
- [X] T010 [P] Create interactive integration test stub in tests/integration/test_install_emacs_interactive.py
- [X] T011 [P] Create regression integration test stub in tests/integration/test_install_emacs_regressions.py
- [X] T012 [P] Create detector unit test stub in tests/unit/test_emacs_detector.py
- [X] T013 [P] Create method recommendation unit test stub in tests/unit/test_emacs_methods.py
- [X] T014 [P] Create executor unit test stub in tests/unit/test_emacs_executor.py
- [X] T015 [P] Create version policy unit test stub in tests/unit/test_emacs_version.py
- [X] T016 [P] Create renderer unit test stub in tests/unit/test_emacs_render_text.py
- [X] T017 [P] Review and finalize contract baseline in specs/004-emacs-install-assistant/contracts/emacs-install-cli-contract.md
- [X] T018 [P] Review and finalize quickstart baseline in specs/004-emacs-install-assistant/quickstart.md
- [X] T019 [P] Review and finalize operational doc baseline in docs/emacs-install-assistant.md
- [X] T020 [P] Review and finalize design diagrams in docs/plantuml/emacs-install-use-cases.puml
- [X] T021 [P] Review and finalize design diagrams in docs/plantuml/emacs-install-sequence-guidance.puml
- [X] T022 [P] Review and finalize design diagrams in docs/plantuml/emacs-install-sequence-assisted.puml
- [X] T023 [P] Review and finalize design diagrams in docs/plantuml/emacs-install-sequence-interactive.puml
- [X] T024 [P] Review and finalize design diagrams in docs/plantuml/emacs-install-architecture.puml
- [X] T025 [P] Review and finalize design diagrams in docs/plantuml/emacs-install-functional-flow.puml

---

## Phase 2: Foundational

**Purpose**: Implementar a infraestrutura bloqueante comum a todas as user stories.

**CRITICAL**: Nenhuma user story deve comecar antes desta fase.

- [X] T026 Implement core dataclasses and enums in src/emacs_a11y/models/emacs_install.py
- [X] T027 Implement exit code mapping rules in src/emacs_a11y/models/emacs_install.py
- [X] T028 [P] Implement OS and architecture detection in src/emacs_a11y/install/emacs_detector.py
- [X] T029 [P] Implement TTY detection and non-interactive safety gate in src/emacs_a11y/install/emacs_detector.py
- [X] T030 [P] Implement Emacs PATH detection and selected path resolution in src/emacs_a11y/install/emacs_detector.py
- [X] T031 [P] Implement multiple Emacs candidate discovery and deterministic prioritization in src/emacs_a11y/install/emacs_detector.py
- [X] T032 [P] Implement Emacs version parser and normalization in src/emacs_a11y/install/emacs_version.py
- [X] T033 [P] Implement configurable minimum version policy assessment using `EMACS_A11Y_MIN_EMACS_VERSION` with safe fallback on missing/invalid values in src/emacs_a11y/install/emacs_version.py
- [X] T034 [P] Implement package manager detection and platform method selection in src/emacs_a11y/install/emacs_methods.py
- [X] T035 [P] Implement exact display_text and assisted execution eligibility rules in src/emacs_a11y/install/emacs_methods.py
- [X] T036 [P] Implement canonical status-marker renderer and consent summary renderer in src/emacs_a11y/install/renderers/emacs_text.py
- [X] T037 Implement doctor reuse adapter for platform, Emacs, version and PATH signals in src/emacs_a11y/install/emacs_detector.py
- [X] T038 Implement orchestration skeleton for guidance, dry-run and assisted branches in src/emacs_a11y/install/emacs.py
- [X] T039 Implement safe subprocess invocation wrapper with shell=False contract in src/emacs_a11y/install/emacs_executor.py
- [X] T040 Implement CLI routing for `install emacs` flags in src/emacs_a11y/cli/install.py
- [X] T041 Implement initial interactive routing hooks for `install > emacs` in src/emacs_a11y/cli/interactive.py
- [X] T042 Update interactive context state model for pending Emacs assistant flow in src/emacs_a11y/models/interactive_cli.py
- [X] T043 Implement foundational contract expectations for flags and exit codes in tests/contract/test_emacs_install_cli_contract.py
- [X] T044 Implement foundational unit coverage for version policy and exit mapping in tests/unit/test_emacs_version.py

**Checkpoint**: Base pronta para iniciar implementacao independente das user stories.

---

## Phase 3: User Story 1 - Recomendar instalacao segura do Emacs quando ele estiver ausente (Priority: P1) 🎯 MVP

**Goal**: Entregar guidance-only seguro por plataforma para pessoas sem Emacs instalado.

**Independent Test**: Executar `emacs-a11y install emacs` em Windows, macOS, Debian/Ubuntu e plataforma desconhecida, sem execucao automatica, com recomendacao correta e proximos passos.

### Validation for User Story 1

- [X] T045 [P] [US1] Add Windows-with-winget guidance integration test in tests/integration/test_install_emacs_cli.py
- [X] T046 [P] [US1] Add Windows-without-winget guidance integration test in tests/integration/test_install_emacs_cli.py
- [X] T047 [P] [US1] Add macOS-with-brew guidance integration test in tests/integration/test_install_emacs_cli.py
- [X] T048 [P] [US1] Add macOS-without-brew guidance integration test in tests/integration/test_install_emacs_cli.py
- [X] T049 [P] [US1] Add Debian/Ubuntu guidance-only integration test in tests/integration/test_install_emacs_cli.py
- [X] T050 [P] [US1] Add unsupported-platform guidance integration test in tests/integration/test_install_emacs_cli.py
- [X] T051 [P] [US1] Add renderer marker coverage for INFO/WARNING/COMMAND/NEXT STEP in tests/unit/test_emacs_render_text.py

### Implementation for User Story 1

- [X] T052 [US1] Implement Windows recommendation rules with `winget install -e --id GNU.Emacs` in src/emacs_a11y/install/emacs_methods.py
- [X] T053 [US1] Implement Windows manual guidance fallback when winget is unavailable in src/emacs_a11y/install/emacs_methods.py
- [X] T054 [US1] Implement macOS Homebrew recommendation `brew install emacs` and manual fallback in src/emacs_a11y/install/emacs_methods.py
- [X] T055 [US1] Implement Debian/Ubuntu guidance-only recommendation with privilege warning in src/emacs_a11y/install/emacs_methods.py
- [X] T056 [US1] Implement safe unknown-platform manual guidance in src/emacs_a11y/install/emacs_methods.py
- [X] T057 [US1] Implement guidance-only branch and next-step composition in src/emacs_a11y/install/emacs.py
- [X] T058 [US1] Implement direct CLI output wiring for guidance-only mode in src/emacs_a11y/cli/install.py
- [X] T059 [US1] Document MVP guidance-only behavior and next steps in docs/emacs-install-assistant.md
- [X] T060 [US1] Align quickstart scenarios for platform recommendations in specs/004-emacs-install-assistant/quickstart.md

**Checkpoint**: US1 entrega o MVP da feature com recomendacao segura sem execucao.

---

## Phase 4: User Story 2 - Executar instalacao assistida somente com consentimento explicito (Priority: P1)

**Goal**: Permitir execucao assistida apenas em metodos suportados, com resumo de consentimento, cancelamento seguro e reavaliacao pos-execucao.

**Independent Test**: Executar `emacs-a11y install emacs --execute` em metodo suportado e validar resumo, cancelamento, execucao exata, falha segura e pos-deteccao do Emacs.

### Validation for User Story 2

- [X] T061 [P] [US2] Add exact-command-before-execution integration test in tests/integration/test_install_emacs_cli.py
- [X] T062 [P] [US2] Add cancellation-without-execution integration test in tests/integration/test_install_emacs_cli.py
- [X] T063 [P] [US2] Add unsupported-method-or-platform execute safety test in tests/integration/test_install_emacs_cli.py
- [X] T064 [P] [US2] Add non-TTY execute rejection test in tests/integration/test_install_emacs_cli.py
- [X] T065 [P] [US2] Add executor shell=False and argv-shape unit tests in tests/unit/test_emacs_executor.py
- [X] T066 [P] [US2] Add assisted execution failure and exit code 3 test in tests/unit/test_emacs_executor.py
- [X] T067 [P] [US2] Add post-success re-detection guidance test in tests/integration/test_install_emacs_cli.py

### Implementation for User Story 2

- [X] T068 [US2] Implement execution consent summary composition in src/emacs_a11y/install/emacs.py
- [X] T069 [US2] Implement explicit confirmation and CANCELLED branch in src/emacs_a11y/install/emacs.py
- [X] T070 [US2] Implement documented-command subprocess execution wrapper in src/emacs_a11y/install/emacs_executor.py
- [X] T071 [US2] Implement accessible external-output summarization and FAILED mapping in src/emacs_a11y/install/renderers/emacs_text.py
- [X] T072 [US2] Implement post-install Emacs re-detection and shell/PATH/doctor guidance in src/emacs_a11y/install/emacs.py
- [X] T073 [US2] Enforce `--execute` support matrix and no-TTY safety checks in src/emacs_a11y/cli/install.py
- [X] T074 [US2] Update CLI contract for assisted execution, cancellation and non-TTY behavior in specs/004-emacs-install-assistant/contracts/emacs-install-cli-contract.md

**Checkpoint**: US2 adiciona execucao assistida segura sem afetar o comportamento guidance-only do MVP.

---

## Phase 5: User Story 3 - Reconhecer Emacs ja instalado e evitar reinstalacao desnecessaria (Priority: P1)

**Goal**: Detectar Emacs existente, classificar a versao e recomendar proximos passos sem reinstalar por padrao.

**Independent Test**: Executar `emacs-a11y install emacs` com Emacs presente em varios cenarios de versao e candidatos multiplos, validando caminho, aviso, ausencia de reinstalacao e proximos passos.

### Validation for User Story 3

- [X] T075 [P] [US3] Add installed-Emacs path reporting integration test in tests/integration/test_install_emacs_cli.py
- [X] T076 [P] [US3] Add parseable-version reporting integration test in tests/integration/test_install_emacs_cli.py
- [X] T077 [P] [US3] Add unknown-version WARNING integration test in tests/integration/test_install_emacs_cli.py
- [X] T078 [P] [US3] Add too-old-version update recommendation integration test in tests/integration/test_install_emacs_cli.py
- [X] T079 [P] [US3] Add multiple-Emacs candidate prioritization test in tests/unit/test_emacs_detector.py

### Implementation for User Story 3

- [X] T080 [US3] Implement installed-Emacs branch with path reporting in src/emacs_a11y/install/emacs.py
- [X] T081 [US3] Implement version assessment rendering for supported, unknown and too_old states in src/emacs_a11y/install/renderers/emacs_text.py
- [X] T082 [US3] Implement deterministic multiple-candidate selection warnings in src/emacs_a11y/install/emacs_detector.py
- [X] T083 [US3] Implement no-reinstall-by-default behavior and next-step recommendations in src/emacs_a11y/install/emacs.py
- [X] T084 [US3] Update documentation for installed Emacs scenarios in docs/emacs-install-assistant.md

**Checkpoint**: US3 completa o conjunto P1 com guidance para ambientes onde o Emacs ja existe.

---

## Phase 6: User Story 4 - Usar o assistente pelo modo interativo contextual (Priority: P2)

**Goal**: Oferecer o mesmo assistente de recomendacao e execucao assistida no contexto interativo `install > emacs`.

**Independent Test**: Navegar pelo shell interativo, acessar `install > emacs`, validar guidance-only e ramo assistido, preservando `help`, `back` e `exit`.

### Validation for User Story 4

- [X] T085 [P] [US4] Add install-context command listing integration test in tests/integration/test_install_emacs_interactive.py
- [X] T086 [P] [US4] Add interactive guidance-only flow integration test in tests/integration/test_install_emacs_interactive.py
- [X] T087 [P] [US4] Add interactive assisted-execution decision flow integration test in tests/integration/test_install_emacs_interactive.py
- [X] T088 [P] [US4] Add global help/back/exit preservation regression test in tests/integration/test_install_emacs_regressions.py

### Implementation for User Story 4

- [X] T089 [US4] Update install-context help text and local command listing in src/emacs_a11y/cli/interactive.py
- [X] T090 [US4] Wire `install > emacs` to the shared assistant orchestrator in src/emacs_a11y/cli/interactive.py
- [X] T091 [US4] Persist pending recommendation and consent state for interactive flow in src/emacs_a11y/models/interactive_cli.py
- [X] T092 [US4] Implement interactive prompt transitions for guidance-only vs assisted execution in src/emacs_a11y/cli/interactive.py
- [X] T093 [US4] Update interactive behavior section in specs/004-emacs-install-assistant/contracts/emacs-install-cli-contract.md

**Checkpoint**: US4 entrega equivalencia funcional entre modo direto e modo interativo.

---

## Phase 7: User Story 5 - Receber saida previsivel em guidance-only ou dry-run para suporte (Priority: P2)

**Goal**: Garantir saida estavel, remota e auditavel para suporte em guidance-only (padrao) e dry-run, sem execucao ou mudanca de sistema.

**Independent Test**: Executar o comando em guidance-only e `--dry-run` em diferentes plataformas, confirmando estabilidade da saida e ausencia total de chamadas externas e modificacoes locais.

### Validation for User Story 5

- [X] T094 [P] [US5] Add dry-run no-execution integration test in tests/integration/test_install_emacs_cli.py
- [X] T095 [P] [US5] Add guidance-only no-execution integration test in tests/integration/test_install_emacs_cli.py
- [X] T096 [P] [US5] Add unsupported-platform dry-run stability integration test in tests/integration/test_install_emacs_cli.py
- [X] T097 [P] [US5] Add no-personal-config-modification regression test in tests/integration/test_install_emacs_regressions.py
- [X] T098 [P] [US5] Add no-minimal-profile-creation regression test in tests/integration/test_install_emacs_regressions.py

### Implementation for User Story 5

- [X] T099 [US5] Implement dry-run branch with normalized recommendation output in src/emacs_a11y/install/emacs.py
- [X] T100 [US5] Implement stable support-oriented renderer output for dry-run and guidance-only in src/emacs_a11y/install/renderers/emacs_text.py
- [X] T101 [US5] Enforce zero external command invocation in dry-run mode in src/emacs_a11y/install/emacs_executor.py
- [X] T102 [US5] Update support-focused documentation for guidance-only and dry-run in docs/emacs-install-assistant.md
- [X] T103 [US5] Align quickstart support scenarios for dry-run and no-change guarantees in specs/004-emacs-install-assistant/quickstart.md

**Checkpoint**: US5 consolida o uso previsivel da feature para suporte remoto e documentacao operacional.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Finalizar cobertura transversal, regressao, consistencia documental e validacao operacional a partir do baseline criado na Phase 1.

- [X] T104 [P] Finalize CLI contract details for accepted commands, flags, exit codes, safety guarantees and reversibility guidance in specs/004-emacs-install-assistant/contracts/emacs-install-cli-contract.md
- [X] T105 [P] Finalize user-facing documentation for direct mode, interactive mode, platform guidance, observability notes, CLI help examples/effects/risks/reversal guidance and `--yes` out-of-scope rationale in docs/emacs-install-assistant.md
- [X] T106 [P] Finalize quickstart validation checklist in specs/004-emacs-install-assistant/quickstart.md
- [X] T107 [P] Finalize use-case diagram coverage in docs/plantuml/emacs-install-use-cases.puml
- [X] T108 [P] Finalize guidance sequence diagram coverage in docs/plantuml/emacs-install-sequence-guidance.puml
- [X] T109 [P] Finalize assisted sequence diagram coverage in docs/plantuml/emacs-install-sequence-assisted.puml
- [X] T110 [P] Finalize interactive sequence diagram coverage in docs/plantuml/emacs-install-sequence-interactive.puml
- [X] T111 [P] Finalize architecture diagram coverage in docs/plantuml/emacs-install-architecture.puml
- [X] T112 [P] Finalize functional flow diagram coverage in docs/plantuml/emacs-install-functional-flow.puml
- [X] T113 Run complete unit test suite for Emacs assistant in tests/unit/test_emacs_detector.py
- [X] T114 Run complete unit test suite for Emacs assistant in tests/unit/test_emacs_methods.py
- [X] T115 Run complete unit test suite for Emacs assistant in tests/unit/test_emacs_executor.py
- [X] T116 Run complete unit test suite for Emacs assistant in tests/unit/test_emacs_version.py
- [X] T117 Run complete unit test suite for Emacs assistant in tests/unit/test_emacs_render_text.py
- [X] T118 Run integration coverage for direct mode, dry-run and assisted execution in tests/integration/test_install_emacs_cli.py
- [X] T119 Run integration coverage for interactive mode in tests/integration/test_install_emacs_interactive.py
- [X] T120 Run regression coverage for doctor, doctor --json and install --profile minimal in tests/integration/test_install_emacs_regressions.py
- [X] T121 Run contract validation for CLI surface and exit codes in tests/contract/test_emacs_install_cli_contract.py
- [X] T122 Validate textual accessibility markers and absence of color dependency in src/emacs_a11y/install/renderers/emacs_text.py
- [X] T123 Validate that guidance-only and dry-run do not alter system state in tests/integration/test_install_emacs_regressions.py
- [X] T124 Validate that assisted execution does not alter PATH or personal Emacs configuration in tests/integration/test_install_emacs_regressions.py
- [X] T125 Validate that assisted execution does not create a minimal profile or install Emacspeak/TTS in tests/integration/test_install_emacs_regressions.py
- [X] T126 Review consistency across specs/004-emacs-install-assistant/spec.md, specs/004-emacs-install-assistant/plan.md, specs/004-emacs-install-assistant/data-model.md, specs/004-emacs-install-assistant/contracts/emacs-install-cli-contract.md, specs/004-emacs-install-assistant/quickstart.md and docs/emacs-install-assistant.md
- [X] T127 Mark final readiness checklist for feature 004 in specs/004-emacs-install-assistant/checklists/requirements.md
- [X] T128 Implement textual execution logging with sensitive-data redaction in src/emacs_a11y/install/emacs.py
- [X] T129 [P] Implement logger support for assisted execution result summaries in src/emacs_a11y/install/emacs_executor.py
- [X] T130 [P] Add unit tests for redaction and log-event coverage in tests/unit/test_emacs_executor.py
- [X] T131 [P] Add integration tests asserting relevant flow logs without sensitive leaks in tests/integration/test_install_emacs_cli.py
- [X] T132 [P] Document reversibility strategy and manual rollback limits in docs/emacs-install-assistant.md
- [X] T133 [P] Validate reversibility section and rollback limitations in specs/004-emacs-install-assistant/contracts/emacs-install-cli-contract.md
- [X] T134 [P] Validate `emacs-a11y install emacs --help` contract coverage for examples, effects, risks and reversibility guidance in tests/contract/test_emacs_install_cli_contract.py
- [X] T135 [P] Add explicit contract/integration validation for all FR-037 status markers by scenario (`INFO`, `WARNING`, `CRITICAL`, `COMMAND`, `CONFIRM`, `CANCELLED`, `NEXT STEP`, `SKIPPED`, `SUCCESS`, `FAILED`) in tests/contract/test_emacs_install_cli_contract.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1: Setup**: no dependencies; starts immediately.
- **Phase 2: Foundational**: depends on Phase 1; blocks all user stories.
- **Phase 3: US1**: depends on Phase 2; defines the MVP.
- **Phase 4: US2**: depends on Phase 2 and integrates on top of US1 behavior.
- **Phase 5: US3**: depends on Phase 2; can proceed in parallel with US2 after foundation.
- **Phase 6: US4**: depends on Phase 2 and shared orchestrator behavior from US1-US3.
- **Phase 7: US5**: depends on Phase 2 and reuses renderer/orchestrator branches from US1-US3.
- **Phase 8: Polish**: depends on all desired user stories being complete.

### User Story Dependencies

- **US1 (P1)**: can start immediately after Foundational and is the MVP.
- **US2 (P1)**: depends on foundational orchestration and method selection from Phase 2; benefits from US1 recommendation paths but remains independently testable.
- **US3 (P1)**: depends on foundational detection/version policy and remains independently testable.
- **US4 (P2)**: depends on shared assistant orchestration behavior from US1-US3.
- **US5 (P2)**: depends on guidance/dry-run rendering behavior built in US1-US3.

### Within Each User Story

- Validation tasks must be created before implementation tasks.
- Detection/models before orchestration.
- Orchestration before CLI or interactive wiring.
- Contract/docs updates after behavior is stabilized for that story.

### Parallel Opportunities

- Setup tasks marked `[P]` can run in parallel because they touch different files.
- Foundational detector, version, method and renderer tasks marked `[P]` can run in parallel.
- Validation tasks within each story marked `[P]` can run in parallel.
- Documentation and PlantUML polish tasks marked `[P]` can run in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch US1 validation tasks in parallel
T045 tests/integration/test_install_emacs_cli.py
T046 tests/integration/test_install_emacs_cli.py
T047 tests/integration/test_install_emacs_cli.py
T048 tests/integration/test_install_emacs_cli.py
T049 tests/integration/test_install_emacs_cli.py
T050 tests/integration/test_install_emacs_cli.py
T051 tests/unit/test_emacs_render_text.py

# Launch US1 platform recommendation implementations in parallel
T052 src/emacs_a11y/install/emacs_methods.py
T053 src/emacs_a11y/install/emacs_methods.py
T054 src/emacs_a11y/install/emacs_methods.py
T055 src/emacs_a11y/install/emacs_methods.py
T056 src/emacs_a11y/install/emacs_methods.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: US1.
4. Stop and validate the MVP with platform guidance-only scenarios.

### Incremental Delivery

1. Setup + Foundational create the stable substrate.
2. US1 delivers immediate value for people sem Emacs instalado.
3. US2 adds assisted execution without breaking guidance-only.
4. US3 covers already-installed Emacs flows.
5. US4 adds interactive parity.
6. US5 hardens support and dry-run predictability.

### Team Strategy

1. One person can own detector/version policy while another owns renderer/CLI after Phase 2.
2. US2 and US3 can proceed in parallel after foundational tasks complete.
3. US4 and US5 can begin once shared orchestration branches stabilize.

---

## Notes

- `[P]` means different files or independently parallelizable slices.
- `[US1]` to `[US5]` provide user-story traceability.
- Every task includes exact file paths.
- `--yes` stays out of scope in v1 and therefore has no implementation task.
- Guidance-only is the default and must remain intact through all phases.