# Feature Specification: Minimal Profile Install

**Feature Branch**: `[003-next-speckit-spec]`

**Created**: 2026-06-01

**Status**: Draft

**Input**: User description: "Create the next feature of the emacs-a11y-installer: a safe, accessible, non-destructive minimal profile installation command named emacs-a11y install --profile minimal."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Primeira instalação minimal segura (Priority: P1)

Como pessoa usuária iniciante, quero executar `emacs-a11y install --profile minimal` para criar um perfil mínimo isolado do Emacs Acessível sem risco para minha configuração pessoal existente.

**Why this priority**: É o objetivo principal da feature e entrega valor imediato de entrada segura no projeto.

**Independent Test**: Executar `emacs-a11y install --profile minimal`, revisar plano pré-instalação, confirmar, validar criação apenas no diretório isolado e receber resumo com rollback.

**Acceptance Scenarios**:

1. **Given** ambiente com permissões válidas, **When** a pessoa executa `emacs-a11y install --profile minimal`, **Then** o sistema apresenta plano textual linear e pede confirmação antes de gravar.
2. **Given** plano apresentado e confirmação explícita, **When** a instalação é executada, **Then** apenas arquivos/diretórios do perfil isolado são criados.
3. **Given** instalação concluída, **When** o comando termina, **Then** o sistema exibe resumo com itens `CREATED`/`SKIPPED` e instruções de remoção segura.
4. **Given** `init.el` gerado para o perfil minimal, **When** seu conteúdo é validado, **Then** ele contém apenas `(require 'init-packages)`, `(require 'init-core)` e `(require 'init-dired)` como módulos obrigatórios da feature.
5. **Given** `init.el` gerado para o perfil minimal, **When** seu conteúdo é validado, **Then** ele não contém `(require 'init-accessibility)`.

---

### User Story 2 - Proteção de configuração pessoal existente (Priority: P1)

Como pessoa usuária que já possui configuração pessoal de Emacs, quero garantia explícita de que meus arquivos pessoais não serão modificados, migrados, apagados ou sobrescritos.

**Why this priority**: Não destrutividade é requisito constitucional e crítico para confiança no instalador.

**Independent Test**: Executar instalação em ambiente com `~/.emacs`, `~/.emacs.d` ou `~/.config/emacs` existentes e verificar mensagens explícitas de proteção e ausência de escrita nesses caminhos.

**Acceptance Scenarios**:

1. **Given** configurações pessoais existentes, **When** o plano pré-instalação é exibido, **Then** o sistema informa explicitamente que esses caminhos não serão tocados.
2. **Given** instalação confirmada, **When** o processo conclui, **Then** nenhum caminho pessoal de Emacs foi alterado.

---

### User Story 3 - Instalação via modo interativo contextual (Priority: P2)

Como pessoa usuária em navegação assistida, quero acessar `install` a partir de `emacs-a11y>`, escolher perfil `minimal`, revisar plano e confirmar/cancelar usando apenas teclado.

**Why this priority**: Mantém consistência com a CLI contextual acessível e amplia usabilidade para quem prefere fluxo guiado.

**Independent Test**: Iniciar `emacs-a11y`, entrar no contexto `install`, selecionar `minimal`, executar confirmação/cancelamento e validar suporte contínuo de `help`, `back` e `exit`.

**Acceptance Scenarios**:

1. **Given** modo interativo ativo no contexto raiz, **When** a pessoa entra em `install`, **Then** o contexto de instalação apresenta opções de perfil e ajuda contextual.
2. **Given** contexto `install` ativo, **When** a pessoa escolhe `minimal`, **Then** o sistema apresenta plano pré-instalação e pede confirmação.
3. **Given** qualquer contexto interativo, **When** a pessoa usa `help`, `back` ou `exit`, **Then** os comandos globais funcionam conforme já estabelecido.

---

### User Story 4 - Execução não interativa segura para automação (Priority: P2)

Como mantenedor(a) ou suporte, quero executar instalação minimal repetível com `--yes` somente quando a ação for explícita, segura e limitada.

**Why this priority**: Permite automação previsível sem abrir risco de operações ambíguas ou destrutivas.

**Independent Test**: Executar `emacs-a11y install --profile minimal --yes` e validar execução sem prompt apenas no caso explícito; testar combinações não explícitas e validar recusa segura.

**Acceptance Scenarios**:

1. **Given** comando explícito `install --profile minimal --yes`, **When** a execução inicia, **Then** o sistema pode prosseguir sem confirmação interativa.
2. **Given** ação não explícita ou fora do escopo seguro, **When** `--yes` é usado, **Then** o sistema falha com mensagem acionável sem gravar alterações.

---

### User Story 5 - Aborto seguro quando Emacs não está disponível (Priority: P1)

Como pessoa usuária sem Emacs instalado, quero que a instalação do perfil minimal seja abortada de forma segura e explicativa, para que eu saiba instalar a dependência correta antes de tentar novamente.

**Why this priority**: Emacs é pré-condição obrigatória para validar o perfil minimal; continuar sem Emacs gera falsa sensação de sucesso.

**Independent Test**: Executar `emacs-a11y install --profile minimal` sem Emacs disponível e validar aborto antes de qualquer escrita, mensagem `CRITICAL` e orientação de próximo passo.

**Acceptance Scenarios**:

1. **Given** Emacs não está disponível, **When** a pessoa executa `emacs-a11y install --profile minimal`, **Then** o sistema aborta antes de qualquer escrita.
2. **Given** Emacs não está disponível, **When** a instalação aborta, **Then** a saída contém `CRITICAL: Emacs não encontrado`.
3. **Given** Emacs não está disponível, **When** a instalação aborta, **Then** nenhum arquivo do perfil é criado.
4. **Given** Emacs não está disponível, **When** a instalação aborta, **Then** nenhuma configuração pessoal de Emacs é modificada.
5. **Given** Emacs não está disponível, **When** a instalação aborta, **Then** a saída sugere `emacs-a11y install emacs` como próximo passo futuro.
6. **Given** Emacs não está disponível, **When** a instalação aborta, **Then** nenhum download, gerenciador de pacotes, alteração de `PATH` ou privilégio administrativo é solicitado.

---

### User Story 6 - Tratamento de perfil existente, permissões e falha parcial (Priority: P3)

Como pessoa usuária, quero receber comportamento seguro e orientações claras quando o perfil já existe ou quando há erro de permissão.

**Why this priority**: Garante robustez operacional em cenários reais e reduz suporte reativo.

**Independent Test**: Testar cenários separados de diretório já existente e erro de permissão; validar mensagens lineares, resumo de impacto e recomendação de limpeza/rollback.

**Acceptance Scenarios**:

1. **Given** perfil isolado já existente, **When** instalação é solicitada, **Then** o sistema não sobrescreve silenciosamente e exige confirmação explícita para itens project-owned.
2. **Given** falha parcial por permissão, **When** o processo interrompe, **Then** o sistema lista o que foi criado e fornece orientação de limpeza segura.
3. **Given** ambiente sem Emacspeak instalado, **When** a instalação minimal é executada com Emacs disponível, **Then** ela não falha por ausência de `emacspeak-setup.el`.
4. **Given** ambiente sem Emacspeak/TTS, **When** a instalação minimal é executada com Emacs disponível, **Then** ela não exige variáveis ou funções `dtk-*` ou `emacspeak-*` para concluir.
5. **Given** instalação minimal concluída, **When** o comando finaliza, **Then** a saída informa explicitamente que recursos de acessibilidade por Emacspeak serão ativados em etapa futura.

### Edge Cases

- Caminho de perfil isolado já existe parcialmente com mistura de arquivos project-owned e arquivos desconhecidos.
- `--yes` é informado sem `--profile minimal` explícito.
- Falha ao criar subdiretório após criação de diretórios anteriores.
- Emacs ausente, mas perfil minimal ainda não existe.
- Emacs ausente, mas perfil minimal já existe parcialmente.
- Emacs ausente em modo interativo após escolha de `minimal`.
- Emacs ausente com `--yes`.
- Emacs ausente e usuário tenta repetir o comando.
- Emacs ausente, mas existe comando futuro `install emacs` documentado apenas como próximo passo.
- Emacs está disponível, mas validação segura de startup retorna falha.
- Modo interativo recebe cancelamento após plano exibido e antes da escrita.
- Ambiente com configuração pessoal em múltiplos caminhos (`~/.emacs`, `~/.emacs.d`, `~/.config/emacs`).
- Ambiente sem Emacspeak instalado e com `init-accessibility.el` presente no template base.
- Template canônico inclui `init-accessibility.el`, mas `init.el` minimal não deve ativá-lo.
- Ambiente sem `emacspeak-setup.el` legível.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST fornecer o comando direto `emacs-a11y install --profile minimal`.
- **FR-002**: O sistema MUST permitir acesso equivalente à instalação minimal via modo interativo contextual.
- **FR-003**: O sistema MUST detectar o diretório de perfil isolado do Emacs Acessível apropriado para a plataforma.
- **FR-004**: O sistema MUST detectar se o perfil alvo já existe antes de qualquer escrita.
- **FR-005**: O sistema MUST detectar configurações pessoais existentes de Emacs e declarar explicitamente que não serão modificadas.
- **FR-006**: O sistema MUST apresentar plano pré-instalação linear e acessível antes de qualquer escrita.
- **FR-007**: O sistema MUST exigir confirmação explícita antes de gravar, exceto no modo seguro e explícito com `--yes`.
- **FR-008**: O sistema MUST criar apenas arquivos e diretórios mínimos project-owned dentro do perfil isolado.
- **FR-009**: O sistema MUST NOT escrever em `~/.emacs.d`, `~/.emacs`, `~/.config/emacs` ou caminhos pessoais equivalentes nesta feature.
- **FR-010**: O sistema MUST NOT sobrescrever arquivos existentes silenciosamente; sobrescrita só MAY ocorrer para artefatos project-owned com confirmação explícita.
- **FR-011**: O sistema MUST validar os artefatos criados após a escrita e reportar status por item.
- **FR-012**: O sistema MUST tentar validação segura de startup do Emacs com perfil isolado quando Emacs estiver disponível e a validação for não invasiva.
- **FR-013**: O sistema MUST verificar a disponibilidade de Emacs antes de gerar ou executar qualquer plano de escrita.
- **FR-014**: O sistema MUST gerar resumo final claro com itens `CREATED`, `COPIED`, `SKIPPED`, `PRESERVED`, `FAILED`, `WARNING`, `CRITICAL` e `NEXT STEP`.
- **FR-015**: O sistema MUST gerar logs de suporte sem segredos, apenas em local project-owned documentado.
- **FR-016**: O sistema MUST fornecer orientação de rollback/remoção após sucesso e após falha parcial.
- **FR-017**: O sistema MUST falhar com mensagens acionáveis e preservar estado seguro em caso de erro.
- **FR-018**: O sistema MUST manter comportamento existente de `emacs-a11y doctor` e `emacs-a11y doctor --json` sem alteração funcional.
- **FR-019**: O sistema MUST manter compatibilidade com distribuição em pacote Python e capacidade futura de executáveis standalone derivados.
- **FR-020**: Em qualquer contexto interativo, `help`, `back` e `exit` MUST continuar funcionando.
- **FR-021**: O modo `--yes` MUST ser aceito apenas quando a ação solicitada for explícita, segura, limitada e totalmente especificada como perfil minimal.
- **FR-022**: O plano pré-instalação MUST listar exatamente quais arquivos e diretórios serão criados antes da confirmação.
- **FR-023**: O perfil `minimal` MUST ser básico, seguro e inicializável sem depender de Emacspeak, TTS ou servidor de voz.
- **FR-024**: O `init.el` gerado para o perfil `minimal` MUST carregar somente `(require 'init-packages)`, `(require 'init-core)` e `(require 'init-dired)` como módulos obrigatórios da feature.
- **FR-025**: O `init.el` gerado para o perfil `minimal` MUST NOT carregar `(require 'init-accessibility)`.
- **FR-026**: A instalação `minimal` MUST NOT executar código que dependa de `dtk-*`, `emacspeak-*` ou `emacspeak-setup.el`.
- **FR-027**: O arquivo `init-accessibility.el` MAY existir no template empacotado/base, mas MUST permanecer inativo por padrão no perfil `minimal`.
- **FR-028**: A ativação de `init-accessibility` MUST ser tratada por feature posterior, após instalação e validação de Emacspeak/TTS.
- **FR-029**: O comando `emacs-a11y install --profile minimal` MUST validar que o perfil criado pode iniciar com segurança mesmo quando Emacspeak não está instalado.
- **FR-030**: A saída final da instalação `minimal` MUST informar que acessibilidade por voz via Emacspeak não faz parte desta etapa e será habilitada em fase futura.
- **FR-031**: O sistema MUST abortar a instalação do perfil `minimal` quando Emacs não estiver disponível.
- **FR-032**: O sistema MUST reportar ausência de Emacs como `CRITICAL: Emacs não encontrado` em saída textual linear e acessível.
- **FR-033**: O sistema MUST garantir zero escrita em disco quando Emacs não estiver disponível.
- **FR-034**: O sistema MUST sugerir `emacs-a11y install emacs` como próximo passo futuro quando Emacs estiver ausente.
- **FR-035**: O sistema MUST recomendar, após instalação futura do Emacs, a execução de `emacs-a11y doctor` e `emacs-a11y install --profile minimal`.
- **FR-036**: O sistema MUST NOT baixar, instalar ou configurar Emacs nesta feature.
- **FR-037**: O sistema MUST NOT executar `winget`, `brew`, `apt`, `dnf`, `pacman` ou gerenciadores equivalentes nesta feature.
- **FR-038**: O sistema MUST NOT alterar `PATH` nesta feature.
- **FR-039**: O sistema MUST NOT solicitar privilégios administrativos nesta feature.
- **FR-040**: No modo interativo `install > minimal`, quando Emacs estiver ausente, o sistema MUST exibir `CRITICAL`, informar que nada foi criado, sugerir `install emacs` e manter navegação clara com `help`, `back` e `exit`.
- **FR-041**: O contexto `install` MAY incluir futuramente instalação de dependências e componentes (`install emacs`, `install emacspeak`, `install tts`, `install tts --engine sharpwin`), mas nesta feature apenas `install --profile minimal` está em escopo.

### Constitution Alignment *(mandatory)*

- **CA-001 Acessibilidade estrutural**: Prompts, confirmações, avisos, sucesso, erros e logs serão lineares, com linguagem explícita e sem dependência de cor ou layout visual.
- **CA-002 CLI primária**: A feature cobre modo direto (`install --profile minimal`) e modo interativo contextual com comportamento equivalente.
- **CA-003 Não destrutivo e reversível**: Operação limitada a perfil isolado project-owned, com confirmação explícita e instruções de rollback/remoção.
- **CA-004 Multiplataforma e adaptadores**: Diretório isolado e validações respeitam diferenças de plataforma sem tocar caminhos pessoais.
- **CA-005 Doctor-first**: Reuso de checks diagnósticos quando útil para detecção de Emacs, permissões e estado de perfil, evitando duplicação de lógica.
- **CA-006 Segurança e consentimento**: Escrita só após confirmação explícita ou `--yes` seguro e explícito; nenhuma operação privilegiada implícita.
- **CA-007 Perfis e modularidade**: Escopo restrito ao perfil `minimal`, preparando base modular para perfis futuros.
- **CA-008 Distribuição e instalação**: Comando projetado para pacote Python canônico e compatível com futura distribuição standalone.
- **CA-009 Scripts auxiliares**: Lógica de instalação permanece no núcleo Python; scripts de plataforma permanecem apenas adaptadores.
- **CA-010 Documentação operacional**: A feature exigirá atualização de ajuda CLI, quickstart e documentação operacional com fluxo de confirmação e rollback.

### Key Entities *(include if feature involves data)*

- **InstallRequest**: Requisição de instalação contendo modo (direto/interativo), perfil solicitado, confirmação, política de sobrescrita e flag `--yes`.
- **InstallPlanItem**: Item planejado de criação com caminho alvo, tipo (arquivo/diretório), status planejado e indicador project-owned.
- **InstallPlan**: Conjunto ordenado de itens planejados, mensagens de proteção de configuração pessoal e pré-condições de segurança.
- **InstallExecutionResult**: Resultado da execução com listas de `CREATED`, `COPIED`, `SKIPPED`, `PRESERVED`, `FAILED`, validações, logs e próximo passo.
- **RollbackGuidance**: Instruções textuais para remoção segura de artefatos criados e limpeza após falha parcial.
- **RuntimeValidationResult**: Resultado da validação de startup com perfil isolado, incluindo estado `validated`, `skipped` ou `failed` com motivo.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Em 100% dos testes da feature, nenhum arquivo de configuração pessoal de Emacs é modificado.
- **SC-002**: Em 100% dos cenários de instalação bem-sucedida, todos os artefatos criados estão exclusivamente dentro do diretório isolado do Emacs Acessível.
- **SC-003**: Em 100% dos fluxos interativos sem `--yes`, a confirmação explícita é solicitada antes de qualquer escrita.
- **SC-004**: Em 100% dos testes de automação com comando explícito `install --profile minimal --yes`, a execução ocorre sem prompt e com comportamento equivalente ao fluxo confirmado interativo.
- **SC-005**: Em 100% dos cenários com perfil existente, não ocorre sobrescrita silenciosa.
- **SC-006**: Em 100% dos cenários de saída, mensagens e logs seguem formato linear com marcadores textuais explícitos (`INFO`, `WARNING`, `CRITICAL`, `CREATED`, `COPIED`, `SKIPPED`, `PRESERVED`, `FAILED`, `NEXT STEP`).
- **SC-007**: Em 100% dos cenários com Emacs disponível e validação segura possível, a validação de runtime é tentada e reportada.
- **SC-008**: Em 100% dos cenários de falha parcial, o sistema informa itens criados e fornece orientação de rollback acionável.
- **SC-009**: Comandos `emacs-a11y doctor` e `emacs-a11y doctor --json` mantêm comportamento atual sem regressão nos testes existentes.
- **SC-010**: Em 100% dos perfis `minimal` gerados, `init.el` contém `(require 'init-packages)`, `(require 'init-core)` e `(require 'init-dired)`.
- **SC-011**: Em 100% dos perfis `minimal` gerados, `init.el` não contém `(require 'init-accessibility)`.
- **SC-012**: Em 100% dos testes de instalação `minimal` sem Emacspeak instalado, a instalação conclui sem falha causada por ausência de `emacspeak-setup.el`.
- **SC-013**: Em 100% dos testes de instalação `minimal` sem Emacspeak/TTS, o fluxo não depende de variáveis ou funções `dtk-*` ou `emacspeak-*`.
- **SC-014**: Em 100% das execuções `minimal`, a saída final informa que recursos de voz por Emacspeak pertencem a etapa futura.
- **SC-015**: Em 100% dos cenários sem Emacs, a instalação aborta antes de qualquer escrita.
- **SC-016**: Em 100% dos cenários sem Emacs, a saída contém `CRITICAL: Emacs não encontrado`.
- **SC-017**: Em 100% dos cenários sem Emacs, nenhum arquivo do perfil minimal é criado.
- **SC-018**: Em 100% dos cenários sem Emacs, nenhuma configuração pessoal de Emacs é modificada.
- **SC-019**: Em 100% dos cenários sem Emacs, nenhum download, gerenciador de pacotes, alteração de `PATH` ou privilégio administrativo é executado.
- **SC-020**: Em 100% dos cenários sem Emacs, a saída sugere `emacs-a11y install emacs` como próximo passo futuro.

## Assumptions

- O diretório de perfil isolado será resolvido por convenção de plataforma e permanecerá distinto da configuração pessoal de Emacs.
- Emacs é pré-condição obrigatória para instalar e validar o perfil `minimal`.
- A primeira entrega de `minimal` prioriza estrutura mínima funcional do perfil e não inclui instalação de componentes avançados.
- Validação de runtime do Emacs será não invasiva e limitada a checagens seguras quando o executável estiver disponível.
- Logs de suporte devem evitar informações sensíveis e registrar apenas dados operacionais necessários para troubleshooting.
- Operações avançadas de migração/edição de configuração pessoal permanecem fora do escopo desta feature.
- `init-accessibility.el` pode existir no template canônico para evolução futura, sem ativação no `init.el` do perfil `minimal`.
- Recursos de voz (Emacspeak/TTS) serão tratados em feature posterior, após fluxo de instalação/validação próprio.
- A instalação assistida do Emacs será especificada em feature posterior (por exemplo, `004-emacs-install-assistant`).
- O comando futuro `emacs-a11y install emacs` pode ser mencionado como orientação, mas não deve ser implementado nesta feature.

## Out of Scope

- Instalar o Emacs.
- Baixar Emacs.
- Executar instaladores do Emacs.
- Executar `winget`, `brew`, `apt`, `dnf`, `pacman` ou gerenciadores equivalentes.
- Alterar `PATH`.
- Solicitar privilégios administrativos.
- Implementar `emacs-a11y install emacs`.
- Instalar ou configurar Emacspeak.
- Configurar TTS.
- Ativar `init-accessibility` no perfil `minimal`.
- Executar código dependente de `dtk-*`, `emacspeak-*` ou `emacspeak-setup.el` durante instalação `minimal`.
- Instalar perfis Java, Python, LaTeX, AI ou full.
- Instalar pacotes Lisp de MELPA/ELPA.
- Criar instaladores nativos.
- Criar interface gráfica.
- Migrar ou editar configuração pessoal existente de Emacs.
