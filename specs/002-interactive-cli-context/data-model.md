# Data Model: Interactive CLI Context Mode

## 1. CommandContext

Representa um nó da árvore de navegação da CLI.

Campos:
- `name`: identificador curto do contexto (`root`, `doctor`).
- `prompt_label`: rótulo exibido no prompt (`emacs-a11y`, `emacs-a11y doctor`).
- `description`: resumo textual do propósito do contexto.
- `parent`: referência para contexto pai (nulo no contexto raiz).
- `commands`: coleção de `CommandDefinition` válidos no contexto.
- `default_help_order`: ordem canônica de listagem para `help`.

Regras de validação:
- `prompt_label` MUST ser único por contexto.
- `commands` MUST conter nomes únicos por contexto.
- `parent` de `root` MUST ser nulo.

Relações:
- `CommandContext` 1:N `CommandDefinition`.
- `CommandContext` N:1 `CommandContext` (self-reference via `parent`).

## 2. CommandDefinition

Define um comando executável em um contexto.

Campos:
- `name`: token de entrada (`help`, `doctor`, `json`).
- `description`: descrição curta em formato linear (`nome - descrição`).
- `kind`: tipo (`global`, `navigation`, `action`).
- `handler_id`: identificador da ação de domínio associada.
- `target_context`: contexto de destino para comandos de navegação (opcional).
- `aliases`: sinônimos opcionais.

Regras de validação:
- Comandos globais MUST estar disponíveis em todos os contextos ativos.
- `target_context` MUST existir quando `kind = navigation`.
- `handler_id` MUST existir quando `kind = action`.

## 3. CommandResult

Resultado normalizado da execução de um comando.

Campos:
- `status`: `ok`, `invalid`, `error`, `exit_requested`.
- `message_lines`: linhas de mensagem em ordem de leitura.
- `suggestions`: comandos sugeridos no contexto atual.
- `next_context`: contexto após execução (pode ser o atual).
- `exit_code`: código de saída quando a sessão termina.

Regras de validação:
- `status = invalid` MUST incluir ao menos uma linha explicativa.
- `status = exit_requested` MUST definir `exit_code`.
- `next_context` MUST ser resolvido antes de renderizar novo prompt.

## 4. NavigationAction

Enumeração de transições entre contextos.

Valores:
- `STAY`: permanece no contexto atual.
- `PUSH`: entra em contexto filho.
- `POP`: retorna ao contexto pai.
- `EXIT`: encerra a sessão.

## 5. InteractiveSessionState

Estado em memória durante o loop interativo.

Campos:
- `context_stack`: pilha ordenada de `CommandContext` (topo é contexto atual).
- `running`: flag de ciclo da sessão.
- `history_enabled`: indicação de histórico de comandos (opcional por ambiente).

Regras de transição:
- Entrada sem argumentos inicia com `context_stack = [root]`.
- `doctor` no `root` gera `PUSH` para `doctor`.
- `back` no `doctor` gera `POP` para `root`.
- `back` no `root` gera `EXIT` com encerramento limpo.
- `exit` em qualquer contexto gera `EXIT` imediato.

## 6. DoctorActionCatalog

Catálogo de ações no contexto `doctor` reaproveitando serviços existentes.

Ações:
- `run_text`: executa diagnóstico textual.
- `run_json`: executa diagnóstico JSON.
- `explain_checks`: lista checks, severidades e propósito.

Regra de consistência:
- `run_text` e `run_json` MUST usar as mesmas funções de domínio do modo não interativo.

## 7. Invariantes de Compatibilidade

- `emacs-a11y doctor` MUST permanecer equivalente ao diagnóstico textual atual.
- `emacs-a11y doctor --json` MUST permanecer equivalente ao diagnóstico JSON atual.
- Fluxo interativo MUST ser somente leitura no escopo do `doctor`.
