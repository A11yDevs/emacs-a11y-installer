# Feature Specification: Doctor CLI Acessível

**Feature Branch**: `[001-doctor-cli]`

**Created**: 2026-06-01

**Status**: Ready for Implementation

**Input**: User description: "Create the first feature of the emacs-a11y-installer: an accessible CLI diagnostic command called `emacs-a11y doctor` that checks the user environment before installation. It should detect the operating system, architecture, Emacs availability and version, Git availability, Python availability, the Emacs Acessível profile directory, existing user Emacs configuration that must not be overwritten, initial TTS or speech infrastructure availability for Windows, macOS and Linux, and possible Emacspeak installation. The command must not modify the system, install dependencies, request administrator privileges, or download binaries. It should produce clear linear terminal output suitable for screen readers, provide concrete next steps for missing dependencies, separate critical problems from warnings and informational items, support optional JSON output with `--json`, and return meaningful exit codes."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Diagnosticar o ambiente antes da instalação (Priority: P1)

Como pessoa usuária do Emacs Acessível, quero executar `emacs-a11y doctor` antes da instalação para entender se meu ambiente está pronto e quais problemas preciso resolver sem que o sistema seja alterado.

**Why this priority**: Esse é o primeiro fluxo útil do projeto e reduz risco antes de qualquer instalação ou configuração.

**Independent Test**: Pode ser testado executando `emacs-a11y doctor` em um ambiente sem preparação prévia e verificando se o comando detecta componentes disponíveis, classifica problemas e não modifica arquivos nem permissões.

**Acceptance Scenarios**:

1. **Given** um ambiente com parte das dependências ausentes, **When** a pessoa executa `emacs-a11y doctor`, **Then** o comando apresenta problemas críticos, avisos e itens informativos em saída textual linear e sugere próximos passos concretos.
2. **Given** um ambiente com Emacs, Git, Python, perfil do Emacs Acessível e infraestrutura inicial de fala disponíveis, **When** a pessoa executa `emacs-a11y doctor`, **Then** o comando informa que o ambiente está pronto para avançar sem alterar o sistema.

---

### User Story 2 - Consumir o diagnóstico em automação e suporte (Priority: P2)

Como mantenedor ou pessoa de suporte, quero obter o mesmo diagnóstico em formato estruturado para integrar o resultado com automação, logs e suporte remoto.

**Why this priority**: O formato estruturado amplia utilidade do comando sem alterar o comportamento principal de terminal acessível.

**Independent Test**: Pode ser testado executando `emacs-a11y doctor --json` e validando se o conteúdo estruturado representa os mesmos achados exibidos na saída padrão.

**Acceptance Scenarios**:

1. **Given** qualquer ambiente suportado, **When** a pessoa executa `emacs-a11y doctor --json`, **Then** o comando retorna um relatório estruturado com checks, severidade, resumo e próximos passos.
2. **Given** um check com falha crítica, **When** a pessoa executa `emacs-a11y doctor --json`, **Then** a saída estruturada identifica a falha e permite determinar o código de saída correspondente.

---

### User Story 3 - Proteger a configuração existente da pessoa usuária (Priority: P3)

Como pessoa usuária com uma configuração pessoal de Emacs já existente, quero que o diagnóstico reconheça diretórios e arquivos relevantes sem sobrescrevê-los nem sugerir ações destrutivas implícitas.

**Why this priority**: O projeto assume instalação não destrutiva e precisa reforçar essa proteção desde o primeiro comando.

**Independent Test**: Pode ser testado em um ambiente com configuração pessoal existente, validando que o comando apenas relata a presença desses arquivos e orienta preservação do conteúdo atual.

**Acceptance Scenarios**:

1. **Given** uma configuração pessoal de Emacs existente, **When** a pessoa executa `emacs-a11y doctor`, **Then** o comando informa a presença dessa configuração e avisa que ela não deve ser sobrescrita.
2. **Given** um diretório de perfil do Emacs Acessível ausente, **When** a pessoa executa `emacs-a11y doctor`, **Then** o comando identifica a ausência como estado diagnóstico e não cria o diretório automaticamente.

### Edge Cases

- O que acontece quando o sistema operacional é identificado, mas a infraestrutura inicial de fala não pode ser determinada com confiança?
- Como o sistema lida com múltiplas instalações de Emacs com versões diferentes no mesmo ambiente?
- Como o sistema apresenta o diagnóstico quando Git ou Python existem no sistema, mas não estão acessíveis no PATH do processo atual?
- O que acontece quando o diretório do perfil do Emacs Acessível existe, mas não é acessível por permissão?
- Como o comando responde quando a configuração pessoal de Emacs existe em caminho não padrão ou em mais de um caminho relevante?
- O que acontece quando a saída JSON é solicitada e um item diagnóstico contém detalhes indisponíveis para a plataforma atual?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST fornecer o comando `emacs-a11y doctor` para executar um diagnóstico de ambiente antes de qualquer instalação.
- **FR-002**: O sistema MUST detectar sistema operacional e arquitetura do ambiente atual.
- **FR-003**: O sistema MUST detectar disponibilidade do Emacs e, quando encontrado, relatar sua versão.
- **FR-004**: O sistema MUST detectar disponibilidade de Git e Python no ambiente atual, tratando ausência de Git como não bloqueante (WARNING) para instalação padrão e ausência de Python como bloqueante (CRITICAL) para a distribuição canônica baseada em pacote Python.
- **FR-005**: O sistema MUST identificar o diretório de perfil do Emacs Acessível e informar se ele existe, está ausente ou não está acessível.
- **FR-006**: O sistema MUST identificar configurações pessoais existentes de Emacs que não devem ser sobrescritas durante futuras instalações.
- **FR-007**: O sistema MUST detectar sinais iniciais de infraestrutura de voz ou TTS relevantes para Windows, macOS e Linux.
- **FR-008**: O sistema MUST detectar indícios de instalação existente do Emacspeak quando identificáveis no ambiente atual.
- **FR-009**: O sistema MUST separar os achados do diagnóstico em problemas críticos, avisos e itens informativos.
- **FR-010**: O sistema MUST apresentar próximos passos concretos para dependências ausentes, configurações incompletas ou problemas detectados.
- **FR-011**: O comando MUST produzir saída textual linear adequada para leitura por tecnologias assistivas.
- **FR-012**: O comando MUST oferecer saída estruturada opcional quando executado com `--json`.
- **FR-013**: O comando MUST retornar códigos de saída significativos que distingam sucesso, avisos e falhas críticas.
- **FR-014**: O comando MUST operar em modo somente leitura, sem modificar arquivos, instalar dependências, solicitar privilégios administrativos ou baixar binários.
- **FR-015**: O sistema MUST manter consistência semântica entre a saída textual e a saída JSON para o mesmo diagnóstico.
- **FR-016**: O comando MUST ser disponibilizado como entrypoint da distribuição canônica em pacote Python multiplataforma, compatível com instalação via `pipx`.
- **FR-017**: Quando houver distribuição em executável autônomo, o comando MUST manter paridade funcional de checks, severidade, próximos passos e códigos de saída em relação ao comando da distribuição canônica.
- **FR-018**: Scripts auxiliares de plataforma MAY iniciar ou automatizar a execução do diagnóstico, mas MUST NOT conter a lógica principal de regras diagnósticas.

### Constitution Alignment *(mandatory)*

- **CA-001 Acessibilidade estrutural**: A saída do comando prioriza ordem linear, texto claro, separação explícita de severidade e leitura íntegra por teclado e leitor de tela.
- **CA-002 CLI primária**: O comportamento essencial é acessível por `emacs-a11y doctor` e por `emacs-a11y doctor --json`, sem depender de interface gráfica.
- **CA-003 Não destrutivo e reversível**: O comando é estritamente diagnóstico e não altera sistema, configurações existentes nem perfis.
- **CA-004 Multiplataforma e adaptadores**: O diagnóstico cobre Windows, macOS e Linux, incluindo sinais específicos de fala/TTS por plataforma.
- **CA-005 Doctor-first**: O recurso existe para orientar a pessoa usuária antes da instalação e antecipa riscos e lacunas do ambiente.
- **CA-006 Segurança e consentimento**: O comando não solicita elevação, não baixa binários e não executa operações sensíveis de escrita.
- **CA-007 Perfis e modularidade**: O diagnóstico reconhece o perfil do Emacs Acessível e diferencia configuração pessoal existente de futura configuração do projeto.
- **CA-008 Observabilidade e suporte remoto**: O resultado do diagnóstico prioriza informação útil para suporte remoto, com preservação de dados sensíveis.
- **CA-009 Distribuição e instalação**: O comportamento especificado cobre a distribuição canônica em pacote Python e define paridade esperada para executáveis autônomos quando publicados.
- **CA-010 Scripts auxiliares**: Scripts de plataforma são tratados como camada de bootstrap/automação, sem deslocar a regra diagnóstica do núcleo Python.
- **CA-011 Documentação operacional**: A feature exigirá ajuda CLI, exemplos de uso e orientação de interpretação dos resultados em todos os canais de distribuição suportados.

### Key Entities *(include if feature involves data)*

- **Check Diagnóstico**: Unidade de verificação individual, com nome, severidade, status, evidência e próximos passos.
- **Relatório de Diagnóstico**: Consolidação do resultado da execução, incluindo resumo, checks, categorias e código de saída.
- **Estado do Ambiente**: Conjunto de informações observadas no sistema atual, como sistema operacional, arquitetura, ferramentas disponíveis, diretórios e sinais de fala.
- **Configuração Pessoal Existente**: Arquivos ou diretórios do Emacs da pessoa usuária que devem ser preservados e apenas reportados.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% das execuções do comando concluem sem modificar arquivos, permissões ou dependências do sistema.
- **SC-002**: Pessoas usuárias conseguem identificar, em uma única execução, se há bloqueios críticos, avisos e itens informativos sem depender de inspeção visual complexa.
- **SC-003**: O relatório textual e o relatório estruturado representam o mesmo conjunto de achados em 100% dos casos validados.
- **SC-004**: Em pelo menos 90% dos ambientes de teste com dependências ausentes, o comando fornece próximos passos específicos o suficiente para orientar a correção sem suporte adicional imediato.
- **SC-005**: O comando distingue com código de saída apropriado os cenários de ambiente pronto, ambiente com avisos e ambiente com bloqueios críticos em 100% dos casos validados.
- **SC-006**: Quando o comando for distribuído em mais de um canal (por exemplo, pacote Python e executável autônomo), os resultados de diagnóstico permanecem funcionalmente equivalentes em 100% dos cenários de validação definidos para a feature.

## Assumptions

- O comando será executado localmente no ambiente da própria pessoa usuária antes de qualquer etapa de instalação.
- A primeira versão cobre detecção inicial de infraestrutura de fala/TTS por plataforma, sem configurar nem instalar componentes de voz.
- Caminhos e sinais de Emacs, Emacspeak e configuração pessoal podem variar por plataforma, mas haverá heurísticas suficientes para produzir orientação útil.
- A saída JSON é destinada a automação, testes e suporte, mas não substitui a saída textual acessível como experiência padrão.
- O comando pode classificar parte das verificações como aviso quando a plataforma não permitir confirmação total de um item sem operações invasivas.
- O pacote Python multiplataforma é o formato canônico da feature, e outros formatos de distribuição são derivados do mesmo código-fonte.

## Scope Notes

- Esta feature cobre o comando `doctor` como etapa doctor-first e inclui conformidade de `--help` para esse comando.
- Os comandos `install`, `update` e `remove` permanecem priorizados no roadmap constitucional e serão tratados em features subsequentes com contratos, tarefas e validações dedicadas.
