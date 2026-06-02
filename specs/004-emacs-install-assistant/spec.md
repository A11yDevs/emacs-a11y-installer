# Feature Specification: Emacs Install Assistant

**Feature Branch**: `[004-emacs-install-assistant]`

**Created**: 2026-06-01

**Status**: Ready for Implementation

**Input**: User description: "Create the next feature of the emacs-a11y-installer: 004-emacs-install-assistant."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Recomendar instalação segura do Emacs quando ele estiver ausente (Priority: P1)

Como pessoa usuária sem Emacs instalado, quero executar `emacs-a11y install emacs` para receber orientação clara, acessível e segura sobre como obter GNU Emacs no meu sistema.

**Why this priority**: Sem Emacs, a instalação do perfil `minimal` não pode prosseguir; esta feature desbloqueia o fluxo principal do produto.

**Independent Test**: Executar `emacs-a11y install emacs` em Windows, macOS e Debian/Ubuntu sem Emacs disponível e validar detecção do ambiente, recomendação do método apropriado e próximos passos sem execução automática.

**Acceptance Scenarios**:

1. **Given** Emacs não está disponível em Windows e `winget` está disponível, **When** a pessoa executa `emacs-a11y install emacs`, **Then** o sistema informa que Emacs não foi encontrado, identifica Windows, apresenta `winget install -e --id GNU.Emacs` como comando recomendado e não o executa sem confirmação explícita.
2. **Given** Emacs não está disponível em macOS e Homebrew está disponível, **When** a pessoa executa `emacs-a11y install emacs`, **Then** o sistema identifica macOS, apresenta o comando recomendado de instalação e explica o efeito esperado antes de qualquer execução.
3. **Given** Emacs não está disponível em Debian/Ubuntu, **When** a pessoa executa `emacs-a11y install emacs`, **Then** o sistema recomenda o fluxo com `apt`, informa que pode exigir privilégios e não executa nada automaticamente.
4. **Given** Emacs não está disponível e a plataforma não é suportada para automação, **When** a pessoa executa `emacs-a11y install emacs`, **Then** o sistema informa que a instalação assistida não está disponível para esse ambiente e fornece orientação manual e próximos passos.

---

### User Story 2 - Executar instalação assistida somente com consentimento explícito (Priority: P1)

Como pessoa usuária que deseja ajuda para instalar o Emacs, quero que a ferramenta mostre exatamente o comando antes da execução e só prossiga após minha confirmação explícita.

**Why this priority**: O valor da feature depende de segurança, consentimento e previsibilidade, especialmente em operações que podem envolver gerenciadores de pacotes e privilégios.

**Independent Test**: Executar o comando em ambiente suportado com modo de execução assistida solicitado e validar exibição do comando exato, aviso de privilégios, opção de cancelamento e ausência de execução antes da confirmação.

**Acceptance Scenarios**:

1. **Given** o ambiente suporta execução assistida, **When** a pessoa solicita execução assistida, **Then** o sistema mostra plataforma detectada, método detectado, comando exato, necessidade potencial de privilégios, efeito esperado e como cancelar.
2. **Given** o comando assistido foi apresentado, **When** a pessoa responde negativamente ou cancela, **Then** nenhum comando de instalação é executado e a saída marca o fluxo como `CANCELLED`.
3. **Given** o comando assistido foi apresentado, **When** a pessoa confirma explicitamente, **Then** somente o comando documentado e previamente mostrado pode ser executado.
4. **Given** a plataforma ou o método não é suportado para execução assistida, **When** a pessoa solicita `--execute`, **Then** o sistema falha com segurança, não executa nada e fornece orientação acionável.

---

### User Story 3 - Reconhecer Emacs já instalado e evitar reinstalação desnecessária (Priority: P1)

Como pessoa usuária que já possui Emacs, quero que a ferramenta detecte isso e me diga o que fazer em seguida, sem tentar reinstalar por padrão.

**Why this priority**: Evita ações desnecessárias, preserva confiança e conecta diretamente com os fluxos `doctor` e `install --profile minimal`.

**Independent Test**: Executar `emacs-a11y install emacs` com Emacs já disponível e validar caminho detectado, versão quando possível, ausência de reinstalação por padrão e próximos passos recomendados.

**Acceptance Scenarios**:

1. **Given** Emacs está disponível no ambiente, **When** a pessoa executa `emacs-a11y install emacs`, **Then** o sistema informa que Emacs já está instalado, mostra o caminho detectado e não tenta reinstalar por padrão.
2. **Given** Emacs está disponível e a versão pode ser identificada, **When** o comando é executado, **Then** a versão é apresentada em saída linear e acessível.
3. **Given** Emacs está disponível e a versão não pode ser identificada, **When** o comando é executado, **Then** o sistema emite `WARNING`, não reinstala automaticamente e sugere `emacs-a11y doctor` e `emacs-a11y install --profile minimal`.
4. **Given** Emacs está disponível, **When** o comando é executado, **Then** a saída recomenda como próximo passo `emacs-a11y doctor` e `emacs-a11y install --profile minimal`.

---

### User Story 4 - Usar o assistente pelo modo interativo contextual (Priority: P2)

Como pessoa usuária em fluxo guiado, quero acessar `install > emacs` no modo interativo para receber as mesmas orientações e confirmações do modo direto.

**Why this priority**: Mantém consistência com a CLI acessível já existente e reduz barreira para quem prefere navegação contextual.

**Independent Test**: Iniciar `emacs-a11y`, entrar em `install`, executar `emacs`, revisar recomendação e validar que `help`, `back` e `exit` continuam disponíveis.

**Acceptance Scenarios**:

1. **Given** a pessoa está no contexto `emacs-a11y install>`, **When** executa `emacs`, **Then** o sistema detecta plataforma, disponibilidade do Emacs e apresenta a recomendação correspondente.
2. **Given** a pessoa está no contexto `install`, **When** solicita ajuda, retorno ou saída, **Then** `help`, `back` e `exit` continuam funcionando sem regressão.
3. **Given** o ambiente suporta execução assistida, **When** a pessoa escolhe continuar com execução no modo interativo, **Then** o fluxo de consentimento é textual, linear e equivalente ao modo direto.

---

### User Story 5 - Receber saída previsível em guidance-only ou dry-run para suporte (Priority: P2)

Como mantenedor(a) ou pessoa de suporte, quero usar o fluxo guidance-only padrão ou dry-run previsível para documentar exatamente o que seria recomendado ou executado sem alterar o sistema.

**Why this priority**: Facilita suporte remoto, documentação operacional e diagnóstico sem risco de mudanças acidentais.

**Independent Test**: Executar o comando em guidance-only ou dry-run em plataformas suportadas e validar saída estável com status, método, comando recomendado, privilégios esperados e próximos passos, sem execução.

**Acceptance Scenarios**:

1. **Given** a pessoa usa guidance-only (padrão) ou `--dry-run`, **When** o comando é executado, **Then** a saída mostra o método recomendado e o comando correspondente sem executá-lo.
2. **Given** a plataforma não suporta automação, **When** guidance-only ou dry-run é usado, **Then** o sistema fornece instruções seguras sem tratar isso como erro interno.
3. **Given** o comando é executado em contexto de suporte, **When** o fluxo termina sem execução, **Then** o resultado permanece previsível, linear e adequado para leitura por leitor de tela.

### Edge Cases

- Emacs existe, mas a versão não pode ser interpretada.
- Emacs existe, mas a versão detectada está abaixo da versão mínima suportada definida pelos mantenedores.
- Múltiplos executáveis de Emacs são encontrados no ambiente.
- O gerenciador de pacotes recomendado existe, mas o comando falha após confirmação.
- O gerenciador de pacotes recomendado não está disponível para a plataforma detectada.
- Windows sem `winget`.
- macOS sem Homebrew.
- Debian/Ubuntu sem `apt` disponível.
- Distribuição Linux diferente de Debian/Ubuntu.
- Plataforma desconhecida ou arquitetura não reconhecida.
- O usuário solicita `--execute` em ambiente não suportado.
- O usuário cancela no ponto de confirmação.
- O comando é invocado em sessão não interativa sem modo seguro suportado.
- O comando de instalação conclui, mas Emacs ainda não é detectado em seguida.
- Emacs passa a ficar disponível apenas após reinício do shell ou da sessão.
- A rede está indisponível durante a execução do gerenciador de pacotes.
- O ambiente exige privilégios administrativos para concluir a instalação.
- `emacs-a11y install --profile minimal` já existe e não deve ser afetado pela nova feature.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST fornecer o comando direto `emacs-a11y install emacs`.
- **FR-002**: O sistema MUST fornecer acesso equivalente no modo interativo por `emacs-a11y install> emacs`.
- **FR-003**: O sistema MUST detectar sistema operacional e arquitetura antes de recomendar qualquer método de instalação.
- **FR-004**: O sistema MUST detectar se o executável do Emacs já está disponível no ambiente.
- **FR-005**: O sistema MUST detectar o caminho do executável do Emacs quando ele estiver disponível.
- **FR-006**: O sistema MUST detectar a versão do Emacs quando isso for possível de forma segura.
- **FR-007**: O sistema MUST detectar a disponibilidade do gerenciador de pacotes recomendado para a plataforma suportada.
- **FR-008**: O sistema MUST recomendar um método de instalação apropriado para Windows, macOS e Debian/Ubuntu.
- **FR-009**: O sistema MUST preferir `winget install -e --id GNU.Emacs` em Windows quando `winget` estiver disponível.
- **FR-010**: O sistema MUST fornecer orientação de download manual oficial em Windows quando `winget` não estiver disponível.
- **FR-011**: O sistema MUST preferir `brew install emacs` em macOS quando Homebrew estiver disponível.
- **FR-012**: O sistema MUST fornecer orientação manual em macOS quando Homebrew não estiver disponível.
- **FR-013**: O sistema MUST recomendar o fluxo documentado com `apt` em Debian/Ubuntu e informar explicitamente que ele pode exigir privilégios.
- **FR-014**: O sistema MUST classificar plataformas não suportadas para automação como não elegíveis para execução assistida (`assisted_execution_eligible=false`) e MUST evitar tentativa de instalação automática.
- **FR-015**: Quando Emacs já estiver instalado, o sistema MUST informar que ele já está disponível e MUST NOT reinstalá-lo por padrão.
- **FR-016**: Quando Emacs já estiver instalado, o sistema MUST sugerir `emacs-a11y doctor` e `emacs-a11y install --profile minimal` como próximos passos.
- **FR-017**: Quando a versão do Emacs não puder ser determinada, o sistema MUST emitir `WARNING` e MUST NOT reinstalar automaticamente.
- **FR-018**: O sistema MUST aplicar uma política de versão mínima suportada configurável pelos mantenedores e MUST tratar três resultados distintos: versão adequada, versão desconhecida e versão antiga. A política MUST usar `EMACS_A11Y_MIN_EMACS_VERSION` quando definida e válida; caso contrário, MUST usar um valor padrão do projeto documentado no código.
- **FR-019**: Quando a versão detectada estiver abaixo da política mínima suportada, o sistema MUST recomendar atualização ou reinstalação com consentimento explícito.
- **FR-020**: O fluxo padrão do comando MUST ser guidance-only (sem execução) e o sistema MUST só executar instalação após solicitação explícita de execução assistida e confirmação do usuário.
- **FR-021**: O sistema MAY oferecer execução assistida somente para comandos suportados e documentados para a plataforma detectada.
- **FR-022**: Antes de executar qualquer comando, o sistema MUST mostrar a plataforma detectada, o método detectado, o comando exato, a possível necessidade de privilégios, o efeito esperado e como cancelar.
- **FR-023**: O sistema MUST exigir confirmação explícita antes de executar qualquer gerenciador de pacotes, download, instalador ou operação com potencial impacto no sistema.
- **FR-024**: O sistema MUST permitir cancelamento seguro antes da execução e MUST informar o cancelamento com o marcador `CANCELLED`.
- **FR-025**: O sistema MUST NOT executar `winget`, `brew`, `apt`, `dnf`, `pacman` ou equivalente sem mostrar antes o comando exato e sem consentimento explícito.
- **FR-026**: O sistema MUST NOT alterar `PATH` silenciosamente.
- **FR-027**: O sistema MUST NOT solicitar privilégios administrativos silenciosamente.
- **FR-028**: O sistema MUST NOT baixar binários silenciosamente.
- **FR-029**: O sistema MUST NOT executar instaladores silenciosamente.
- **FR-030**: O sistema MUST NOT instalar Emacspeak ou configurar TTS como parte desta feature.
- **FR-031**: O sistema MUST NOT criar ou modificar o perfil do Emacs Acessível como parte desta feature.
- **FR-032**: O sistema MUST NOT modificar `~/.emacs`, `~/.emacs.d`, `~/.config/emacs` ou caminhos pessoais equivalentes.
- **FR-033**: O sistema MUST oferecer guidance-only como modo padrão e `--dry-run` como modo explícito para mostrar o que seria recomendado ou executado sem executar comandos.
- **FR-034**: O sistema MAY oferecer seleção explícita de método suportado, desde que a escolha permaneça simples, acessível e validada contra a plataforma detectada.
- **FR-035**: Se um modo não interativo como `--yes` ou equivalente for exposto nesta feature, ele MUST ser conservador, MUST NOT ser padrão, MUST NOT ignorar verificações de segurança e MUST falhar com segurança em operações privilegiadas ou ambientes não suportados.
- **FR-036**: O sistema MUST falhar com segurança quando o usuário solicitar execução assistida em plataforma ou método não suportado.
- **FR-037**: A saída do comando MUST usar marcadores textuais lineares e legíveis por leitor de tela, incluindo `INFO`, `WARNING`, `CRITICAL`, `COMMAND`, `CONFIRM`, `CANCELLED`, `NEXT STEP`, `SKIPPED`, `SUCCESS` e `FAILED` quando aplicável.
- **FR-038**: O contexto interativo `install` MUST listar `emacs`, `profile minimal`, `back`, `exit` e `help` com descrições lineares acessíveis.
- **FR-039**: O modo interativo MUST preservar o comportamento existente de `help`, `back` e `exit`.
- **FR-040**: O sistema MUST preservar o comportamento existente de `emacs-a11y doctor` e `emacs-a11y doctor --json`.
- **FR-041**: O sistema MUST preservar o comportamento existente de `emacs-a11y install --profile minimal`.
- **FR-042**: O sistema MUST aproveitar a capacidade diagnóstica já existente para detectar plataforma, disponibilidade do Emacs, versão quando possível e avisos relevantes, evitando divergência de comportamento entre comandos.
- **FR-043**: Em plataformas não suportadas para automação, o sistema MUST fornecer orientação manual útil e acionável, incluindo fonte oficial recomendada e próximo passo verificável, em vez de tentar adivinhar comandos inseguros.
- **FR-044**: Após uma execução assistida concluída com sucesso, o sistema MUST informar se o Emacs foi encontrado no ambiente e MUST fornecer próximos passos.
- **FR-045**: Se a execução assistida terminar com sucesso, mas o Emacs ainda não puder ser detectado, o sistema MUST emitir orientação explícita sobre reabrir shell, verificar `PATH` ou executar `emacs-a11y doctor`, sem modificar o ambiente automaticamente.
- **FR-046**: O comando MUST retornar códigos de saída significativos com o mapeamento: `0` sucesso, `1` guidance-only/dry-run/cancelamento explícito, `2` plataforma ou método indisponível para a ação solicitada, `3` falha do comando assistido e `4` erro interno.
- **FR-047**: O sistema MUST documentar claramente o relacionamento entre `install emacs`, `doctor` e `install --profile minimal`.
- **FR-048**: Execuções relevantes de `install emacs` MUST gerar logs textuais úteis para suporte remoto, com redaction de dados sensíveis.
- **FR-049**: Quando aplicável, o comando MUST documentar estratégia de reversão. Quando não houver reversão automática segura, MUST informar explicitamente as limitações e passos manuais.
- **FR-050**: O comando MUST incluir ajuda CLI com exemplos de uso, descrição de efeitos, riscos conhecidos e estratégia de reversão quando aplicável.

### Constitution Alignment *(mandatory)*

- **CA-001 Acessibilidade estrutural**: Toda recomendação, confirmação, aviso e próximo passo será textual, linear, navegável por teclado e compreensível por leitor de tela.
- **CA-002 CLI primária**: A feature cobre o comando direto `install emacs` e o fluxo contextual `install > emacs`, sem depender de interface gráfica.
- **CA-003 Não destrutivo e reversível**: A feature não modifica configuração pessoal de Emacs e exige consentimento explícito antes de qualquer execução assistida.
- **CA-004 Multiplataforma e adaptadores**: O comportamento deve diferenciar Windows, macOS e Debian/Ubuntu, com tratamento seguro para plataformas desconhecidas.
- **CA-005 Doctor-first**: O fluxo usa sinais diagnósticos consistentes para detecção de plataforma, Emacs e avisos antes de qualquer tentativa de execução.
- **CA-006 Segurança e consentimento**: Gerenciadores de pacotes, downloads, instaladores e operações potencialmente privilegiadas só podem ocorrer após exibição do comando exato e confirmação explícita.
- **CA-007 Perfis e modularidade**: A feature cobre somente a obtenção do Emacs e não cria perfis adicionais nem amplia escopo para Emacspeak/TTS.
- **CA-008 Distribuição e instalação**: O comportamento especificado deve funcionar de forma consistente no pacote Python canônico e em futuras distribuições derivadas.
- **CA-009 Scripts auxiliares**: O valor principal da feature está no fluxo da CLI e nas regras do assistente, não em scripts externos de plataforma.
- **CA-010 Documentação operacional**: A entrega exige documentação de modo direto, modo interativo, modo manual/dry-run, segurança, consentimento e próximos passos pós-instalação.

### Key Entities *(include if feature involves data)*

- **Environment Detection Result**: Representa o sistema operacional, arquitetura, disponibilidade do Emacs, caminho detectado, versão detectada e avisos relevantes do ambiente.
- **Installation Method Recommendation**: Representa o método recomendado para a plataforma atual, incluindo nome do método, comando recomendado, necessidade potencial de privilégios, modo manual suportado e elegibilidade para execução assistida.
- **Execution Consent Summary**: Representa o resumo textual apresentado antes da execução, incluindo plataforma, método, comando, impacto esperado, privilégios potenciais e instrução de cancelamento.
- **Installation Attempt Result**: Representa o desfecho do fluxo, incluindo status final, comando executado ou não, saída resumida, detecção pós-execução do Emacs, próximos passos e código de saída.
- **Version Support Assessment**: Representa a classificação da versão detectada como adequada, desconhecida ou abaixo da política mínima suportada.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Em 100% dos cenários suportados, o comando identifica plataforma e arquitetura antes de recomendar qualquer método de instalação.
- **SC-002**: Em 100% dos cenários em que Emacs já está disponível, o comando informa caminho detectado e não tenta reinstalar por padrão.
- **SC-003**: Em 100% dos cenários em que a versão do Emacs é legível, a saída informa a versão detectada.
- **SC-004**: Em 100% dos cenários de execução assistida, o comando exato é exibido antes de qualquer execução.
- **SC-005**: Em 100% dos cenários de execução assistida, nenhuma ação é executada sem confirmação explícita.
- **SC-006**: Em 100% dos cenários cancelados, nenhum gerenciador de pacotes, download ou instalador é executado.
- **SC-007**: Em 100% dos cenários em plataformas não suportadas, o sistema falha com segurança e fornece orientação útil sem tentar instalação automática.
- **SC-008**: Em 100% dos cenários de guidance-only ou dry-run, o resultado não altera o sistema local.
- **SC-009**: Em 100% dos cenários cobertos pela feature, nenhum arquivo de configuração pessoal do Emacs é modificado.
- **SC-010**: Em 100% dos cenários cobertos pela feature, o sistema não instala Emacspeak, não configura TTS e não cria o perfil `minimal`.
- **SC-011**: Em 100% dos cenários com Emacs ausente em Windows com `winget` disponível, a recomendação padrão apresenta `winget install -e --id GNU.Emacs`.
- **SC-012**: Em 100% dos cenários com Emacs ausente em macOS com Homebrew disponível, a recomendação padrão apresenta o método documentado baseado em Homebrew.
- **SC-013**: Em 100% dos cenários com Emacs ausente em Debian/Ubuntu, a recomendação padrão apresenta o fluxo documentado com `apt` e informa possível necessidade de privilégios.
- **SC-014**: Em 100% dos cenários com Emacs disponível, a saída recomenda `emacs-a11y doctor` e `emacs-a11y install --profile minimal` como próximos passos.
- **SC-015**: Os comandos `emacs-a11y doctor`, `emacs-a11y doctor --json`, `emacs-a11y install --profile minimal` e o contexto interativo `install` permanecem sem regressão nos testes existentes e nos novos testes da feature.
- **SC-016**: Em 100% das execuções relevantes da feature, logs textuais com status e decisão de fluxo são emitidos sem expor dados sensíveis.
- **SC-017**: Em 100% dos cenários em que houver efeito potencial no sistema, a documentação da feature explicita estratégia de reversão, ou explicita ausência de reversão automática com passos manuais.
- **SC-018**: Em 100% das validações contratuais da CLI, a ajuda do comando `install emacs` inclui exemplos de uso, efeitos esperados, riscos conhecidos e orientação de reversão quando aplicável.

## Assumptions

- A primeira entrega cobre apenas Windows, macOS e Debian/Ubuntu como plataformas com recomendação formal mínima.
- Métodos adicionais para Fedora, Arch e outras distribuições Linux podem ser adicionados em feature posterior sem alterar o comportamento seguro de ambientes ainda não suportados.
- A política de versão mínima suportada do Emacs será configurável por `EMACS_A11Y_MIN_EMACS_VERSION`, com fallback para valor padrão do projeto quando a variável estiver ausente ou inválida.
- Guidance-only é o comportamento seguro padrão sempre que a execução assistida não estiver claramente suportada.
- A execução assistida só deve abranger comandos previamente documentados e considerados seguros para o ambiente detectado.
- A instalação do Emacs pode exigir reinício de shell, atualização de sessão ou ajuste manual do ambiente para que o executável passe a ser detectado, e esta feature apenas orienta o usuário sobre isso.
- A feature deve manter compatibilidade com a infraestrutura diagnóstica e com os fluxos já existentes de `doctor` e `install --profile minimal`.

## Out of Scope

- Instalar ou configurar Emacspeak.
- Instalar ou configurar TTS.
- Instalar SharpWin.
- Criar ou modificar o perfil `minimal`.
- Editar configuração pessoal do Emacs.
- Instalar pacotes Lisp adicionais.
- Implementar interface gráfica.
- Corrigir automaticamente `PATH`.
- Executar operações privilegiadas sem consentimento explícito.
- Cobrir de forma automática todas as distribuições Linux na primeira versão.