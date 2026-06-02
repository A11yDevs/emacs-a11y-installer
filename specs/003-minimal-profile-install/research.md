# Research: Minimal Profile Install

## Decision 1: Tratar a feature ativa como `003-minimal-profile-install`
- Decision: Planejar e manter todos os artefatos da implementação em `specs/003-minimal-profile-install/`.
- Rationale: O workspace contém a especificação ativa da feature 003 e ponteiro oficial em `.specify/feature.json`.
- Alternatives considered: renumeração de diretório durante o planejamento (rejeitado por quebrar consistência dos artefatos já existentes).

## Decision 2: Usar uma fonte de template canônica empacotável
- Decision: Planejar um subsistema de templates com `TemplateLocator` e `TemplateSource` para resolver a configuração base do perfil a partir de três fontes compatíveis: pacote Python instalado, executável futuro e caminho local de desenvolvimento.
- Rationale: A feature precisa funcionar via `pipx`, permanecer compatível com PyInstaller no futuro e suportar desenvolvimento local sem clonar ou baixar o repositório canônico em runtime.
- Alternatives considered: gerar `init.el` e módulos do zero no instalador (rejeitado porque o pedido exige referência canônica ao repositório `A11yDevs/emacs-a11y`).

## Decision 3: Empacotar a estrutura canônica relevante em `src/emacs_a11y/resources/a11y-emacs/`
- Decision: Planejar a materialização da estrutura base `early-init.el`, `init.el` e `lisp/` como recursos do pacote Python.
- Rationale: Recursos empacotados permitem instalação offline, previsível e compatível com `pipx`/PyInstaller, sem download dinâmico durante a instalação minimal.
- Alternatives considered: ler diretamente de um repositório externo em disco (rejeitado por fragilidade e por não ser garantido no ambiente do usuário final).

## Decision 4: Filtrar a ativação do perfil minimal no `init.el`
- Decision: Planejar um `init.el` minimal derivado da estrutura canônica, ativando apenas `init-packages`, `init-core` e `init-dired`.
- Rationale: Garante que o perfil minimal seja inicializável sem Emacspeak/TTS nesta fase e evita dependências fora do escopo.
- Alternatives considered: ativar também `init-accessibility` (rejeitado por potencial quebrar inicialização quando Emacspeak não estiver instalado).

## Decision 5: Copiar a pasta `lisp/` inteira empacotada, mas ativar somente os módulos mínimos
- Decision: Planejar cópia da estrutura `lisp/` preservando hierarquia original, enquanto o `init.el` minimal carrega apenas os três módulos permitidos.
- Rationale: Simplifica manutenção e evolução futura de perfis, reduz regras especiais de cópia e preserva fidelidade à estrutura canônica.
- Alternatives considered: copiar somente os quatro arquivos mínimos (rejeitado por aumentar divergência com a árvore canônica e tornar expansão futura mais cara).

## Decision 6: Instalação em duas fases: planejar primeiro, escrever depois
- Decision: Separar `planner`, `writer` e `validator`, preparando todo o plano antes de qualquer escrita e gravando apenas após confirmação.
- Rationale: Reduz risco de escrita parcial, melhora acessibilidade da revisão pré-instalação e fortalece reversibilidade.
- Alternatives considered: validar e escrever item a item no mesmo passo (rejeitado por dificultar rollback e clareza do plano).

## Decision 7: Reusar a infraestrutura do doctor quando útil, sem acoplamento indevido
- Decision: Reaproveitar detecção de Emacs, plataforma, configuração pessoal e permissões quando essa lógica já existir no `doctor`, mas manter o fluxo de instalação em módulos próprios.
- Rationale: Evita duplicação de regras diagnósticas e preserva separação clara entre diagnóstico e instalação.
- Alternatives considered: duplicar checks críticos no instalador (rejeitado por risco de drift comportamental).

## Decision 7.1: Tratar Emacs como pré-condição obrigatória via preflight
- Decision: Introduzir etapa de preflight obrigatório antes de template/planner/writer; se Emacs estiver ausente, abortar com `CRITICAL` e zero escrita.
- Rationale: Perfil `minimal` sem Emacs não é validável e gera falsa percepção de sucesso.
- Alternatives considered: criar perfil mesmo sem Emacs e marcar validação como `skipped` (rejeitado por reduzir confiabilidade operacional).

## Decision 8: Confirmação explícita e `--yes` com escopo estritamente limitado
- Decision: Permitir `--yes` apenas para `install --profile minimal` totalmente explícito; todos os demais fluxos exigem confirmação textual/interativa.
- Rationale: Mantém automação segura sem abrir brecha para ações ambíguas ou destrutivas.
- Alternatives considered: aceitar `--yes` em qualquer forma de `install` (rejeitado por ampliar risco operacional).

## Decision 9: Validação de runtime do Emacs deve ser segura e opcional
- Decision: Planejar validação não invasiva, preferencialmente em batch/dry-run, somente quando `emacs` estiver disponível e sem instalar pacotes nem escrever fora do perfil isolado.
- Rationale: Atende ao requisito de confiança sem transformar a validação em operação arriscada.
- Alternatives considered: exigir Emacs presente para concluir a instalação (rejeitado por ser desnecessariamente bloqueante).

Nota de revisão: Em fase posterior de especificação, Emacs passou a ser pré-condição obrigatória. Assim, validação de runtime ocorre apenas no ramo com preflight aprovado; ramo sem Emacs aborta antes da escrita.

## Decision 10: Logs e rollback guiados por artefatos criados
- Decision: Registrar logs apenas em local project-owned e produzir resumo final com itens criados/copiados/preservados/falhos e instruções manuais de remoção.
- Rationale: Observabilidade e reversibilidade são exigências constitucionais; a primeira versão não deve executar remoção automática agressiva.
- Alternatives considered: rollback automático total em qualquer falha (rejeitado por poder remover em excesso sem confirmação explícita).

## Resolved Clarifications
- A fonte canônica dos templates é externa ao workspace atual; o plano assume que sua estrutura será vendorizada/empacotada no pacote durante a implementação.
- O perfil minimal ativará somente `init-packages`, `init-core` e `init-dired`; `init-accessibility` permanece inativo nesta fase.
- Emacs ausente gera aborto crítico sem escrita e com orientação para comando futuro `emacs-a11y install emacs`.
- O fluxo interativo adicionará contexto `install` sem quebrar o modo contextual existente.
- A feature permanece restrita ao perfil `minimal`; perfis avançados ficam apenas preparados arquiteturalmente.
