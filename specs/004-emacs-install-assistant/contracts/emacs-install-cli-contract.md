# Contract: Emacs Install Assistant CLI

## 1. Objective

Definir o contrato comportamental para orientar ou executar, de forma segura e
acessivel, a instalacao do GNU Emacs via CLI direta e via contexto interativo.

## 2. Direct CLI Surface

### 2.1 Supported command
- `emacs-a11y install emacs`

### 2.2 Supported flags
- `--dry-run`
- `--execute`
- `--method auto`
- `--method winget`
- `--method brew`
- `--method apt`

### 2.3 Flag rules
- Sem flags, o comando MUST operar em guidance-only.
- `--dry-run` MUST mostrar o que seria recomendado ou tentado sem executar nada.
- `--execute` MUST solicitar execucao assistida apenas quando o metodo/plataforma suportarem esse fluxo.
- `--method` MUST ser validado contra a plataforma detectada.
- `--yes` e `--assume-yes` nao fazem parte do contrato da v1 desta feature.

## 3. Interactive Surface

### 3.1 Root context
- `emacs-a11y>` MUST manter `install` como contexto navegavel.

### 3.2 Install context
- Prompt: `emacs-a11y install>`
- Comandos locais minimos:
  - `emacs - Instala ou orienta a instalacao do GNU Emacs.`
  - `profile minimal - Instala o perfil minimal do Emacs Acessivel.`
  - `back - voltar`
  - `exit - sair`
  - `help - ajuda de comandos`

### 3.3 Interactive behavior
- `emacs` no contexto `install` MUST detectar ambiente e Emacs.
- O fluxo interativo MAY perguntar se a pessoa deseja apenas orientacao ou se deseja execucao assistida quando o metodo permitir.
- `help`, `back` e `exit` MUST continuar funcionando sem regressao.

## 4. Platform and Method Contract

### 4.1 Windows
- Se `winget` estiver disponivel, a recomendacao canonica MUST usar:
  - `winget install -e --id GNU.Emacs`
- Uma forma simplificada sem flags MAY aparecer em texto explicativo, mas o comando exibido para execucao MUST ser o canonico acima.
- Se `winget` nao estiver disponivel, o sistema MUST entrar em orientacao manual segura.

### 4.2 macOS
- Se Homebrew estiver disponivel, a recomendacao canonica MUST usar:
  - `brew install emacs`
- Se Homebrew nao estiver disponivel, o sistema MUST entrar em orientacao manual segura.

### 4.3 Debian/Ubuntu
- O sistema MUST recomendar:
  - `sudo apt update`
  - `sudo apt install emacs`
- O sistema MUST informar potencial necessidade de privilegios.
- Na v1, esse metodo MUST permanecer guidance-only.

### 4.4 Unsupported platform
- O sistema MUST NOT tentar adivinhar um comando de instalacao.
- O sistema MUST fornecer orientacao manual e proximos passos.

## 5. Emacs Detection Contract

- O sistema MUST detectar plataforma e arquitetura antes de qualquer recomendacao.
- O sistema MUST detectar se o Emacs ja esta disponivel.
- Quando disponivel, o sistema MUST informar caminho detectado.
- Quando a versao puder ser obtida, o sistema MUST informa-la em texto linear.
- Quando houver multiplos executaveis encontrados, o sistema MUST emitir `WARNING` com priorizacao clara.

## 6. Version Policy Contract

- A avaliacao da versao MUST retornar exatamente um estado:
  - `supported`
  - `unknown`
  - `too_old`
- `supported`: o sistema informa disponibilidade e recomenda proximos passos.
- `unknown`: o sistema emite `WARNING` e nao reinstala automaticamente.
- `too_old`: o sistema recomenda atualizacao/reinstalacao, ainda sujeita a consentimento explicito.

## 7. Safety Contract

- MUST NOT executar qualquer comando de instalacao sem confirmacao explicita.
- MUST NOT alterar PATH silenciosamente.
- MUST NOT solicitar privilegios administrativos silenciosamente.
- MUST NOT baixar binarios silenciosamente.
- MUST NOT executar instaladores silenciosamente.
- MUST NOT executar `winget`, `brew`, `apt`, `dnf`, `pacman` ou equivalente sem mostrar o comando exato antes.
- MUST NOT instalar Emacspeak.
- MUST NOT configurar TTS.
- MUST NOT criar ou modificar o perfil Emacs Acessivel.
- MUST NOT modificar `~/.emacs`, `~/.emacs.d`, `~/.config/emacs` ou equivalentes.
- MUST NOT quebrar `doctor` nem `install --profile minimal`.

## 8. Consent Contract

Antes de qualquer execucao assistida, a saida MUST mostrar:
- plataforma detectada;
- arquitetura detectada;
- metodo escolhido;
- comando exato;
- indicacao de privilegio potencial;
- efeito esperado;
- como cancelar.

Se a pessoa cancelar:
- o resultado MUST ser `CANCELLED`;
- nenhum comando externo MUST ser executado;
- o exit code MUST ser `1`.

## 9. Output Contract

A saida textual MUST usar marcadores lineares, incluindo quando aplicavel:
- `INFO`
- `WARNING`
- `CRITICAL`
- `COMMAND`
- `CONFIRM`
- `CANCELLED`
- `NEXT STEP`
- `SKIPPED`
- `SUCCESS`
- `FAILED`

## 10. Exit Codes

- `0`: Emacs ja instalado ou comando assistido concluido com sucesso.
- `1`: guidance-only/dry-run concluido sem execucao ou usuario cancelou.
- `2`: plataforma, metodo ou gerenciador necessario indisponivel para a acao solicitada.
- `3`: comando assistido falhou.
- `4`: erro interno inesperado.

## 11. Compatibility Contract

- `emacs-a11y doctor` MUST continuar funcionando sem alteracao funcional.
- `emacs-a11y doctor --json` MUST continuar funcionando sem alteracao funcional.
- `emacs-a11y install --profile minimal` MUST continuar funcionando sem alteracao funcional.
- O contexto interativo raiz e o contexto `install` MUST preservar `help`, `back` e `exit`.