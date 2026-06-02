# Install Minimal Profile Design Notes

## Visão geral

A feature `emacs-a11y install --profile minimal` planeja a criação segura de um
perfil isolado do Emacs Acessível, sem tocar a configuração pessoal existente do
usuário.

## Comandos previstos

### Modo direto
- `emacs-a11y install --profile minimal`
- `emacs-a11y install --profile minimal --yes`

### Modo interativo
- `emacs-a11y>` -> `install`
- `emacs-a11y install>` -> `minimal`

## Garantias de segurança

- verifica Emacs como pré-condição obrigatória antes de qualquer escrita;
- aborta com `CRITICAL: Emacs não encontrado` quando a pré-condição falha;
- não escreve em `~/.emacs`, `~/.emacs.d`, `~/.config/emacs` ou equivalentes;
- não altera PATH;
- não baixa binários;
- não instala dependências;
- não instala Emacspeak;
- não configura TTS;
- não instala/atualiza/configura Emacs nesta feature;
- não solicita privilégios administrativos;
- não executa `winget`, `brew`, `apt`, `dnf`, `pacman` ou equivalente;
- não clona nem baixa o repositório `emacs-a11y` durante a instalação.

## Fonte canônica de templates

A estrutura de referência do perfil vem do repositório `A11yDevs/emacs-a11y`,
a partir de `packages/emacs-a11y-config/usr/share/a11y-emacs`.

Para distribuição do instalador, essa estrutura deve ser empacotada como recurso
local do projeto, preservando compatibilidade com:

- pacote Python instalado via `pipx`;
- ambiente de desenvolvimento local;
- executável futuro empacotado.

## Estrutura mínima do perfil

```text
/
├── early-init.el
├── init.el
├── custom.el
├── lisp/
│   ├── init-packages.el
│   ├── init-core.el
│   └── init-dired.el
└── logs/
```

Opcional na estratégia de cópia da árvore completa de `lisp/`:

```text
lisp/init-accessibility.el   # módulo futuro, não ativado no perfil minimal
```

## Estratégia do `init.el`

O `init.el` do perfil minimal será baseado na estrutura canônica, mas ativará
somente:

```elisp
(require 'init-packages)
(require 'init-core)
(require 'init-dired)
```

`init-accessibility.el` pode existir em `lisp/` por motivos de empacotamento e
expansão futura, mas não deve ser ativado nessa feature.

## Fluxo operacional esperado

1. Normalizar requisição de instalação.
2. Executar preflight obrigatório de dependências (especialmente Emacs).
3. Se Emacs estiver ausente: abortar com `CRITICAL`, sem escrita e com próximos
   passos (`emacs-a11y install emacs`, `emacs-a11y doctor`,
   `emacs-a11y install --profile minimal`).
4. Se Emacs estiver presente: detectar diretório alvo e proteções pessoais.
5. Localizar e validar template canônico empacotado.
6. Montar plano de instalação sem escrever no disco.
7. Exibir plano em saída textual linear.
8. Solicitar confirmação ou aceitar `--yes` apenas no caso seguro explícito.
9. Materializar o perfil project-owned.
10. Validar arquivos gerados e runtime seguro do Emacs sem exigir Emacspeak/TTS.
11. Exibir resumo final, logs e rollback guidance.

## Rollback manual esperado

Após sucesso ou falha parcial, a CLI deve listar explicitamente os caminhos
project-owned criados e instruir a pessoa usuária a removê-los manualmente,
preparando integração futura com `emacs-a11y remove --profile minimal`.

## Relação com `doctor`

O comando `doctor` continua sendo o diagnóstico prévio recomendado antes da
instalação. A implementação deve reutilizar suas capacidades quando útil para
Emacs, plataforma, permissões e configuração pessoal, sem duplicar lógica.

## Instalação de Emacs (futura)

Nesta feature, `emacs-a11y install --profile minimal` não instala Emacs.
Quando Emacs estiver ausente, o fluxo apenas orienta o comando futuro
`emacs-a11y install emacs` e aborta sem escrita.

## Escopo de voz (futuro)

Nesta feature, o perfil `minimal` é uma base segura e inicializável.
Recursos de acessibilidade por voz via Emacspeak serão ativados em feature
posterior, após instalação e validação específicas.
