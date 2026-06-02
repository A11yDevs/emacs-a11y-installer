# Implementation Plan: Emacs Install Assistant

**Branch**: `004-emacs-install-assistant` | **Date**: 2026-06-01 | **Spec**: `/specs/004-emacs-install-assistant/spec.md`

**Input**: Feature specification from `/specs/004-emacs-install-assistant/spec.md`

## Summary

Implementar um assistente acessivel, seguro e explicito para orientar ou
executar, com consentimento explicito, a instalacao do GNU Emacs por meio de
`emacs-a11y install emacs` e do contexto interativo `install > emacs`. A
arquitetura reutiliza sinais do `doctor` para deteccao de plataforma, Emacs,
PATH e versao quando util, mas separa claramente deteccao de ambiente,
avaliacao de versao, recomendacao de metodo, consentimento, execucao assistida
e renderizacao textual. A primeira versao suporta recomendacao formal para
Windows, macOS e Debian/Ubuntu; a execucao assistida fica habilitada apenas para
metodos sem privilegio elevado na v1, enquanto plataformas ou metodos de maior
risco permanecem em guidance-only seguro.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Typer, pytest, biblioteca padrao (`platform`,
`subprocess`, `shutil`, `pathlib`, `dataclasses`, `enum`, `re`, `typing`),
infraestrutura diagnostica existente do `doctor`

**Storage**: sem armazenamento persistente dedicado; logs textuais de execucao
em formato project-owned quando aplicavel; sem modificacao de configuracao do
Emacs

**Testing**: pytest com `monkeypatch`, `tmp_path`, mocks de `subprocess`, mocks
de PATH e fixtures de deteccao de plataforma/Emacs

**Target Platform**: Windows, macOS, Debian/Ubuntu Linux na v1; guidance-only
seguro para outros ambientes

**Project Type**: pacote Python multiplataforma com CLI acessivel e modo
interativo contextual

**Performance Goals**: deteccao e recomendacao em tempo interativo local;
operacoes sem rede no modo guidance/dry-run; pos-deteccao apos comando externo
limitada a nova verificacao do executavel do Emacs

**Constraints**: nao alterar PATH; nao modificar configuracao pessoal de Emacs;
nao instalar Emacspeak/TTS; nao criar perfil `minimal`; nao executar comando de
instalacao sem mostrar o comando exato e obter confirmacao; sessao sem TTY nao
deve executar instalacao assistida; `--yes` fica fora do escopo da v1 para esta
feature

**Scale/Scope**: um comando novo, extensao do contexto interativo `install`, um
subdominio novo em `install/` para Emacs assistant, cerca de 30+ testes entre
unitarios, integracao e contrato

## Constitution Check (Pre-Design Gate)

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Acessibilidade estrutural**: PASS. O plano exige prompts, comandos,
  resumos e falhas em saida textual linear com marcadores canonicos.
- **CLI primaria**: PASS. O comportamento fica coberto em modo direto e no
  contexto interativo `install`.
- **Instalacao nao destrutiva**: PASS. A feature nao modifica perfil ou
  configuracao pessoal do Emacs e exige consentimento explicito antes de
  qualquer execucao assistida.
- **Multiplataforma nativa**: PASS. A estrategia separa deteccao de ambiente,
  recomendacao por plataforma e adaptadores de execucao externos.
- **Doctor-first**: PASS. A feature reusa diagnostico de plataforma, Emacs e
  PATH sempre que possivel, sem duplicar regras centrais.
- **Distribuicao canonica**: PASS. O comportamento continua no pacote Python
  canonico e permanece compativel com instalacao via `pipx` e executaveis
  autonomos futuros.
- **Scripts auxiliares**: PASS. Nenhuma regra de negocio fica em `.ps1` ou
  `.sh`; toda a logica permanece em Python.
- **Seguranca e consentimento**: PASS. Operacoes externas so ocorrem apos
  resumo de consentimento e confirmacao explicita; metodos com maior risco
  permanecem guidance-only.
- **Modularidade por perfis**: PASS. O novo assistente trata apenas a obtencao
  do Emacs e preserva o fluxo `install --profile minimal` existente.
- **Documentacao operacional**: PASS. O plano inclui contrato CLI, quickstart,
  doc dedicada e diagramas PlantUML.

## Project Structure

### Documentation (this feature)

```text
specs/004-emacs-install-assistant/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── emacs-install-cli-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── emacs_a11y/
    ├── cli/
    │   ├── doctor.py
    │   ├── install.py
    │   └── interactive.py
    ├── doctor/
    │   └── ...
    ├── install/
    │   ├── orchestrator.py               # existente para perfil minimal
    │   ├── emacs.py                      # novo orquestrador do assistente
    │   ├── emacs_detector.py             # deteccao de ambiente e Emacs
    │   ├── emacs_methods.py              # recomendacao por plataforma
    │   ├── emacs_executor.py             # execucao assistida segura
    │   ├── emacs_version.py              # politica de versao e parser
    │   └── renderers/
    │       ├── text.py                   # existente para perfil minimal
    │       └── emacs_text.py             # novo renderer textual
    └── models/
        ├── interactive_cli.py
        └── emacs_install.py

tests/
├── contract/
│   └── test_emacs_install_cli_contract.py
├── integration/
│   ├── test_install_emacs_cli.py
│   ├── test_install_emacs_interactive.py
│   └── test_install_emacs_regressions.py
└── unit/
    ├── test_emacs_detector.py
    ├── test_emacs_methods.py
    ├── test_emacs_executor.py
    ├── test_emacs_version.py
    └── test_emacs_render_text.py

docs/
├── emacs-install-assistant.md
└── plantuml/
    ├── emacs-install-use-cases.puml
    ├── emacs-install-sequence-guidance.puml
    ├── emacs-install-sequence-assisted.puml
    ├── emacs-install-sequence-interactive.puml
    ├── emacs-install-architecture.puml
    └── emacs-install-functional-flow.puml
```

**Structure Decision**: manter o projeto como um unico pacote Python e adicionar
um subdominio especifico para `install emacs`, evitando acoplamento com o fluxo
de perfil `minimal` e reaproveitando apenas a integracao CLI/interativa e os
sinais diagnosticos comuns.

## Design Strategy

### 1. Arquitetura funcional com OO leve

- Modelos em `models/emacs_install.py` usam `dataclass` para resultados de
  deteccao, recomendacao, consentimento e execucao.
- `Enum` modela categorias discretas: `PackageManager`, `InstallMethod`,
  `InstallExecutionMode`, `ConsentDecision` e `VersionSupportState`.
- Funcoes puras concentram parsing, selecao de metodo e classificacao de versao.
- Adaptadores externos ficam isolados em `emacs_detector.py` e
  `emacs_executor.py`.

### 2. Reuso do doctor sem duplicacao diagnostica

- Introduzir um adaptador de reuso para consumir a mesma logica de deteccao de
  plataforma, Emacs no PATH e versao do Emacs quando ela ja existir no `doctor`.
- Se algum detalhe do `doctor` estiver fortemente acoplado ao modelo de
  diagnostico atual, criar funcoes pequenas de traducao em vez de duplicar a
  regra de negocio.
- O assistente de instalacao continua responsavel apenas por recomendacao,
  consentimento, execucao assistida e pos-deteccao.

### 3. Politica de versao

- Introduzir configuracao central para versao minima suportada do Emacs usando
  a variavel `EMACS_A11Y_MIN_EMACS_VERSION` quando definida e valida, com
  fallback para constante padrao versionada no codigo.
- O resultado de avaliacao de versao deve sempre cair em um dos estados:
  `supported`, `unknown`, `too_old`.
- `supported`: informar caminho, versao e proximos passos.
- `unknown`: emitir `WARNING`, nao reinstalar automaticamente e sugerir
  `doctor` + `install --profile minimal`.
- `too_old`: recomendar atualizacao/reinstalacao, mas manter consentimento
  explicito para qualquer execucao assistida.

### 4. Observabilidade e redaction

- Registrar logs textuais em eventos relevantes: deteccao de ambiente,
  recomendacao de metodo, escolha de modo, tentativa de execucao assistida,
  cancelamento, resultado final e pos-deteccao.
- Aplicar redaction para dados sensiveis antes de gravar/emitir logs.
- Preservar rastreabilidade operacional com foco em suporte remoto sem expor
  credenciais, tokens ou caminhos sensiveis nao necessarios.

### 5. Recomendacao por plataforma

- **Windows**: se `winget` estiver disponivel, recomendar como comando canonico
  `winget install -e --id GNU.Emacs`; se indisponivel, guidance-only manual.
- **macOS**: se Homebrew estiver disponivel, adotar `brew install emacs` como
  comando oficial da v1, porque ha formula oficial ativa e verificavel; a opcao
  `--cask` fica rejeitada nesta fase por nao haver base igual de estabilidade no
  material pesquisado.
- **Debian/Ubuntu**: guidance-only com `sudo apt update` e
  `sudo apt install emacs`, sem execucao assistida na v1 por envolver privilegio
  e prompts externos de dificil padronizacao acessivel.
- **Plataforma desconhecida**: nunca adivinhar comando; guidance-only seguro.

### 6. Modos e flags

- **Padrao**: guidance-only, sem execucao.
- **`--dry-run`**: emite forma normalizada do que seria recomendado ou do que
  seria tentado em modo assistido, sem execucao.
- **`--execute`**: solicita execucao assistida quando o metodo/plataforma forem
  explicitamente suportados.
- **`--method {auto,winget,brew,apt}`**: opcional, com validacao contra a
  plataforma detectada.
- **Decisao**: nao expor `--manual`, porque guidance-only ja eh o padrao; nao
  expor `--yes` na v1, porque isso aumentaria o risco sem ganho suficiente.

### 7. Modelo de consentimento

Antes de qualquer execucao, a renderizacao MUST mostrar:

- plataforma detectada;
- arquitetura detectada;
- metodo escolhido;
- comando exato;
- necessidade potencial de privilegios;
- efeito esperado;
- como cancelar.

O prompt de confirmacao deve ser linear, com resposta conservadora padrao. Em
sessao sem TTY, `--execute` deve falhar com seguranca e retornar codigo de
metodo/plataforma indisponivel.

### 8. Estrategia de execucao externa

- Usar `subprocess.run` com lista de argumentos, `shell=False` e captura
  controlada de `stdout`/`stderr`.
- Resumir a saida externa para o usuario em linguagem acessivel, sem despejar
  ruido excessivo nem dados sensiveis.
- Tratar falha do comando assistido como `FAILED` com exit code `3`.
- Reexecutar deteccao de Emacs apos sucesso do comando assistido.
- Se o comando encerrar com sucesso mas o Emacs ainda nao for detectado,
  orientar a reabrir o shell, verificar PATH ou executar `emacs-a11y doctor`.

### 9. Estrategia interativa

- O contexto `install` passa a listar `emacs`, `profile minimal`, `back`,
  `exit` e `help`.
- O comando `emacs` no contexto chama o mesmo orquestrador do modo direto.
- Quando a plataforma suportar execucao assistida, o shell pergunta se a pessoa
  deseja apenas orientacao ou se deseja prosseguir para confirmacao de execucao.
- `help`, `back` e `exit` permanecem globais e nao podem ser interceptados pelo
  fluxo local.

### 10. Exit codes

- `0`: Emacs ja instalado ou comando assistido concluido com sucesso.
- `1`: guidance-only/dry-run concluido sem execucao ou cancelamento explicito
  (diferenciados por marcador textual no resultado).
- `2`: plataforma/metodo/gerenciador indisponivel para a acao solicitada.
- `3`: comando assistido falhou.
- `4`: erro interno inesperado.

Justificativa: separa final feliz, fluxo informativo sem mudanca, ambiente
incompativel, falha operacional externa e erro interno do programa.

### 11. Reversibilidade e limitacoes

- Quando houver possibilidade de efeito no sistema por execucao assistida,
  documentar estrategia de reversao aplicavel.
- Quando nao houver reversao automatica segura, explicitar limitacoes e passos
  manuais de retorno em documentacao e contrato da CLI.

## Test Plan

- **Unitarios**:
  - deteccao de OS e arquitetura;
  - deteccao de Emacs, caminho e multiplos executaveis;
  - parser e avaliacao de versao;
  - recomendacao de metodos por plataforma;
  - bloqueio de `--execute` em metodos nao suportados;
  - renderizacao textual com marcadores canonicos;
  - composicao do resumo de consentimento;
  - mapeamento de exit codes.
- **Integracao**:
  - Windows com `winget` disponivel;
  - Windows sem `winget`;
  - macOS com Homebrew;
  - macOS sem Homebrew;
  - Debian/Ubuntu guidance-only;
  - plataforma desconhecida guidance-only;
  - Emacs ja instalado com versao adequada/desconhecida/antiga;
  - `--dry-run` e `--execute`;
  - cancelamento seguro;
  - sessao nao interativa;
  - pos-sucesso sem Emacs detectavel;
  - fluxo interativo `install > emacs`.
- **Contrato/Regressao**:
  - `doctor` e `doctor --json` sem regressao;
  - `install --profile minimal` sem regressao;
  - `help`, `back` e `exit` preservados;
  - nenhuma alteracao em `~/.emacs`, `~/.emacs.d`, `~/.config/emacs`;
  - nenhum PATH alterado;
  - nenhum perfil `minimal` criado;
  - nenhum Emacspeak/TTS instalado.

## Documentation and Design Artifacts

Artefatos gerados nesta fase:

- `/specs/004-emacs-install-assistant/research.md`
- `/specs/004-emacs-install-assistant/data-model.md`
- `/specs/004-emacs-install-assistant/contracts/emacs-install-cli-contract.md`
- `/specs/004-emacs-install-assistant/quickstart.md`
- `/docs/emacs-install-assistant.md`
- `/docs/plantuml/emacs-install-use-cases.puml`
- `/docs/plantuml/emacs-install-sequence-guidance.puml`
- `/docs/plantuml/emacs-install-sequence-assisted.puml`
- `/docs/plantuml/emacs-install-sequence-interactive.puml`
- `/docs/plantuml/emacs-install-architecture.puml`
- `/docs/plantuml/emacs-install-functional-flow.puml`

## Constitution Check (Post-Design Re-Check)

- **Acessibilidade estrutural**: PASS. A arquitetura prioriza saida linear,
  prompts conservadores e marcadores textuais canonicos.
- **CLI primaria**: PASS. A feature fica toda coberta por CLI direta e modo
  interativo contextual.
- **Instalacao nao destrutiva**: PASS. Nenhum caminho pessoal do Emacs sera
  modificado; execucao assistida e opcional e controlada.
- **Multiplataforma nativa**: PASS. Windows, macOS e Debian/Ubuntu receberam
  tratamento especifico e plataformas desconhecidas entram em guidance-only.
- **Doctor-first**: PASS. Reuso diagnostico foi planejado por adaptador,
  evitando drift de comportamento.
- **Python como nucleo canonico**: PASS. Toda a logica permanece em Python,
  sem delegacao de regra central a scripts externos.
- **Seguranca, consentimento e reversibilidade**: PASS. Nenhuma execucao sem
  comando exibido e confirmacao; cancelamento e metodos nao suportados falham
  com seguranca.
- **Modularidade**: PASS. O subdominio `install/emacs*` fica separado do fluxo
  `install --profile minimal`.
- **Observabilidade e suporte remoto**: PASS. Dry-run e guidance-only produzem
  saida previsivel para suporte; execucao assistida resume efeitos e falhas.
- **Documentacao operacional**: PASS. Doc dedicada, contrato, quickstart e
  diagramas foram definidos no mesmo change set.
- **Distribuicao em camadas**: PASS. O comportamento continua compativel com
  pacote Python e futuros executaveis autonomos.

## Complexity Tracking

Sem violacoes de constituicao que exijam excecao.
