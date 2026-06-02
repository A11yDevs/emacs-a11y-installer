# Tasks: Minimal Profile Install

**Input**: Artefatos de design em /specs/003-minimal-profile-install/

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md, .specify/memory/constitution.md

**Tests**: Validacoes e testes sao obrigatorios para jornadas principais e fluxos criticos de seguranca.

**Organization**: Tarefas agrupadas por user story para permitir implementacao e teste independente.

## Format: [ID] [P?] [Story] Description

- [P]: executavel em paralelo (arquivos diferentes, sem dependencia de tarefa incompleta)
- [Story]: US1, US2, US3, US4 ou US5
- Todas as tarefas incluem caminho de arquivo explicito

## Phase 1: Setup

**Purpose**: Preparar estrutura de codigo, recursos e testes para a feature 003.

- [X] T001 Criar pacote de instalacao em src/emacs_a11y/install/__init__.py
- [X] T002 Criar comando CLI de install em src/emacs_a11y/cli/install.py
- [X] T003 [P] Criar modulo de preflight em src/emacs_a11y/install/preflight.py
- [X] T004 [P] Criar orquestrador de install em src/emacs_a11y/install/orchestrator.py
- [X] T005 [P] Criar planejador sem escrita em src/emacs_a11y/install/planner.py
- [X] T006 [P] Criar resolvedor de templates em src/emacs_a11y/install/templates.py
- [X] T007 [P] Criar utilitarios de perfil minimal em src/emacs_a11y/install/profile.py
- [X] T008 [P] Criar writer de artefatos project-owned em src/emacs_a11y/install/writer.py
- [X] T009 [P] Criar validator de artefatos e runtime em src/emacs_a11y/install/validator.py
- [X] T010 [P] Criar rollback guidance em src/emacs_a11y/install/rollback.py
- [X] T011 [P] Criar renderizador textual em src/emacs_a11y/install/renderers/text.py
- [X] T012 Criar modelos de instalacao em src/emacs_a11y/models/install.py
- [X] T013 Criar recurso base early-init em src/emacs_a11y/resources/a11y-emacs/early-init.el
- [X] T014 [P] Criar recurso base init em src/emacs_a11y/resources/a11y-emacs/init.el
- [X] T015 [P] Criar modulo init-packages em src/emacs_a11y/resources/a11y-emacs/lisp/init-packages.el
- [X] T016 [P] Criar modulo init-core em src/emacs_a11y/resources/a11y-emacs/lisp/init-core.el
- [X] T017 [P] Criar modulo init-dired em src/emacs_a11y/resources/a11y-emacs/lisp/init-dired.el
- [X] T018 [P] Criar modulo futuro inativo em src/emacs_a11y/resources/a11y-emacs/lisp/init-accessibility.el
- [X] T019 Garantir empacotamento de resources em pyproject.toml
- [X] T020 Criar stub unitario de modelos de install em tests/unit/test_install_models.py
- [X] T021 [P] Criar stub unitario de preflight em tests/unit/test_install_preflight.py
- [X] T022 [P] Criar stub unitario de templates em tests/unit/test_install_templates.py
- [X] T023 [P] Criar stub de integracao para install direto em tests/integration/test_install_minimal_cli.py
- [X] T024 [P] Criar stub de integracao para install interativo em tests/integration/test_interactive_install_context.py
- [X] T025 [P] Criar stub de contrato de install em tests/contract/test_install_minimal_cli_contract.py

---

## Phase 2: Foundational

**Purpose**: Entregar infraestrutura bloqueante para todas as user stories.

**CRITICAL**: Nenhuma user story inicia antes desta fase.

- [X] T026 Implementar RequiredDependency, PreflightCheck e PreflightResult em src/emacs_a11y/models/install.py
- [X] T027 [P] Implementar InstallProfile, TemplateSource, ProfileTemplate e TemplateValidationResult em src/emacs_a11y/models/install.py
- [X] T028 [P] Implementar InstallRequest, InstallPlanItem, InstallPlan e InstallActionType em src/emacs_a11y/models/install.py
- [X] T029 [P] Implementar InstallExecutionResult, RuntimeValidationResult, RollbackInstruction e ConfirmationPolicy em src/emacs_a11y/models/install.py
- [X] T030 Implementar verificacao de Emacs obrigatoria por perfil em src/emacs_a11y/install/preflight.py
- [X] T031 [P] Integrar reuso de sinais do doctor para deteccao de Emacs em src/emacs_a11y/install/preflight.py
- [X] T032 Implementar gate de preflight no orquestrador antes de template/planner/writer/validator em src/emacs_a11y/install/orchestrator.py
- [X] T033 Implementar branch de aborto critico sem escrita e com exit code 2 em src/emacs_a11y/install/orchestrator.py
- [X] T034 [P] Implementar TemplateLocator com packaged_resource, development_path e frozen_bundle em src/emacs_a11y/install/templates.py
- [X] T035 [P] Implementar validacao estrutural de template minimo em src/emacs_a11y/install/templates.py
- [X] T036 Implementar composicao de init.el minimal sem init-accessibility em src/emacs_a11y/install/profile.py
- [X] T037 [P] Implementar planner somente-leitura para gerar InstallPlan sem escrita em src/emacs_a11y/install/planner.py
- [X] T038 Implementar regras de path safety para restringir escrita ao perfil isolado em src/emacs_a11y/install/writer.py
- [X] T039 [P] Implementar politica de confirmacao e escopo de explicit_yes em src/emacs_a11y/install/orchestrator.py
- [X] T040 [P] Implementar rollback guidance por itens criados e copiados em src/emacs_a11y/install/rollback.py
- [X] T041 [P] Implementar renderer textual para preflight critico, plano, sucesso e falha em src/emacs_a11y/install/renderers/text.py
- [X] T042 Integrar comando install ao roteamento CLI em src/emacs_a11y/cli/__init__.py
- [X] T043 [P] Criar testes unitarios de RequiredDependency e PreflightResult em tests/unit/test_install_models.py
- [X] T044 [P] Criar testes unitarios de preflight bloqueando plano e escrita em tests/unit/test_install_preflight.py
- [X] T045 [P] Criar testes unitarios de locator e template validation em tests/unit/test_install_templates.py
- [X] T046 [P] Criar testes unitarios de planner sem escrita em tests/unit/test_install_planner.py
- [X] T047 [P] Criar testes unitarios de renderer para mensagem CRITICAL e next steps em tests/unit/test_install_render_text.py
- [X] T048 [P] Criar testes de regressao e reuso de sinais do doctor (Emacs, permissoes e estado de perfil) em tests/integration/test_doctor_install_compatibility.py
- [X] T049 Validar checkpoint da fundacao em specs/003-minimal-profile-install/quickstart.md

**Checkpoint**: Fundacao pronta, stories podem iniciar.

---

## Phase 3: User Story 1 - Primeira instalação minimal segura, Priority P1, MVP

**Goal**: Entregar fluxo direto seguro com preflight aprovado, plano, confirmacao e escrita no perfil isolado.

**Independent Test**: Executar install minimal com Emacs presente simulado, confirmar, validar artefatos criados no perfil isolado e resumo final.

### Validation for User Story 1

- [X] T050 [P] [US1] Criar teste de Emacs presente liberando fluxo para template/planner/writer em tests/integration/test_install_minimal_cli.py
- [X] T051 [P] [US1] Criar teste de plano pre-instalacao antes de escrita em tests/integration/test_install_minimal_cli.py
- [X] T052 [P] [US1] Criar teste de cancelamento antes de escrita em tests/integration/test_install_minimal_cli.py
- [X] T053 [P] [US1] Criar teste de escrita apenas no perfil isolado em tests/integration/test_install_minimal_cli.py
- [X] T054 [P] [US1] Criar teste de materializacao de early-init.el, init.el, custom.el e logs em tests/integration/test_install_minimal_cli.py
- [X] T055 [P] [US1] Criar teste de copia de lisp preservando estrutura em tests/integration/test_install_minimal_cli.py
- [X] T056 [P] [US1] Criar teste de conteudo permitido do init.el minimal em tests/unit/test_install_profile.py
- [X] T057 [P] [US1] Criar teste de ausencia de require init-accessibility no init.el em tests/unit/test_install_profile.py
- [X] T058 [P] [US1] Criar teste de resumo final com CREATED, COPIED, SKIPPED, PRESERVED, FAILED, WARNING, CRITICAL e NEXT STEP em tests/contract/test_install_minimal_cli_contract.py

### Implementation for User Story 1

- [X] T059 [US1] Implementar handler do comando install --profile minimal em src/emacs_a11y/cli/install.py
- [X] T060 [US1] Implementar pipeline plan-confirm-write-validate-summary com preflight pass em src/emacs_a11y/install/orchestrator.py
- [X] T061 [US1] Implementar materializacao de arquivos e diretorios do perfil minimal em src/emacs_a11y/install/writer.py
- [X] T062 [US1] Implementar construcao final de init.el minimal com tres requires permitidos em src/emacs_a11y/install/profile.py
- [X] T063 [US1] Implementar validacao de artefatos criados e startup segura do Emacs em src/emacs_a11y/install/validator.py
- [X] T064 [US1] Implementar resumo textual final com rollback guidance em src/emacs_a11y/install/renderers/text.py
- [X] T065 [US1] Atualizar guia de execucao MVP em specs/003-minimal-profile-install/quickstart.md
- [X] T066 [US1] Registrar checkpoint de conclusao do MVP em specs/003-minimal-profile-install/tasks.md

**Checkpoint**: US1 pronta e testavel de forma independente.

---

## Phase 4: User Story 2 - Proteção de configuração pessoal existente, Priority P1

**Goal**: Garantir nao destrutividade de configuracoes pessoais e bloqueio de escrita fora do escopo project-owned.

**Independent Test**: Executar install com caminhos pessoais existentes e comprovar que nao houve alteracoes nesses caminhos.

### Validation for User Story 2

- [X] T067 [P] [US2] Criar teste de deteccao de ~/.emacs sem alteracao em tests/integration/test_install_personal_config_protection.py
- [X] T068 [P] [US2] Criar teste de deteccao de ~/.emacs.d sem alteracao em tests/integration/test_install_personal_config_protection.py
- [X] T069 [P] [US2] Criar teste de deteccao de ~/.config/emacs sem alteracao em tests/integration/test_install_personal_config_protection.py
- [X] T070 [P] [US2] Criar teste de nao alteracao de configuracao pessoal em fluxo com Emacs presente em tests/integration/test_install_personal_config_protection.py
- [X] T071 [P] [US2] Criar teste de bloqueio de escrita fora do diretorio isolado em tests/unit/test_install_path_safety.py
- [X] T072 [P] [US2] Criar teste de aviso explicito de protecao de caminhos pessoais em tests/contract/test_install_minimal_cli_contract.py

### Implementation for User Story 2

- [X] T073 [US2] Implementar deteccao de caminhos pessoais e notices no plano em src/emacs_a11y/install/planner.py
- [X] T074 [US2] Implementar bloqueio de qualquer escrita fora do perfil isolado em src/emacs_a11y/install/writer.py
- [X] T075 [US2] Implementar mensagens textuais de preservacao de configuracao pessoal em src/emacs_a11y/install/renderers/text.py
- [X] T076 [US2] Atualizar contrato de nao destrutividade em specs/003-minimal-profile-install/contracts/install-minimal-cli-contract.md
- [X] T077 [US2] Atualizar documentacao de seguranca do fluxo em docs/install-minimal-profile.md
- [X] T078 [US2] Registrar checkpoint da US2 em specs/003-minimal-profile-install/tasks.md

**Checkpoint**: US2 pronta e testavel de forma independente.

---

## Phase 5: User Story 3 - Instalação via modo interativo contextual, Priority P2

**Goal**: Oferecer fluxo interativo install > minimal equivalente ao modo direto com navegacao acessivel.

**Independent Test**: Rodar modo interativo, entrar em install, executar minimal, confirmar/cancelar e validar help/back/exit.

### Validation for User Story 3

- [X] T079 [P] [US3] Criar teste do contexto interativo install em tests/integration/test_interactive_install_context.py
- [X] T080 [P] [US3] Criar teste da opcao minimal no contexto install em tests/integration/test_interactive_install_context.py
- [X] T081 [P] [US3] Criar teste de exibicao de plano no fluxo interativo com Emacs presente em tests/integration/test_interactive_install_context.py
- [X] T082 [P] [US3] Criar teste de confirmacao e cancelamento por teclado em tests/integration/test_interactive_install_context.py
- [X] T083 [P] [US3] Criar teste de regressao de help, back e exit no prompt contextual em tests/integration/test_interactive_root_cli.py
- [X] T084 [P] [US3] Criar teste de equivalencia funcional entre modo direto e interativo em tests/integration/test_install_direct_interactive_equivalence.py
- [X] T085 [P] [US3] Criar teste de Emacs ausente no modo interativo com abort sem escrita em tests/integration/test_interactive_install_context.py

### Implementation for User Story 3

- [X] T086 [US3] Implementar contexto install no shell interativo em src/emacs_a11y/cli/interactive.py
- [X] T087 [US3] Implementar comando minimal no contexto install em src/emacs_a11y/cli/interactive.py
- [X] T088 [US3] Integrar fluxo interativo ao InstallOrchestrator em src/emacs_a11y/cli/interactive.py
- [X] T089 [US3] Implementar saida CRITICAL e next steps no interativo quando Emacs ausente em src/emacs_a11y/install/renderers/text.py
- [X] T090 [US3] Atualizar diagrama de sequencia interativa em docs/plantuml/install-minimal-sequence-interactive.puml
- [X] T091 [US3] Registrar checkpoint da US3 em specs/003-minimal-profile-install/tasks.md

**Checkpoint**: US3 pronta e testavel de forma independente.

---

## Phase 6: User Story 4 - Execução não interativa segura para automação, Priority P2

**Goal**: Suportar --yes somente no caso seguro e explicito do perfil minimal com preflight aprovado.

**Independent Test**: Rodar install --profile minimal --yes em cenarios validos e invalidos, validando comportamento seguro.

### Validation for User Story 4

- [X] T092 [P] [US4] Criar teste de --yes seguro com perfil minimal explicito em tests/integration/test_install_yes_mode.py
- [X] T093 [P] [US4] Criar teste de recusa de --yes ambiguo em tests/integration/test_install_yes_mode.py
- [X] T094 [P] [US4] Criar teste de --yes com Emacs ausente abortando sem escrita em tests/integration/test_install_yes_mode.py
- [X] T095 [P] [US4] Criar teste de ausencia de arquivos criados quando --yes falha por preflight critico em tests/integration/test_install_yes_mode.py
- [X] T096 [P] [US4] Criar teste de mensagem CRITICAL e sugestao install emacs no --yes, preservando vocabulário canônico de status, em tests/contract/test_install_minimal_cli_contract.py
- [X] T097 [P] [US4] Criar teste de equivalencia de resultado entre confirmacao manual e --yes com preflight pass em tests/integration/test_install_yes_mode.py

### Implementation for User Story 4

- [X] T098 [US4] Implementar validacao de escopo de explicit_yes no orquestrador em src/emacs_a11y/install/orchestrator.py
- [X] T099 [US4] Implementar recusa segura de --yes fora do escopo em src/emacs_a11y/cli/install.py
- [X] T100 [US4] Garantir que --yes nao ignora preflight critico no fluxo de install em src/emacs_a11y/install/orchestrator.py
- [X] T101 [US4] Atualizar contrato de flags e confirmacao para --yes em specs/003-minimal-profile-install/contracts/install-minimal-cli-contract.md
- [X] T102 [US4] Atualizar quickstart para automacao segura com --yes em specs/003-minimal-profile-install/quickstart.md
- [X] T103 [US4] Registrar checkpoint da US4 em specs/003-minimal-profile-install/tasks.md

**Checkpoint**: US4 pronta e testavel de forma independente.

---

## Phase 7: User Story 5 - Perfil existente, ausência de Emacs e permissões, Priority P3

**Goal**: Cobrir cenarios de robustez com abort critico por Emacs ausente, perfil existente e falhas de permissao.

**Independent Test**: Validar perfil existente, Emacs ausente/presente, falha parcial e garantias de nao destrutividade.

### Validation for User Story 5

- [X] T104 [P] [US5] Criar teste de perfil existente sem sobrescrita silenciosa em tests/integration/test_install_existing_profile.py
- [X] T105 [P] [US5] Criar teste de mistura project-owned e desconhecidos no perfil existente em tests/integration/test_install_existing_profile.py
- [X] T106 [P] [US5] Criar teste de Emacs ausente abortando antes de TemplateLocator e Planner em tests/unit/test_install_preflight.py
- [X] T107 [P] [US5] Criar teste de Emacs ausente sem criar diretorio de perfil em tests/integration/test_install_preflight_abort.py
- [X] T108 [P] [US5] Criar teste de Emacs ausente sem criar early-init.el em tests/integration/test_install_preflight_abort.py
- [X] T109 [P] [US5] Criar teste de Emacs ausente sem criar init.el em tests/integration/test_install_preflight_abort.py
- [X] T110 [P] [US5] Criar teste de Emacs ausente sem criar custom.el em tests/integration/test_install_preflight_abort.py
- [X] T111 [P] [US5] Criar teste de Emacs ausente sem criar logs em tests/integration/test_install_preflight_abort.py
- [X] T112 [P] [US5] Criar teste de Emacs ausente sem modificar ~/.emacs, ~/.emacs.d e ~/.config/emacs em tests/integration/test_install_preflight_abort.py
- [X] T113 [P] [US5] Criar teste de Emacs ausente sem executar winget, brew, apt, dnf e pacman em tests/unit/test_install_preflight.py
- [X] T114 [P] [US5] Criar teste de Emacs ausente sem download, sem alterar PATH e sem pedir privilegio admin em tests/unit/test_install_preflight.py
- [X] T115 [P] [US5] Criar teste de mensagem CRITICAL com sugestao install emacs e recomendacao doctor plus retry minimal em tests/contract/test_install_minimal_cli_contract.py
- [X] T116 [P] [US5] Criar teste de runtime validation com Emacs presente simulado em tests/integration/test_install_runtime_validation.py
- [X] T117 [P] [US5] Criar teste de falha parcial por permissao com resumo de itens criados em tests/integration/test_install_partial_failure.py
- [X] T118 [P] [US5] Criar teste de rollback guidance apos falha parcial em tests/integration/test_install_partial_failure.py
- [X] T119 [P] [US5] Criar teste de ausencia de dependencia de emacspeak-setup.el, dtk-* e emacspeak-* em tests/unit/test_install_no_emacspeak_dependency.py
- [X] T120 [P] [US5] Criar teste de template encontrado, ausente e incompleto em tests/unit/test_install_templates.py

### Implementation for User Story 5

- [X] T121 [US5] Implementar politica de preservacao para perfil existente em src/emacs_a11y/install/planner.py
- [X] T122 [US5] Implementar tratamento de arquivo existente project-owned com confirmacao explicita em src/emacs_a11y/install/writer.py
- [X] T123 [US5] Implementar bloqueio total de escrita no ramo de preflight critico em src/emacs_a11y/install/orchestrator.py
- [X] T124 [US5] Implementar saida CRITICAL com garantias de nao escrita e next steps em src/emacs_a11y/install/renderers/text.py
- [X] T125 [US5] Implementar mapeamento de exit codes 0, 1, 2 e 3 em src/emacs_a11y/install/orchestrator.py
- [X] T126 [US5] Implementar representacao de abort seguro sem itens criados em InstallExecutionResult em src/emacs_a11y/models/install.py
- [X] T127 [US5] Implementar tratamento de permissao negada com falha parcial e rollback guidance em src/emacs_a11y/install/writer.py
- [X] T128 [US5] Atualizar contrato de preflight obrigatorio e exit codes em specs/003-minimal-profile-install/contracts/install-minimal-cli-contract.md
- [X] T129 [US5] Atualizar guia de cenarios de falha em docs/install-minimal-profile.md
- [X] T130 [US5] Registrar checkpoint da US5 em specs/003-minimal-profile-install/tasks.md

**Checkpoint**: US5 pronta e testavel de forma independente.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Fechamento da feature com regressao, docs, diagramas e consistencia cruzada.

- [X] T131 [P] Executar testes unitarios da feature em tests/unit/
- [X] T132 [P] Executar testes de integracao da feature em tests/integration/
- [X] T133 [P] Executar testes de contrato da feature em tests/contract/
- [X] T134 Validar regressao de doctor em tests/integration/test_doctor_text_cli.py
- [X] T135 Validar regressao de doctor --json em tests/integration/test_doctor_json_cli.py
- [X] T136 [P] Validar acessibilidade textual e ausencia de dependencia de cor em tests/contract/test_install_minimal_cli_contract.py
- [X] T137 [P] Validar logs sem dados sensiveis em tests/integration/test_install_logging_safety.py
- [X] T138 [P] Validar que testes escrevem apenas em tmp_path em tests/unit/test_script_boundary.py
- [X] T139 [P] Validar resources com importlib.resources em tests/unit/test_install_resource_packaging.py
- [X] T140 Atualizar documentacao operacional final em docs/install-minimal-profile.md
- [X] T141 [P] Atualizar orientacao de doctor como gate antes de install em docs/doctor-cli.md
- [X] T142 [P] Atualizar contrato final da feature em specs/003-minimal-profile-install/contracts/install-minimal-cli-contract.md
- [X] T143 [P] Atualizar quickstart final em specs/003-minimal-profile-install/quickstart.md
- [X] T144 [P] Atualizar diagrama de casos de uso em docs/plantuml/install-minimal-use-cases.puml
- [X] T145 [P] Atualizar diagrama de sequencia direta em docs/plantuml/install-minimal-sequence-direct.puml
- [X] T146 [P] Atualizar diagrama de sequencia interativa em docs/plantuml/install-minimal-sequence-interactive.puml
- [X] T147 [P] Atualizar diagrama de arquitetura em docs/plantuml/install-minimal-architecture.puml
- [X] T148 [P] Atualizar diagrama de fluxo funcional em docs/plantuml/install-minimal-functional-flow.puml
- [X] T149 Revisar consistencia entre spec, plan, research, data-model, contrato, quickstart e docs em specs/003-minimal-profile-install/spec.md
- [X] T150 Marcar checklist final da feature em specs/003-minimal-profile-install/checklists/requirements.md

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1: sem dependencias
- Phase 2: depende da conclusao da Phase 1 e bloqueia todas as stories
- Phase 3 ate Phase 7: dependem da conclusao da Phase 2
- Phase 8: depende da conclusao das stories selecionadas para release

### User Story Dependencies

- US1: inicia apos Foundational e define o MVP
- US2: inicia apos Foundational e depende de base de path safety
- US3: inicia apos Foundational e integra com pipeline da US1
- US4: inicia apos Foundational e depende da politica de confirmacao
- US5: inicia apos Foundational e cobre robustez, preflight critico e permissoes

### Critical Ordering Notes

- T030 ate T033 devem concluir antes de qualquer tarefa de US1-US5
- T036 deve concluir antes de T056 e T062
- T123 e T124 devem concluir antes de T131-T133
- T125 deve concluir antes de T142 e de validacoes finais de contrato

---

## Parallel Opportunities

- Setup: T003-T011, T014-T018, T021-T025
- Foundational: T027-T029, T031, T034-T048
- US1 validacao: T050-T058
- US2 validacao: T067-T072
- US3 validacao: T079-T085
- US4 validacao: T092-T097
- US5 validacao: T104-T120
- Polish: T131-T148

---

## Parallel Example: User Story 1

- T050 em tests/integration/test_install_minimal_cli.py
- T056 em tests/unit/test_install_profile.py
- T058 em tests/contract/test_install_minimal_cli_contract.py

## Parallel Example: User Story 5

- T106 em tests/unit/test_install_preflight.py
- T107 em tests/integration/test_install_preflight_abort.py
- T115 em tests/contract/test_install_minimal_cli_contract.py

---

## Implementation Strategy

### MVP First

1. Concluir Phase 1
2. Concluir Phase 2
3. Entregar Phase 3 (US1)
4. Validar independentemente US1
5. Publicar demonstracao MVP

### Incremental Delivery

1. Entregar US1
2. Entregar US2
3. Entregar US3
4. Entregar US4
5. Entregar US5
6. Finalizar em Phase 8

### Definition of Done Operacional

- Preflight de Emacs obrigatorio e explicito
- Emacs ausente aborta antes de qualquer escrita
- init.el minimal com somente init-packages, init-core e init-dired
- init-accessibility permanece inativo no perfil minimal
- Compatibilidade sem regressao com doctor e doctor --json
- Cobertura de contrato, integracao e unidade alinhada ao quickstart
