# Quickstart: Interactive CLI Context Mode

## 1. Goal

Validar manualmente e por testes automatizados o comportamento do modo interativo contextual, preservando o modo não interativo existente.

## 2. Preconditions

- Python 3.11+ ativo.
- Projeto instalado em modo editável ou via `pipx`.
- Dependências de teste instaladas (`pytest`).

## 3. Manual Validation

### 3.1 Root Interactive Entry
1. Executar: `emacs-a11y`
2. Confirmar:
- prompt `emacs-a11y>`
- ajuda contextual automática
- listagem linear de comandos

### 3.2 Global Commands
1. Em `emacs-a11y>`, executar `help`.
2. Em `emacs-a11y>`, executar `doctor` para entrar no contexto filho.
3. Em `emacs-a11y doctor>`, executar `back` e confirmar retorno ao raiz.
4. Em qualquer contexto, executar `exit` e confirmar encerramento imediato.

### 3.3 Doctor Context
1. Em `emacs-a11y doctor>`, executar `run` e validar diagnóstico textual.
2. Em `emacs-a11y doctor>`, executar `json` e validar diagnóstico JSON.
3. Em `emacs-a11y doctor>`, executar `explain` e validar explicações de checks.

### 3.4 Invalid Commands
1. Em `emacs-a11y>`, executar `doctro` (erro proposital).
2. Confirmar mensagem clara + sugestão para `help` + comandos válidos.

### 3.5 Non-Interactive Compatibility
1. Executar `emacs-a11y doctor` e validar comportamento atual.
2. Executar `emacs-a11y doctor --json` e validar comportamento atual.

## 4. Automated Test Plan

### 4.1 Unit Tests
- resolução de comandos globais e locais por contexto
- transições `PUSH`, `POP`, `EXIT`, `STAY`
- normalização de `CommandResult`
- sugestão para comando inválido

### 4.2 Integration Tests
- sessão interativa com sequência de comandos válidos
- `help`, `back`, `exit` em raiz e `doctor`
- entrada sem argumentos inicia prompt interativo
- validação de continuidade de `doctor` e `doctor --json` em modo direto

### 4.3 Contract Tests
- equivalência semântica entre `doctor run` interativo e `emacs-a11y doctor`
- equivalência semântica entre `doctor json` interativo e `emacs-a11y doctor --json`

## 5. Documentation and Diagram Updates (Required)

Atualizar no mesmo change set da implementação:
- `docs/doctor-cli.md` com seção de modo interativo contextual.
- `docs/plantuml/doctor-sequence-text.puml` com sequência interativa textual.
- `docs/plantuml/doctor-sequence-json.puml` com sequência interativa JSON.
- `docs/plantuml/doctor-architecture.puml` com árvore de contextos e roteador de comandos.
- `docs/plantuml/doctor-functional-flow.puml` com navegação `help/back/exit`.

## 6. Done Criteria

- Entrada sem argumentos abre modo interativo acessível.
- `help`, `back`, `exit` funcionam em todos os contextos.
- Contexto `doctor` executa ações previstas sem quebrar compatibilidade direta.
- Mensagens de erro/sugestão são claras e lineares.
- Documentação operacional e diagramas atualizados.

## 7. Evidência de Regressão

Execução validada com Python 3.11:

- comando: `/opt/local/bin/python3.11 -m pytest -q`
- resultado: `41 passed`

Validações críticas cobertas na suíte:

- entrada sem argumentos no modo interativo;
- ajuda automática no contexto raiz;
- comandos `help`, `back`, `exit` em raiz e `doctor`;
- transição `emacs-a11y>` -> `emacs-a11y doctor>`;
- mensagem de comando inválido com orientação para `help`;
- preservação de `emacs-a11y doctor` e `emacs-a11y doctor --json`.
