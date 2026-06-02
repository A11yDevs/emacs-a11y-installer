# Data Model: Minimal Profile Install

## 1. InstallProfile

Representa um perfil instalável suportado pela CLI.

Campos:
- `name`: identificador do perfil (`minimal`).
- `description`: descrição curta do perfil.
- `enabled_modules`: lista ordenada de módulos Lisp ativados.
- `template_policy`: política de materialização a partir do template canônico.

Regras:
- `minimal` MUST ativar somente `init-packages`, `init-core` e `init-dired`.
- `minimal` MUST NOT ativar `init-accessibility` nesta feature.
- Perfis futuros MAY reutilizar a mesma estrutura com outro conjunto de módulos.

## 1.1 RequiredDependency

Dependência obrigatória para execução de um perfil.

Campos:
- `name`: identificador da dependência (`emacs`).
- `required_for_profiles`: perfis impactados.
- `status`: `available` ou `missing`.
- `severity`: `critical` para bloqueio de fluxo.

Regras:
- Para `minimal`, `emacs` MUST ser `RequiredDependency` obrigatória.

## 2. TemplateSource

Origem de resolução do template canônico.

Campos:
- `kind`: `packaged_resource`, `development_path`, `frozen_bundle`.
- `location`: caminho resolvido.
- `is_read_only`: indica se a origem é somente leitura.
- `priority`: ordem de fallback.

Regras:
- O instalador MUST resolver uma única fonte canônica válida por execução.
- A resolução MUST NOT clonar nem baixar repositórios remotos.

## 3. ProfileTemplate

Estrutura validada do template de perfil.

Campos:
- `root_path`: diretório raiz do template.
- `early_init_path`: caminho de `early-init.el`.
- `init_path`: caminho do `init.el` base.
- `lisp_root`: diretório `lisp/`.
- `available_modules`: módulos detectados em `lisp/`.
- `optional_modules`: módulos presentes, mas inativos no perfil.

Regras:
- `early-init.el`, `init.el` e `lisp/` MUST existir.
- `init-packages.el`, `init-core.el` e `init-dired.el` MUST existir para o perfil `minimal`.
- `init-accessibility.el` MAY existir, mas MUST ser tratado como módulo futuro/inativo no perfil `minimal`.

## 4. TemplateValidationResult

Resultado da validação da origem e da estrutura do template.

Campos:
- `status`: `valid`, `invalid`, `incomplete`.
- `message_lines`: mensagens lineares de validação.
- `missing_items`: itens ausentes.
- `warnings`: avisos não bloqueantes.

## 5. InstallRequest

Entrada normalizada da execução.

Campos:
- `profile_name`: perfil solicitado.
- `mode`: `direct` ou `interactive`.
- `confirmation_policy`: `interactive_confirm`, `direct_confirm`, `explicit_yes`.
- `target_directory`: diretório isolado resolvido.
- `allow_project_owned_overwrite`: booleano.

## 5.1 PreflightCheck

Entrada de validação pré-escrita.

Campos:
- `request`: `InstallRequest`.
- `required_dependencies`: lista de `RequiredDependency`.
- `doctor_signals`: sinais reutilizados do `doctor` quando disponíveis.

## 5.2 PreflightResult

Resultado da etapa obrigatória de pré-condições.

Campos:
- `status`: `pass` ou `critical_abort`.
- `missing_dependencies`: lista de dependências ausentes.
- `message_lines`: mensagens lineares para renderização.
- `suggested_next_steps`: comandos recomendados.
- `exit_code`: código de saída calculado.

Regras:
- Se `emacs` estiver ausente, `status` MUST ser `critical_abort`.
- Com `critical_abort`, não deve existir plano de escrita.

Regras:
- `explicit_yes` MUST ser aceito apenas para `profile_name = minimal` explicitamente informado.

## 6. InstallPlanItem

Unidade do plano pré-instalação.

Campos:
- `path`: caminho alvo.
- `item_type`: `directory`, `file`, `log_directory`.
- `action_type`: `create`, `copy`, `preserve`, `skip`, `validate`.
- `project_owned`: indica se o item pertence ao projeto.
- `source_path`: origem opcional do template.
- `reason`: justificativa da ação.

## 7. InstallPlan

Plano completo gerado antes da escrita.

Campos:
- `request`: `InstallRequest`.
- `template`: `ProfileTemplate`.
- `items`: lista ordenada de `InstallPlanItem`.
- `personal_config_notices`: caminhos pessoais detectados e protegidos.
- `preflight_messages`: mensagens lineares exibidas antes da confirmação.

Regras:
- O plano MUST listar exatamente o que será criado/copiado/preservado.
- O plano MUST ser renderizável sem escrita no filesystem.
- O plano MUST ser gerado apenas quando `PreflightResult.status = pass`.

## 8. InstallActionType

Enumeração das ações executáveis.

Valores:
- `CREATE_DIRECTORY`
- `COPY_FILE`
- `WRITE_FILE`
- `PRESERVE_EXISTING`
- `SKIP`
- `VALIDATE`

## 9. InstallExecutionResult

Resultado consolidado da execução.

Campos:
- `created_items`: itens criados.
- `copied_items`: itens copiados do template.
- `skipped_items`: itens ignorados.
- `preserved_items`: itens preservados.
- `failed_items`: itens que falharam.
- `runtime_validation`: resultado da validação do Emacs.
- `preflight_result`: resultado da etapa de pré-condições.
- `rollback_guidance`: instruções de rollback.
- `log_paths`: caminhos de log project-owned.
- `exit_code`: código final de execução.

Regras:
- Em aborto por pré-condição ausente, `created_items` MUST ser vazio.
- Em aborto por pré-condição ausente, `copied_items` MUST ser vazio.
- Em aborto por pré-condição ausente, `runtime_validation` não deve executar.

## 10. RuntimeValidationResult

Resultado da tentativa de validação do Emacs com o perfil isolado.

Campos:
- `status`: `validated`, `skipped`, `failed`.
- `message_lines`: mensagens lineares.
- `command_preview`: comando seguro tentado, quando houver.

Regras:
- Runtime validation só ocorre quando preflight obrigatório tiver passado.

## 11. RollbackInstruction

Instruções textuais de reversão manual segura.

Campos:
- `paths_to_remove`: lista ordenada de caminhos project-owned.
- `notes`: observações sobre preservação de arquivos pessoais.
- `future_command_hint`: referência futura para `remove --profile minimal`.

## 12. ConfirmationPolicy

Política de confirmação da execução.

Valores:
- `PROMPT_REQUIRED`
- `INTERACTIVE_SELECTION`
- `EXPLICIT_YES_ALLOWED`
- `DENY_UNSAFE_AUTOMATION`
