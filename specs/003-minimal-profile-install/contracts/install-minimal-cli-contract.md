# Contract: Install Minimal Profile CLI

## 1. Objective

Definir o contrato comportamental da instalação minimal segura, acessível e não destrutiva do perfil isolado do Emacs Acessível.

## 2. Direct CLI Surface

### 2.1 Supported command
- `emacs-a11y install --profile minimal`

### 2.2 Equivalent shorthand
- `emacs-a11y install minimal` MAY ser suportado se o parser permanecer inequívoco.

### 2.3 Non-interactive explicit mode
- `emacs-a11y install --profile minimal --yes`
- `--yes` MUST ser rejeitado para ações ambíguas ou fora do escopo minimal.

## 3. Interactive Surface

### 3.1 Root context
- `emacs-a11y>` MUST expor `install` como comando de navegação contextual.

### 3.2 Install context
- Prompt: `emacs-a11y install>`
- Comandos globais: `help`, `back`, `exit`
- Comandos locais mínimos: `minimal`, `confirm`, `cancel`

## 4. Safety Contract

- MUST verificar pré-condição obrigatória de Emacs antes de qualquer plano de escrita.
- MUST abortar com `CRITICAL: Emacs não encontrado` quando Emacs estiver ausente.
- MUST garantir zero escrita em disco quando Emacs estiver ausente.
- MUST NOT escrever em caminhos pessoais de Emacs.
- MUST NOT alterar PATH.
- MUST NOT baixar binários.
- MUST NOT instalar dependências.
- MUST NOT instalar, atualizar ou configurar Emacs nesta feature.
- MUST NOT instalar Emacspeak.
- MUST NOT configurar TTS.
- MUST NOT carregar `init-accessibility` no perfil `minimal`.
- MUST NOT exigir `emacspeak-setup.el`.
- MUST NOT executar código dependente de `dtk-*` ou `emacspeak-*` durante a instalação `minimal`.
- MUST NOT executar `winget`, `brew`, `apt`, `dnf`, `pacman` ou equivalente nesta feature.
- MUST NOT solicitar privilégios administrativos.
- MUST NOT clonar ou baixar o repositório canônico durante a instalação.

## 5. Template Contract

O sistema MUST validar a presença de:
- `early-init.el`
- `init.el`
- `lisp/`
- `lisp/init-packages.el`
- `lisp/init-core.el`
- `lisp/init-dired.el`

`lisp/init-accessibility.el` MAY existir no template como módulo futuro e
MUST permanecer inativo no perfil `minimal`.

## 5.1 Minimal Init Activation Contract

No perfil `minimal`, o `init.el` MUST ativar somente:
- `(require 'init-packages)`
- `(require 'init-core)`
- `(require 'init-dired)`

No perfil `minimal`, o `init.el` MUST NOT conter:
- `(require 'init-accessibility)`

## 6. Install Plan Contract

Antes da escrita, o sistema MUST exibir:
- diretório alvo do perfil isolado;
- aviso explícito de que configurações pessoais não serão modificadas;
- lista de itens a criar/copiar/preservar;
- política de confirmação;
- aviso de validação segura do Emacs quando aplicável.

Com Emacs ausente, o sistema MUST:
- não exibir plano de escrita;
- não solicitar confirmação de escrita;
- não aplicar `--yes` para criação de perfil;
- exibir `CRITICAL: Emacs não encontrado` e próximos passos.

## 7. Result Contract

Após execução, o sistema MUST exibir resumo linear com:
- `CREATED`
- `COPIED`
- `SKIPPED`
- `PRESERVED`
- `FAILED`
- `WARNING`
- `CRITICAL`
- `NEXT STEP`

O sistema MUST fornecer instruções de rollback manual em sucesso e falha parcial.
O resumo final MUST informar que recursos de voz por Emacspeak serão ativados
em feature posterior.

No ramo de aborto por ausência de Emacs, a saída MUST sugerir:
- `emacs-a11y install emacs` (comando futuro)
- `emacs-a11y doctor`
- `emacs-a11y install --profile minimal`

## 7.1 Exit Codes

- `0`: sucesso da instalação.
- `1`: cancelamento pelo usuário ou condição não crítica.
- `2`: pré-condição obrigatória ausente (ex.: Emacs não encontrado).
- `3`: erro interno inesperado.

## 8. Compatibility Contract

- `emacs-a11y doctor` MUST continuar funcionando sem alteração.
- `emacs-a11y doctor --json` MUST continuar funcionando sem alteração.
- O modo interativo existente MUST preservar `help`, `back` e `exit` em todos os contextos.
