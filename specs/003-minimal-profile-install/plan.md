# Implementation Plan: Minimal Profile Install

**Branch**: `003-next-speckit-spec` | **Date**: 2026-06-01 | **Spec**: `/specs/003-minimal-profile-install/spec.md`

**Input**: Feature specification from `/specs/003-minimal-profile-install/spec.md`

## Summary

Implementar a instalação minimal, segura, acessível e reversível de um perfil
isolado do Emacs Acessível por meio de `emacs-a11y install --profile minimal`,
com equivalência funcional no modo interativo contextual. A solução deve
reutilizar o `doctor` para sinais diagnósticos quando útil, localizar uma fonte
canônica de templates empacotável, montar o plano antes de qualquer escrita,
exigir confirmação explícita e materializar apenas artefatos project-owned no
perfil isolado. Emacs é pré-condição obrigatória: sem Emacs disponível o fluxo
deve abortar com `CRITICAL` antes de qualquer escrita. O perfil `minimal` deve
permanecer inicializável sem Emacspeak/TTS, sem ativar `init-accessibility`
nesta fase.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Typer (CLI), pytest, biblioteca padrão (`pathlib`,
`dataclasses`, `enum`, `shutil`, `tempfile`, `importlib.resources` ou
equivalente), infraestrutura diagnóstica existente do `doctor`

**Storage**: filesystem local apenas em diretório isolado project-owned; logs
somente em local do projeto

**Testing**: pytest com `monkeypatch`, `tmp_path`, mocks de filesystem e
simulação de Emacs

**Target Platform**: Windows, macOS, Linux

**Project Type**: pacote Python multiplataforma (CLI)

**Performance Goals**: geração do plano em tempo interativo local; validações e
escritas limitadas ao perfil isolado, sem downloads ou instalações externas

**Constraints**: não destrutivo; sem alteração de PATH; sem privilégios; sem
download; sem modificação de configuração pessoal; `--yes` somente no caso
explícito `install --profile minimal`; sem dependência de `emacspeak-*`,
`dtk-*` ou `emacspeak-setup.el` no perfil `minimal`; Emacs obrigatório antes de
qualquer plano de escrita; sem `winget`/`brew`/`apt`/`dnf`/`pacman`

**Scale/Scope**: perfil `minimal` apenas nesta fase, com estrutura expansível
para perfis futuros `java`, `python`, `latex`, `ai` e `full`

## Constitution Check (Pre-Design Gate)

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Acessibilidade estrutural**: PASS. O plano exige prompts, confirmações,
  resumos e logs lineares, explícitos e adequados a leitor de tela.
- **CLI primária**: PASS. O comportamento será coberto em modo direto e modo
  interativo contextual.
- **Instalação não destrutiva**: PASS. Toda escrita fica restrita ao perfil
  isolado project-owned, com proteção explícita dos caminhos pessoais.
- **Multiplataforma nativa**: PASS. O diretório alvo e a resolução de templates
  serão sensíveis à plataforma sem espalhar lógica específica pelo sistema.
- **Doctor-first**: PASS. O plano prevê reuso da infraestrutura do `doctor` e
  reforça `doctor` como gate recomendado antes da instalação.
- **Distribuição canônica**: PASS. O mecanismo de templates considera pacote
  Python, ambiente de desenvolvimento e executável futuro.
- **Scripts auxiliares**: PASS. A lógica de instalação permanece no núcleo
  Python; scripts seguem apenas como adaptadores.
- **Segurança e consentimento**: PASS. Confirmação explícita antes da escrita e
  `--yes` estritamente limitado.
- **Modularidade por perfis**: PASS. O modelo de perfil/template prepara a
  expansão futura sem implementar perfis avançados agora.
- **Documentação operacional**: PASS. O plano inclui docs específicas e
  diagramas PlantUML da nova feature.

## Project Structure

### Documentation (this feature)

```text
specs/003-minimal-profile-install/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── install-minimal-cli-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── emacs_a11y/
    ├── cli/
    │   ├── doctor.py
    │   ├── interactive.py
    │   └── install.py
    ├── doctor/
    │   └── ...
    ├── install/
    │   ├── orchestrator.py
    │   ├── preflight.py
    │   ├── planner.py
    │   ├── templates.py
    │   ├── profile.py
    │   ├── writer.py
    │   ├── validator.py
    │   ├── rollback.py
    │   └── renderers/
    │       └── text.py
    ├── models/
    │   ├── diagnostic.py
    │   └── install.py
    └── resources/
        └── a11y-emacs/
            ├── early-init.el
            ├── init.el
            └── lisp/

tests/
├── contract/
├── integration/
└── unit/

docs/
├── doctor-cli.md
├── install-minimal-profile.md
└── plantuml/
    ├── install-minimal-use-cases.puml
    ├── install-minimal-sequence-direct.puml
    ├── install-minimal-sequence-interactive.puml
    ├── install-minimal-architecture.puml
    └── install-minimal-functional-flow.puml
```

**Structure Decision**: manter o projeto single-package Python e adicionar um
subdomínio `install/` dedicado, com recursos empacotados e integração explícita
com a CLI existente e com o shell contextual.

## Design Strategy

### Template System

- Introduzir `TemplateSource`, `ProfileTemplate` e `TemplateLocator` para
  localizar e validar a estrutura canônica de `a11y-emacs`.
- Prioridade de fontes: recurso empacotado do pacote -> caminho de
  desenvolvimento explicitamente configurado -> bundle congelado futuro.
- O instalador não deve clonar, baixar nem depender de rede em runtime.

### Preflight and Required Dependencies

- Introduzir `preflight.py` para verificar pré-condições obrigatórias antes de
  template/planner/writer.
- Emacs é `RequiredDependency` do perfil `minimal`.
- Quando Emacs estiver ausente: retornar `CRITICAL: Emacs não encontrado`,
  abortar com código dedicado e zero escrita em disco.
- O preflight deve sugerir próximo passo futuro: `emacs-a11y install emacs`,
  seguido de `emacs-a11y doctor` e `emacs-a11y install --profile minimal`.
- O fluxo de preflight não instala dependências, não altera `PATH` e não
  solicita privilégios administrativos.

### Minimal Profile Materialization

- O perfil minimal será derivado da estrutura canônica, não gerado do zero.
- `early-init.el` e `lisp/` preservam a referência canônica empacotada.
- `init.el` do perfil minimal será filtrado/construído para carregar somente:
  `init-packages`, `init-core` e `init-dired`.
- `init-accessibility.el` pode ser copiado junto com `lisp/`, mas permanece
  inativo no perfil `minimal`.
- `custom.el` pode ser criado vazio ou com cabeçalho seguro do projeto.
- `logs/` será criado como local project-owned para suporte.

### Write Safety and Confirmation

- Com Emacs ausente, o fluxo aborta antes de montar plano de escrita.
- Com Emacs ausente, não há confirmação de escrita e `--yes` não é aplicado.
- Separar `planner` e `writer`: todo o plano é calculado antes de qualquer
  escrita.
- O plano descreve itens a criar, copiar, preservar, ignorar e validar.
- Sobrescrita silenciosa é proibida; itens project-owned existentes só podem
  ser substituídos mediante confirmação explícita futura suportada pelo fluxo.
- `--yes` só é válido para `install --profile minimal` totalmente explícito.

### Doctor Reuse

- Reusar detecção de Emacs, plataforma, configuração pessoal e permissões a
  partir do `doctor` quando apropriado.
- Não duplicar regras diagnósticas já estabelecidas; o instalador consome
  sinais, mas mantém orquestração própria de plano/escrita/validação.

### Runtime Validation

- Quando `emacs` estiver disponível, realizar validação segura e não invasiva,
  preferencialmente em modo batch/dry-run com perfil isolado e sem exigir
  Emacspeak/TTS.
- Quando `emacs` não estiver disponível, a instalação deve abortar no preflight
  e não alcançar fase de runtime validation.

### Exit Codes Strategy

- `0`: instalação concluída com sucesso.
- `1`: instalação cancelada pela pessoa usuária ou condição não crítica.
- `2`: pré-condição obrigatória ausente (ex.: Emacs não encontrado).
- `3`: erro interno inesperado.

Justificativa: separa claramente aborto seguro por dependência ausente de erros
internos e cancelamento voluntário, mantendo contrato CLI auditável.

### Logging and Rollback

- Logs apenas em `logs/` do perfil isolado ou local project-owned documentado.
- Sem segredos nem dados sensíveis.
- Sempre emitir orientação de rollback manual com lista exata de caminhos
  criados/copiados/preservados/falhos.

## Test Plan

- **Unitários**:
  - preflight de dependências obrigatórias (`RequiredDependency`);
  - aborto crítico quando Emacs ausente, sem acionar writer;
  - localização e validação de templates;
  - filtragem/construção do `init.el` minimal;
  - verificação de ausência de `(require 'init-accessibility)` no `init.el`
    minimal;
  - verificação de ausência de dependência de `dtk-*`, `emacspeak-*` e
    `emacspeak-setup.el`;
  - geração de plano sem escrita;
  - política de confirmação e `--yes`;
  - geração de rollback guidance;
  - detecção de segurança de caminhos project-owned.
- **Integração**:
  - Emacs ausente aborta antes de qualquer escrita;
  - Emacs ausente sugere `emacs-a11y install emacs` e próximos passos;
  - Emacs ausente com `--yes` também aborta sem escrita;
  - Emacs ausente no modo interativo mantém contexto navegável;
  - fluxo direto `install --profile minimal` com confirmação;
  - fluxo direto com `--yes` seguro;
  - fluxo interativo `install -> minimal`;
  - cancelamento limpo sem escrita;
  - falha parcial com resumo e limpeza recomendada.
- **Contrato/Regressão**:
  - Emacs ausente retorna `CRITICAL` e exit code de pré-condição ausente;
  - nenhuma alteração em `~/.emacs`, `~/.emacs.d`, `~/.config/emacs`;
  - inicialização do perfil `minimal` sem Emacspeak instalado;
  - `doctor` textual e JSON continuam sem regressão;
  - equivalência funcional entre modo direto e interativo;
  - compatibilidade com pacote Python e empacotamento futuro.

## Documentation and Design Artifacts

Artefatos gerados nesta fase:

- `/specs/003-minimal-profile-install/research.md`
- `/specs/003-minimal-profile-install/data-model.md`
- `/specs/003-minimal-profile-install/contracts/install-minimal-cli-contract.md`
- `/specs/003-minimal-profile-install/quickstart.md`
- `/docs/install-minimal-profile.md`
- `/docs/plantuml/install-minimal-use-cases.puml`
- `/docs/plantuml/install-minimal-sequence-direct.puml`
- `/docs/plantuml/install-minimal-sequence-interactive.puml`
- `/docs/plantuml/install-minimal-architecture.puml`
- `/docs/plantuml/install-minimal-functional-flow.puml`

## Constitution Check (Post-Design Re-Check)

- **Acessibilidade estrutural**: PASS. Plano, confirmação, resumo e logs foram
  modelados em formato linear e textual explícito.
- **CLI primária**: PASS. Modo direto e contexto `install` foram cobertos.
- **Instalação não destrutiva**: PASS. Escrita restrita a diretório isolado.
- **Multiplataforma nativa**: PASS. Resolução de caminhos e templates prevista
  para Windows/macOS/Linux.
- **Doctor-first**: PASS. Reuso diagnóstico e recomendação de `doctor` antes de
  instalar foram incorporados.
- **Diagnóstico antes da instalação**: PASS. Preflight obrigatório baseado em
  sinais do `doctor` aborta fluxo sem escrita quando Emacs está ausente.
- **Python canônico + distribuição em camadas**: PASS. Templates compatíveis
  com pacote Python, `pipx` e bundle futuro.
- **Scripts como adaptadores**: PASS. Não há lógica de negócio planejada em
  scripts auxiliares.
- **Segurança/consentimento/reversibilidade**: PASS. Confirmação explícita,
  `--yes` restrito e rollback guidance definidos.
- **Modularidade por perfis**: PASS. Modelo preparado para perfis futuros.
- **Observabilidade/documentação operacional**: PASS. Logs project-owned e docs
  dedicadas incluídas.

## Complexity Tracking

Sem violações de constituição que exijam exceção.
