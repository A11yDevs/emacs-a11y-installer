# Emacs Install Assistant

## Visao geral

A feature `emacs-a11y install emacs` planeja um assistente textual, acessivel e
seguro para orientar ou, quando permitido, executar a instalacao do GNU Emacs.

Ela existe para desbloquear o fluxo ja previsto em `emacs-a11y install --profile minimal`, que depende de Emacs como pre-condicao obrigatoria.

## Comandos previstos

### Modo direto
- `emacs-a11y install emacs`
- `emacs-a11y install emacs --dry-run`
- `emacs-a11y install emacs --execute`
- `emacs-a11y install emacs --method auto|winget|brew|apt`

### Modo interativo
- `emacs-a11y>` -> `install`
- `emacs-a11y install>` -> `emacs`

## Comportamento padrao

O modo padrao e guidance-only:

- detecta sistema operacional e arquitetura;
- detecta se o Emacs ja existe;
- detecta caminho e versao quando possivel;
- recomenda um metodo seguro por plataforma;
- nao executa nada automaticamente.

## Recomendacoes por plataforma

### Windows
- Se `winget` estiver disponivel, o metodo recomendado e:

```text
winget install -e --id GNU.Emacs
```

- Se `winget` nao estiver disponivel, a CLI fornece orientacao manual segura.

### macOS
- Se Homebrew estiver disponivel, o metodo recomendado e:

```text
brew install emacs
```

- Se Homebrew nao estiver disponivel, a CLI fornece orientacao manual segura.

### Debian/Ubuntu
- O fluxo recomendado e:

```text
sudo apt update
sudo apt install emacs
```

- A CLI informa que esse fluxo pode exigir privilegios.
- Na primeira versao, esse ramo permanece guidance-only.

### Plataformas nao suportadas para automacao
- O sistema nao tenta adivinhar comandos inseguros.
- A CLI fornece orientacao manual e proximos passos.

## Quando Emacs ja esta instalado

Se o Emacs ja estiver disponivel, a saida planejada deve:

- informar que o Emacs foi encontrado;
- mostrar caminho detectado;
- mostrar versao quando parseavel;
- evitar reinstalacao por padrao;
- recomendar:

```text
emacs-a11y doctor
emacs-a11y install --profile minimal
```

## Dry-run e execucao assistida

### `--dry-run`
- mostra o que seria recomendado ou executado;
- nunca executa o comando externo.

### `--execute`
- so e aceito quando o metodo/plataforma suportam execucao assistida;
- mostra o comando exato antes de qualquer execucao;
- informa impacto esperado e possivel necessidade de privilegios;
- pede confirmacao explicita;
- permite cancelamento seguro.

## Modelo de consentimento

Antes de qualquer execucao, a CLI deve mostrar:

- plataforma detectada;
- arquitetura detectada;
- metodo escolhido;
- comando exato;
- possivel necessidade de privilegios;
- efeito esperado;
- como cancelar.

Sem confirmacao explicita, nada e executado.

## Garantias de seguranca

O assistente:

- nao altera PATH silenciosamente;
- nao modifica `~/.emacs`, `~/.emacs.d` ou `~/.config/emacs`;
- nao cria o perfil `minimal`;
- nao instala Emacspeak;
- nao configura TTS;
- nao quebra `doctor`;
- nao quebra `install --profile minimal`.

## Relacao com outros comandos

- `emacs-a11y doctor`: continua sendo o comando recomendado para verificar o ambiente.
- `emacs-a11y install --profile minimal`: continua sendo o passo seguinte depois que o Emacs estiver disponivel.

## Limitacoes da primeira versao

- execucao assistida inicial focada em metodos sem privilegio elevado mais previsiveis;
- Debian/Ubuntu fica em guidance-only na v1;
- plataformas como Fedora, Arch e outras distros Linux ficam para expansao futura.