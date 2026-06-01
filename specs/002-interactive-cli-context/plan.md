# Implementation Plan: Interactive CLI Context Mode

**Branch**: `001-doctor-cli` | **Date**: 2026-06-01 | **Spec**: `/specs/002-interactive-cli-context/spec.md`

**Input**: Feature specification from `/specs/002-interactive-cli-context/spec.md`

## Summary

Planejar a evolução da CLI para modo interativo contextual em árvore
(`emacs-a11y>`, `emacs-a11y doctor>`), com comandos globais (`help`, `back`,
`exit`), reaproveitando regras existentes de diagnóstico e preservando
compatibilidade total com execução direta não interativa (`emacs-a11y doctor`,
`emacs-a11y doctor --json`). A estratégia técnica separa loop interativo,
roteamento contextual e ações de domínio para evitar duplicação de lógica.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Typer (CLI existente), pytest, biblioteca padrão
(`dataclasses`, `enum`, `difflib`, `typing`)

**Storage**: N/A (sessão interativa efêmera, sem persistência obrigatória)

**Testing**: pytest (unitário, integração e contrato de compatibilidade)

**Target Platform**: Windows, macOS, Linux

**Project Type**: pacote Python multiplataforma (CLI)

**Performance Goals**: latência de resposta por comando interativo <100ms para
roteamento e ajuda contextual local; execução de diagnóstico sem regressão
perceptível em relação ao caminho atual

**Constraints**: saída textual linear sem dependência de cor; navegação 100%
por teclado; sem alterações destrutivas no escopo `doctor`; compatibilidade
retroativa dos comandos não interativos

**Scale/Scope**: contexto `root` + `doctor` nesta fase; contextos `install`,
`update` e `remove` apenas modelados para expansão futura

## Constitution Check (Pre-Design Gate)

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Acessibilidade estrutural**: PASS. Plano define prompt explícito por
  contexto, ajuda textual linear e mensagens objetivas para erro/sugestão.
- **CLI primária**: PASS. Entrada sem argumentos vira modo interativo; execução
  direta por argumentos permanece suportada.
- **Instalação não destrutiva**: PASS. Escopo cobre apenas fluxo contextual e
  diagnóstico somente leitura.
- **Multiplataforma nativa**: PASS. Loop e árvore são agnósticos de SO;
  reaproveitam checks multiplataforma já existentes.
- **Doctor-first**: PASS. Contexto `doctor` é caminho central do modo
  interativo e preserva o comportamento atual.
- **Distribuição canônica**: PASS. Mudança permanece no pacote Python canônico,
  sem impacto no modelo de distribuição em camadas.
- **Scripts auxiliares**: PASS. Sem migração de regra de negócio para scripts.
- **Segurança e consentimento**: PASS. Sem novas operações privilegiadas ou
  destrutivas.
- **Modularidade por perfis**: PASS. Estrutura em árvore permite crescimento por
  contexto sem acoplamento forte.
- **Documentação operacional**: PASS. Plano inclui atualização de docs e
  diagramas PlantUML no mesmo ciclo.

## Project Structure

### Documentation (this feature)

```text
specs/002-interactive-cli-context/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── interactive-cli-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── emacs_a11y/
    ├── cli/
    │   └── doctor.py
    ├── doctor/
    │   ├── orchestrator.py
    │   ├── renderers/
    │   └── checks/
    └── models/
        └── diagnostic.py

tests/
├── unit/
├── integration/
└── contract/

docs/
├── doctor-cli.md
└── plantuml/
    ├── doctor-architecture.puml
    ├── doctor-functional-flow.puml
    ├── doctor-sequence-text.puml
    └── doctor-sequence-json.puml
```

**Structure Decision**: manter projeto single-package Python com inclusão de
camada de sessão interativa na CLI e reuso dos serviços de diagnóstico já
existentes.

## Architecture Plan (Interactive Loop)

1. Detectar execução sem subcomando no entrypoint da CLI e iniciar sessão
   interativa contextual.
2. Construir `root` como contexto inicial e exibir ajuda automática.
3. Ler entrada do usuário, normalizar token e resolver comando em duas etapas:
   comandos globais -> comandos locais do contexto.
4. Produzir `CommandResult` com ação de navegação (`STAY`, `PUSH`, `POP`,
   `EXIT`) e mensagens lineares.
5. Atualizar pilha de contexto e renderizar próximo prompt.
6. Encerrar por `exit`, `back` no raiz, EOF ou interrupção, sempre com saída
   curta e previsível.

## Data Model Plan

- `CommandContext`: nó da árvore (nome, prompt, pai, comandos).
- `CommandDefinition`: metadados de comando (nome, descrição, tipo, handler,
  destino contextual quando aplicável).
- `CommandResult`: status, mensagens, sugestões, próximo contexto e código de
  saída quando houver encerramento.
- Navegação por pilha: `PUSH` em `doctor`, `POP` em `back`, `EXIT` em `exit` ou
  `back` no raiz.

Detalhamento completo em `/specs/002-interactive-cli-context/data-model.md`.

## Reuse Strategy (Typer + Existing Domain)

- Extrair/usar funções de aplicação para `doctor` textual e JSON com assinatura
  estável, invocadas tanto por Typer não interativo quanto por comandos do
  contexto `doctor`.
- Evitar duplicação de regra: sessão interativa apenas roteia e renderiza,
  enquanto diagnóstico permanece no domínio já existente.
- Manter contratos de saída e códigos de retorno já definidos para caminho
  direto não interativo.

## Accessibility Strategy

- Prompt explícito por contexto (`emacs-a11y>`, `emacs-a11y doctor>`).
- `help` com formato linear `comando - descrição`, ordem previsível e sem caixas
  visuais dependentes de cor.
- Mensagens de erro claras e curtas, com sugestão de próximos comandos.
- Sem atalhos que exijam mouse; navegação integral por teclado.

## Invalid Command Strategy

- Para comando inválido: mensagem com contexto atual + orientação para `help` +
  até três sugestões por similaridade textual entre comandos válidos.
- Sessão permanece no mesmo contexto após erro de entrada.
- Erros internos de execução são isolados do loop e retornam mensagem segura
  sem quebrar a sessão, quando aplicável.

## Test Plan

- **Unitários**:
  - resolução de comandos globais e locais por contexto;
  - transições da pilha (`PUSH`, `POP`, `EXIT`, `STAY`);
  - formatação de ajuda contextual linear;
  - geração de mensagens/sugestões para inválidos.
- **Integração**:
  - entrada sem argumentos inicia modo interativo;
  - navegação `root` -> `doctor` -> `back` -> `root`;
  - `help`, `back`, `exit` em ambos contextos;
  - EOF/interrupt como encerramento controlado.
- **Compatibilidade/Contrato**:
  - `emacs-a11y doctor` continua diagnóstico textual direto;
  - `emacs-a11y doctor --json` continua JSON direto;
  - equivalência funcional entre comandos diretos e ações interativas
    correspondentes.

## Documentation and Diagram Plan

Atualizar no mesmo change set de implementação:

- `docs/doctor-cli.md`: nova seção do modo interativo contextual e exemplos.
- `docs/plantuml/doctor-sequence-text.puml`: sequência de sessão interativa
  textual.
- `docs/plantuml/doctor-sequence-json.puml`: sequência da ação JSON no contexto
  `doctor`.
- `docs/plantuml/doctor-architecture.puml`: árvore de contextos + roteador.
- `docs/plantuml/doctor-functional-flow.puml`: fluxo de `help/back/exit` e
  transições de contexto.

## Planned Artifacts

- `/specs/002-interactive-cli-context/research.md`
- `/specs/002-interactive-cli-context/data-model.md`
- `/specs/002-interactive-cli-context/contracts/interactive-cli-contract.md`
- `/specs/002-interactive-cli-context/quickstart.md`

## Constitution Check (Post-Design Re-Check)

- **Acessibilidade estrutural**: PASS. Critérios explícitos de prompt/ajuda/
  erro lineares definidos.
- **CLI primária**: PASS. Plano cobre modo interativo e preserva modo direto.
- **Instalação não destrutiva**: PASS. Escopo continua sem operações de escrita.
- **Multiplataforma nativa**: PASS. Arquitetura independente de SO para loop e
  navegação.
- **Doctor-first**: PASS. Contexto `doctor` é componente central do desenho.
- **Distribuição canônica**: PASS. Sem alteração do pacote Python canônico.
- **Scripts auxiliares**: PASS. Nenhuma regra de negócio movida para scripts.
- **Segurança e consentimento**: PASS. Sem novas ações sensíveis.
- **Modularidade por perfis**: PASS. Árvore de contextos extensível por módulo.
- **Documentação operacional**: PASS. Docs e PlantUML incluídos no plano.

## Complexity Tracking

Sem violações de constituição que exijam exceção.
