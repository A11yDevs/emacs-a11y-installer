# Data Model: Emacs Install Assistant

## 1. EnvironmentDetectionResult

Representa o resultado consolidado de deteccao do ambiente local.

Campos:
- `operating_system`: `windows`, `macos`, `linux`, `unknown`.
- `distribution`: `debian`, `ubuntu`, `other_linux`, `unknown`.
- `architecture`: `x64`, `arm64`, `x86`, `unknown`.
- `is_tty`: indica se a sessao permite confirmacao interativa segura.
- `path_entries_visible`: opcional, usado apenas para diagnostico resumido.
- `warnings`: avisos relevantes para renderizacao.

Regras:
- A deteccao de plataforma MUST ocorrer antes de qualquer recomendacao.
- `distribution` so tem valor semantico quando `operating_system = linux`.

## 2. EmacsCandidate

Representa um executavel de Emacs encontrado no ambiente.

Campos:
- `path`: caminho detectado.
- `source`: origem da descoberta (`which`, `where`, `doctor_adapter`, etc.).
- `priority`: criterio usado para priorizacao.

Regras:
- O sistema MAY detectar multiplos candidatos.
- A priorizacao MUST ser deterministica e reportavel em aviso quando houver mais de um candidato.

## 3. EmacsDetectionResult

Representa a disponibilidade atual do Emacs no ambiente.

Campos:
- `status`: `found`, `missing`, `multiple_found`.
- `selected_path`: caminho priorizado, quando existir.
- `candidates`: lista de `EmacsCandidate`.
- `version_text`: texto bruto de versao, quando disponivel.
- `warnings`: avisos textuais.

Regras:
- `missing` bloqueia o ramo "Emacs ja instalado" e encaminha para recomendacao de metodo.
- `multiple_found` MUST gerar aviso explicito antes de qualquer proximo passo.

## 4. VersionSupportAssessment

Classificacao da versao detectada do Emacs contra a politica minima do projeto.

Campos:
- `state`: `supported`, `unknown`, `too_old`.
- `detected_version`: string normalizada ou `None`.
- `minimum_supported_version`: string configurada pelos mantenedores.
- `message`: resumo textual da avaliacao.

Regras:
- `unknown` MUST gerar `WARNING`, mas nao pode forcar reinstalacao automatica.
- `too_old` MUST recomendar atualizacao/reinstalacao, ainda sujeita a consentimento explicito.

## 5. PackageManager

Enum para gerenciadores de pacote conhecidos.

Valores:
- `WINGET`
- `BREW`
- `APT`
- `NONE`
- `UNSUPPORTED`

## 6. InstallMethod

Enum do metodo recomendado ou selecionado.

Valores:
- `WINGET_GNU_EMACS`
- `HOMEBREW_FORMULA`
- `APT_GUIDANCE`
- `MANUAL_GUIDANCE`

Regras:
- Um `InstallMethod` sempre pertence a exatamente uma plataforma/estrategia.

## 7. InstallExecutionMode

Enum do modo operacional do comando.

Valores:
- `GUIDANCE_ONLY`
- `DRY_RUN`
- `ASSISTED_EXECUTION`

Regras:
- O modo padrao MUST ser `GUIDANCE_ONLY`.

## 8. InstallCommand

Representa um comando externo documentado e potencialmente executavel.

Campos:
- `argv`: lista de argumentos.
- `display_text`: forma textual a exibir ao usuario.
- `requires_privilege`: booleano.
- `supported_for_assisted_execution`: booleano.
- `expected_effect`: descricao textual do que deve mudar.

Regras:
- O comando exibido ao usuario MUST ser exatamente o comando que seria executado.
- `supported_for_assisted_execution = false` implica guidance-only.

## 9. InstallationMethodRecommendation

Representa a recomendacao consolidada para o ambiente atual.

Campos:
- `method`: `InstallMethod`.
- `package_manager`: `PackageManager`.
- `recommended_commands`: lista ordenada de `InstallCommand`.
- `manual_steps`: passos textuais quando nao houver execucao assistida.
- `assisted_execution_supported`: booleano.
- `rationale`: justificativa resumida para a escolha.

Regras:
- Plataformas desconhecidas MUST cair em `MANUAL_GUIDANCE`.
- Debian/Ubuntu na v1 MUST ter `assisted_execution_supported = false`.

## 10. ExecutionConsentSummary

Resumo textual apresentado imediatamente antes da confirmacao.

Campos:
- `platform_line`: plataforma e arquitetura detectadas.
- `method_line`: metodo escolhido.
- `command_lines`: comandos exatos.
- `privilege_line`: aviso de privilegio quando aplicavel.
- `effect_line`: impacto esperado.
- `cancel_line`: como cancelar.

Regras:
- So existe quando a pessoa solicitou execucao assistida e o metodo suporta esse ramo.

## 11. ConsentDecision

Enum da decisao de confirmacao.

Valores:
- `CONFIRMED`
- `DECLINED`
- `UNAVAILABLE_NO_TTY`

## 12. InstallationAttemptResult

Resultado consolidado do fluxo de `install emacs`.

Campos:
- `status`: `success`, `cancelled`, `guidance_only`, `unsupported`, `failed`, `internal_error`.
- `environment`: `EnvironmentDetectionResult`.
- `emacs_detection_before`: `EmacsDetectionResult`.
- `version_assessment`: `VersionSupportAssessment`.
- `recommendation`: `InstallationMethodRecommendation`.
- `consent_decision`: `ConsentDecision` opcional.
- `executed_commands`: lista de comandos efetivamente executados.
- `emacs_detection_after`: `EmacsDetectionResult` opcional.
- `next_steps`: lista de proximos passos acionaveis.
- `exit_code`: inteiro final.

Regras:
- `guidance_only` e `cancelled` usam exit code `1`.
- `unsupported` usa exit code `2`.
- `failed` usa exit code `3`.
- `internal_error` usa exit code `4`.

## 13. InteractiveInstallContextState

Estado leve do fluxo interativo no contexto `install`.

Campos:
- `pending_emacs_recommendation`: recomendacao atual, se houver.
- `pending_consent_summary`: resumo de consentimento, se o usuario entrou no ramo de execucao assistida.
- `last_status`: ultimo status textual emitido.

Regras:
- `help`, `back` e `exit` nao dependem desse estado para funcionar.