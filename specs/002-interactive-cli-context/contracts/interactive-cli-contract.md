# Contract: Interactive Contextual CLI

## 1. Objective

Definir o contrato comportamental do modo interativo contextual da CLI, preservando compatibilidade do modo direto não interativo.

## 2. Entry Points

### 2.1 Interactive Mode
- Trigger: execução de `emacs-a11y` sem subcomando.
- Expected behavior:
  - Inicia sessão interativa no contexto raiz.
  - Exibe prompt `emacs-a11y>`.
  - Exibe ajuda contextual inicial automaticamente.

### 2.2 Direct Non-Interactive Mode
- `emacs-a11y doctor` -> executa diagnóstico textual e encerra.
- `emacs-a11y doctor --json` -> executa diagnóstico JSON e encerra.

## 3. Context Tree (Initial Scope)

- `root` (`emacs-a11y>`)
  - comandos globais: `help`, `back`, `exit`
  - comandos locais: `doctor`
- `doctor` (`emacs-a11y doctor>`)
  - comandos globais: `help`, `back`, `exit`
  - comandos locais: `run`, `json`, `explain`

Observação: contextos `install`, `update` e `remove` permanecem apenas previstos para expansão futura.

## 4. Global Commands

### 4.1 help
- Sem argumentos.
- Exibe ajuda do contexto atual.
- Formato linear: uma linha por comando, `comando - descrição`.

### 4.2 back
- Sem argumentos.
- Em contexto filho: retorna ao pai.
- Em contexto raiz: encerra sessão interativa.

### 4.3 exit
- Sem argumentos.
- Encerra imediatamente a sessão interativa.

## 5. Doctor Context Commands

### 5.1 run
- Executa diagnóstico textual com mesmas regras do caminho direto.

### 5.2 json
- Executa diagnóstico JSON com mesmas regras do caminho direto.

### 5.3 explain
- Exibe explicações curtas dos checks de diagnóstico, em texto linear.

## 6. Invalid Command Handling

Para comando inválido no contexto atual:
- Mensagem obrigatória: identificação do comando inválido e contexto.
- Sugestão obrigatória: instrução para `help`.
- Sugestões recomendadas: até 3 comandos válidos por similaridade e disponibilidade contextual.
- Sessão MUST permanecer ativa, salvo `EOF`/`exit`.

## 7. Accessibility Requirements

- Navegação totalmente por teclado.
- Saída textual linear, sem dependência de cor.
- Mensagens curtas, previsíveis e orientadas à ação.
- Prompt contextual explícito antes da leitura de comando.

## 8. Exit Semantics

- Encerramento por `exit`: término imediato da sessão.
- Encerramento por `back` no raiz: término limpo da sessão.
- Encerramento por EOF/KeyboardInterrupt: término limpo com mensagem curta.

## 9. Compatibility Guarantees

- Contratos existentes de `doctor` textual e JSON MUST ser preservados.
- A adição do modo interativo MUST NOT alterar formato/semântica do JSON atual.
- O modo interativo MUST NOT introduzir efeitos colaterais destrutivos no escopo do `doctor`.
