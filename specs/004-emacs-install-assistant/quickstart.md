# Quickstart: Emacs Install Assistant

## 1. Goal

Validar a futura implementacao do assistente `emacs-a11y install emacs` em modo
direto e interativo, cobrindo guidance-only, dry-run e execucao assistida com
consentimento explicito quando suportada.

## 2. Preconditions

- Python 3.11+ disponivel.
- Projeto instalado localmente ou via `pipx`.
- Ambiente de testes com mocks para plataforma, PATH, Homebrew, winget, apt e
  subprocessos externos.
- Nenhum teste deve depender de instalacao real do Emacs ou de acesso a rede.

## 3. Direct Mode Validation

### 3.1 Windows with winget available
1. Simular Windows x64 sem Emacs.
2. Simular `winget` disponivel.
3. Executar `emacs-a11y install emacs`.
4. Validar recomendacao guidance-only com `COMMAND: winget install -e --id GNU.Emacs`.
5. Validar ausencia de execucao automatica.

### 3.2 macOS with Homebrew available
1. Simular macOS sem Emacs.
2. Simular `brew` disponivel.
3. Executar `emacs-a11y install emacs`.
4. Validar recomendacao `COMMAND: brew install emacs`.
5. Validar ausencia de execucao automatica sem `--execute`.

### 3.3 Debian/Ubuntu guidance-only
1. Simular Debian/Ubuntu sem Emacs.
2. Executar `emacs-a11y install emacs`.
3. Validar exibicao de `sudo apt update` e `sudo apt install emacs`.
4. Validar aviso de privilegio e guidance-only seguro.

### 3.4 Emacs already installed
1. Simular Emacs presente no PATH.
2. Executar `emacs-a11y install emacs`.
3. Validar caminho detectado.
4. Validar versao quando parseavel.
5. Validar proximos passos: `emacs-a11y doctor` e `emacs-a11y install --profile minimal`.

### 3.5 Dry-run
1. Executar `emacs-a11y install emacs --dry-run`.
2. Validar exibicao do metodo e comando recomendado.
3. Validar ausencia total de execucao externa.

### 3.6 Assisted execution
1. Simular plataforma/metodo com suporte assistido.
2. Executar `emacs-a11y install emacs --execute`.
3. Validar resumo de consentimento com comando exato.
4. Cancelar e validar `CANCELLED` sem execucao.
5. Confirmar e validar execucao apenas do comando mostrado.

## 4. Interactive Mode Validation

1. Executar `emacs-a11y`.
2. Entrar em `install`.
3. Validar lista local:
   - `emacs`
   - `profile minimal`
   - `back`
   - `exit`
   - `help`
4. Executar `emacs`.
5. Validar deteccao do ambiente e recomendacao equivalente ao modo direto.
6. Validar cancelamento seguro ou confirmacao quando o ramo assistido existir.

## 5. Safety and Failure Validation

- Windows sem `winget`.
- macOS sem Homebrew.
- Debian/Ubuntu sem `apt` disponivel.
- Plataforma desconhecida.
- Sessao sem TTY com `--execute`.
- Emacs com versao desconhecida.
- Emacs com versao antiga.
- Multiplos executaveis de Emacs encontrados.
- Falha do package manager apos confirmacao.
- Sucesso do package manager sem Emacs detectavel apos a execucao.
- Confirmar que PATH nao foi modificado.
- Confirmar que `~/.emacs`, `~/.emacs.d` e `~/.config/emacs` nao foram alterados.
- Confirmar que nenhum perfil `minimal` foi criado.
- Confirmar que Emacspeak/TTS nao foi instalado nem configurado.

## 6. Automated Test Strategy

- Unitarios: deteccao, parsing de versao, selecao de metodo, renderizacao,
  consentimento, mapeamento de exit code.
- Integracao: fluxos por plataforma, cancelamento, execucao assistida, sessao
  nao interativa, interativo `install > emacs`.
- Contrato: CLI surface, output markers, exit codes, regressao de `doctor` e
  `install --profile minimal`.

## 7. Documentation and Design Updates Required

- `specs/004-emacs-install-assistant/plan.md`
- `specs/004-emacs-install-assistant/research.md`
- `specs/004-emacs-install-assistant/data-model.md`
- `specs/004-emacs-install-assistant/contracts/emacs-install-cli-contract.md`
- `docs/emacs-install-assistant.md`
- `docs/plantuml/emacs-install-use-cases.puml`
- `docs/plantuml/emacs-install-sequence-guidance.puml`
- `docs/plantuml/emacs-install-sequence-assisted.puml`
- `docs/plantuml/emacs-install-sequence-interactive.puml`
- `docs/plantuml/emacs-install-architecture.puml`
- `docs/plantuml/emacs-install-functional-flow.puml`

## 8. Done Criteria

- Guidance-only e o comportamento padrao.
- `--dry-run` nao executa nada.
- `--execute` so executa em metodos formalmente suportados.
- Nenhum comando externo e executado sem confirmacao explicita.
- `doctor`, `doctor --json` e `install --profile minimal` seguem sem regressao.
- Saida textual usa marcadores canonicos e nao depende de cor.
- Exit codes `0`, `1`, `2`, `3` e `4` estao cobertos.