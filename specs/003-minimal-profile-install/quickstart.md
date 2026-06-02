# Quickstart: Minimal Profile Install

## 1. Goal

Validar a futura implementação da instalação minimal segura do perfil isolado do Emacs Acessível, em modo direto e interativo, sem tocar configurações pessoais.

## 2. Preconditions

- Python 3.11+ disponível.
- Projeto instalado localmente ou via `pipx`.
- Emacs disponível (pré-condição obrigatória para instalação do perfil `minimal`).
- Ambiente de teste com diretório temporário para perfil isolado.
- Mocks/fixtures para template canônico empacotado ou caminho local de desenvolvimento.

## 3. Direct Mode Validation

### 3.0 Mandatory preflight abort (without Emacs)
1. Simular Emacs ausente.
2. Executar `emacs-a11y install --profile minimal`.
3. Validar saída com `CRITICAL: Emacs não encontrado`.
4. Validar ausência total de escrita (nenhum arquivo/diretório criado no perfil).
5. Validar recomendação de próximos passos: `emacs-a11y install emacs`, `emacs-a11y doctor`, `emacs-a11y install --profile minimal`.

### 3.1 Install plan without write
1. Executar `emacs-a11y install --profile minimal`.
2. Confirmar exibição do plano antes da escrita.
3. Confirmar menção explícita de que configurações pessoais não serão modificadas.

### 3.2 Confirmed write
1. Confirmar a instalação.
2. Validar criação apenas dentro do perfil isolado.
3. Validar presença de `early-init.el`, `init.el`, `custom.el`, `lisp/` e `logs/`.

### 3.3 Safe automation
1. Executar `emacs-a11y install --profile minimal --yes`.
2. Validar ausência de prompt.
3. Validar que a execução é recusada para casos não explícitos.

## 4. Interactive Mode Validation

1. Executar `emacs-a11y`.
2. Entrar em `install`.
3. Executar `minimal`.
4. Revisar plano.
5. Confirmar ou cancelar.
6. Validar suporte contínuo de `help`, `back` e `exit`.

## 5. Safety and Failure Validation

- Perfil alvo já existente.
- Arquivo project-owned já existente no perfil.
- Configurações pessoais detectadas (`~/.emacs`, `~/.emacs.d`, `~/.config/emacs`).
- Template ausente.
- Template incompleto.
- Permissão negada em diretório do perfil.
- Emacs ausente.
- Emacs ausente com `--yes`.
- Emacspeak ausente.
- Ausência de `emacspeak-setup.el`.
- Emacs disponível com validação segura simulada.
- Falha parcial com orientação de limpeza segura.

## 6. Expected Artifacts

No perfil isolado minimal, no mínimo:

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

Opcional na estratégia de cópia da estrutura base:

```text
lisp/init-accessibility.el   # pode existir, mas permanece inativo no minimal
```

## 7. Automated Test Strategy

- Unitários: planner, template locator, init filtering, writer policy, rollback guidance.
- Integração: fluxo direto, fluxo interativo, confirmação/cancelamento, `--yes`.
- Contrato: caminhos seguros, não destrutividade, compatibilidade com doctor.

## 8. Documentation and Design Updates Required

- `docs/install-minimal-profile.md`
- `docs/plantuml/install-minimal-use-cases.puml`
- `docs/plantuml/install-minimal-sequence-direct.puml`
- `docs/plantuml/install-minimal-sequence-interactive.puml`
- `docs/plantuml/install-minimal-architecture.puml`
- `docs/plantuml/install-minimal-functional-flow.puml`
- menção em `docs/doctor-cli.md` de uso do doctor antes da instalação

## 9. Done Criteria

- Com Emacs ausente, instalação aborta antes de qualquer escrita.
- Com Emacs ausente, saída inclui `CRITICAL: Emacs não encontrado` e próximos passos.
- Nenhuma configuração pessoal do Emacs é modificada.
- Escrita ocorre apenas após confirmação ou `--yes` seguro e explícito.
- Apenas diretórios project-owned são criados.
- `init.el` minimal ativa somente `init-packages`, `init-core` e `init-dired`.
- `init.el` minimal não ativa `init-accessibility`.
- O fluxo minimal não exige `emacspeak-setup.el`, `dtk-*` ou `emacspeak-*`.
- `lisp/` é materializado preservando estrutura.
- Resumo final e rollback guidance são sempre exibidos.
- Compatibilidade do doctor permanece inalterada.
