# Feature Specification: Interactive CLI Context Mode

**Feature Branch**: `[002-interactive-cli-context]`

**Created**: 2026-06-01

**Status**: Draft

**Input**: User description: "Ajuste a CLI do emacs-a11y-installer para oferecer um modo interativo acessível, contextual e orientado por comandos, inspirado em CLIs hierárquicas como as de roteadores Cisco. Quando a pessoa usuária executar apenas emacs-a11y, sem subcomando, o programa deve entrar em um prompt contextual interativo emacs-a11y>, exibir automaticamente a ajuda do contexto atual e permitir comandos disponíveis naquele contexto. Em qualquer contexto, os comandos help, back e exit devem estar disponíveis: help mostra a ajuda contextual, back retorna ao contexto anterior ou sai quando estiver no contexto raiz, e exit encerra imediatamente a CLI. O contexto raiz deve listar comandos como doctor - Executa diagnóstico de ambiente em modo estritamente somente leitura. Ao digitar doctor, a CLI deve entrar no contexto emacs-a11y doctor> e exibir a ajuda contextual desse comando, permitindo executar ações específicas do diagnóstico, como rodar o diagnóstico textual, rodar o diagnóstico em JSON, consultar explicações dos checks e voltar ao menu anterior. A interface deve ser totalmente navegável por teclado, ter saída textual linear adequada a leitores de tela, não depender de cor, apresentar comandos e descrições curtas em formato previsível, aceitar comandos inválidos com mensagens claras e sugestões, e preservar a execução direta não interativa já existente, como emacs-a11y doctor e emacs-a11y doctor --json."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Navegar no modo interativo raiz (Priority: P1)

Como pessoa usuária, quero executar apenas `emacs-a11y` e entrar em um prompt interativo acessível para descobrir e executar comandos por contexto sem depender de memória de sintaxe.

**Why this priority**: Esse fluxo é o novo ponto de entrada principal da CLI e determina a usabilidade imediata para pessoas que preferem exploração guiada por teclado.

**Independent Test**: Pode ser testado executando apenas `emacs-a11y`, verificando prompt `emacs-a11y>`, ajuda contextual automática, comandos disponíveis e comportamento correto de `help`, `back` e `exit` no contexto raiz.

**Acceptance Scenarios**:

1. **Given** a CLI instalada e sem argumentos, **When** a pessoa executa `emacs-a11y`, **Then** a CLI entra no contexto `emacs-a11y>`, mostra ajuda contextual inicial e lista comandos do contexto raiz.
2. **Given** o contexto raiz ativo, **When** a pessoa executa `help`, **Then** a CLI mostra ajuda textual linear e previsível, sem depender de cor.
3. **Given** o contexto raiz ativo, **When** a pessoa executa `back`, **Then** a CLI encerra a sessão interativa com saída clara.
4. **Given** qualquer contexto ativo, **When** a pessoa executa `exit`, **Then** a CLI encerra imediatamente.

---

### User Story 2 - Navegar e executar ações no contexto doctor (Priority: P2)

Como pessoa usuária, quero entrar no contexto `doctor` a partir do modo interativo e executar ações do diagnóstico sem sair da navegação contextual.

**Why this priority**: Reaproveita a funcionalidade central doctor-first já existente e a torna mais acessível para uso guiado.

**Independent Test**: Pode ser testado iniciando no prompt raiz, entrando com `doctor`, validando prompt `emacs-a11y doctor>`, executando diagnóstico textual e JSON, consultando explicações de checks e retornando com `back`.

**Acceptance Scenarios**:

1. **Given** o contexto raiz ativo, **When** a pessoa executa `doctor`, **Then** a CLI entra no prompt `emacs-a11y doctor>` e mostra ajuda contextual desse contexto.
2. **Given** o contexto `doctor` ativo, **When** a pessoa executa a ação de diagnóstico textual, **Then** a CLI executa o mesmo diagnóstico textual disponível no modo não interativo.
3. **Given** o contexto `doctor` ativo, **When** a pessoa executa a ação de diagnóstico JSON, **Then** a CLI executa o mesmo diagnóstico JSON e mantém consistência semântica com a saída textual.
4. **Given** o contexto `doctor` ativo, **When** a pessoa executa `back`, **Then** a CLI retorna ao contexto raiz.

---

### User Story 3 - Receber feedback claro para comandos inválidos (Priority: P3)

Como pessoa usuária, quero mensagens claras para comandos inválidos em qualquer contexto, com sugestões de próximos comandos válidos.

**Why this priority**: Erros de digitação e exploração por tentativa são comuns em modo interativo; feedback adequado reduz fricção e aumenta acessibilidade.

**Independent Test**: Pode ser testado enviando comandos inválidos nos contextos raiz e `doctor`, validando mensagem compreensível, ausência de travamento e sugestão de ajuda/comandos válidos.

**Acceptance Scenarios**:

1. **Given** um contexto ativo, **When** a pessoa digita comando inválido, **Then** a CLI retorna mensagem clara em texto linear e sugere `help` e comandos disponíveis no contexto.
2. **Given** uma sequência de comandos válidos e inválidos, **When** a pessoa continua a sessão, **Then** a CLI preserva o contexto correto e permanece responsiva por teclado.

### Edge Cases

- O que acontece quando a pessoa envia linha vazia repetidamente no prompt interativo?
- Como a CLI se comporta quando recebe EOF ou interrupção de teclado durante o modo interativo?
- Como a CLI evita ambiguidade entre comandos globais (`help`, `back`, `exit`) e ações específicas do contexto?
- O que acontece quando a ação interativa de diagnóstico retorna falha crítica ou erro interno?
- Como a CLI mantém consistência entre modo interativo e execução direta de `emacs-a11y doctor` e `emacs-a11y doctor --json`?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST iniciar modo interativo contextual quando `emacs-a11y` for executado sem subcomando.
- **FR-002**: O sistema MUST exibir prompt `emacs-a11y>` no contexto raiz e ajuda contextual automaticamente ao entrar no modo interativo.
- **FR-003**: O sistema MUST disponibilizar `help`, `back` e `exit` em todos os contextos interativos.
- **FR-004**: O comando `help` MUST mostrar ajuda do contexto atual em formato textual linear, previsível e sem dependência de cor.
- **FR-005**: O comando `back` MUST retornar ao contexto anterior; no contexto raiz, MUST encerrar a sessão interativa.
- **FR-006**: O comando `exit` MUST encerrar imediatamente a sessão interativa em qualquer contexto.
- **FR-007**: O contexto raiz MUST listar comandos e descrições curtas, incluindo `doctor - Executa diagnóstico de ambiente em modo estritamente somente leitura`.
- **FR-008**: Ao executar `doctor` no contexto raiz, o sistema MUST entrar no contexto `emacs-a11y doctor>` e mostrar ajuda contextual desse contexto.
- **FR-009**: O contexto `doctor` MUST permitir executar diagnóstico textual e diagnóstico JSON com semântica equivalente ao modo não interativo.
- **FR-010**: O contexto `doctor` MUST oferecer ação para consultar explicações dos checks de diagnóstico.
- **FR-011**: O sistema MUST aceitar comandos inválidos com mensagens claras e sugestões de próximos comandos válidos no contexto atual.
- **FR-012**: O sistema MUST ser totalmente navegável por teclado no modo interativo.
- **FR-013**: O sistema MUST preservar a execução direta não interativa já existente, incluindo `emacs-a11y doctor` e `emacs-a11y doctor --json`.
- **FR-014**: O comportamento diagnóstico em modo interativo MUST manter as garantias de somente leitura já estabelecidas para doctor.

### Constitution Alignment *(mandatory)*

- **CA-001 Acessibilidade estrutural**: O prompt, ajuda e erros do modo interativo serão lineares, com linguagem objetiva e leitura íntegra por leitor de tela.
- **CA-002 CLI primária**: A feature amplia a CLI com modo interativo sem remover os fluxos explícitos por subcomando.
- **CA-003 Não destrutivo e reversível**: O modo interativo não introduz operações destrutivas; ações de diagnóstico permanecem somente leitura.
- **CA-004 Multiplataforma e adaptadores**: O modo contextual deve manter o mesmo comportamento em Windows, macOS e Linux.
- **CA-005 Doctor-first**: O contexto `doctor` continua sendo o caminho de verificação antes de qualquer mudança de estado.
- **CA-006 Segurança e consentimento**: O modo interativo não solicita elevação nem executa downloads/instalações implícitas.
- **CA-007 Perfis e modularidade**: A navegação contextual expõe capacidades sem conflitar com perfil isolado e configuração pessoal.
- **CA-008 Distribuição e instalação**: O comportamento vale para o pacote Python canônico e deve manter paridade em canais derivados quando publicados.
- **CA-009 Scripts auxiliares**: Qualquer wrapper de plataforma permanece sem lógica de contexto/negócio principal.
- **CA-010 Documentação operacional**: A feature exigirá atualização da ajuda CLI, quickstart e exemplos de uso interativo.

### Key Entities *(include if feature involves data)*

- **Contexto Interativo**: Estado atual da sessão de prompt, incluindo nome do contexto, comandos disponíveis e referência ao contexto pai.
- **Comando Contextual**: Unidade de ação disponível em um contexto, com nome, descrição curta e regra de execução.
- **Sessão Interativa**: Ciclo de leitura e execução de comandos até `back` no raiz, `exit`, EOF ou interrupção.
- **Resposta de Ajuda Contextual**: Saída textual linear contendo comandos válidos e descrições curtas do contexto ativo.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Em 100% dos testes de entrada sem argumentos, a CLI entra em `emacs-a11y>` e mostra ajuda contextual inicial.
- **SC-002**: Em 100% dos contextos suportados, `help`, `back` e `exit` funcionam conforme definido sem depender de mouse.
- **SC-003**: Em pelo menos 95% dos testes de usabilidade com comandos inválidos, as pessoas identificam o próximo comando correto usando apenas a mensagem de erro/sugestão.
- **SC-004**: A execução de `doctor` textual e JSON no modo interativo mantém equivalência funcional com o modo não interativo em 100% dos cenários validados.
- **SC-005**: A navegação contextual mantém saída textual linear sem códigos de cor em 100% dos cenários de validação de acessibilidade.

## Assumptions

- O modo interativo será implementado sobre a CLI existente sem alterar o contrato principal dos subcomandos já disponíveis.
- A ajuda contextual será textual e concisa, com foco em comandos do contexto atual.
- O conjunto inicial do contexto `doctor` cobre execução textual, JSON e explicações de checks; novas ações poderão ser acrescentadas em iterações futuras.
- A pessoa usuária pode alternar entre modo interativo e não interativo sem mudanças de configuração.
- As regras de somente leitura do diagnóstico já estabelecidas permanecem vigentes dentro do fluxo interativo.
