<!--
Sync Impact Report
- Version change: 2.0.0 -> 2.1.0
- Modified principles:
	- Artigo VI — Python como núcleo, scripts como adaptadores -> Artigo VI — Python como núcleo canônico e scripts como adaptadores
	- Artigo XII — Simplicidade antes de empacotamento sofisticado -> Artigo XII — Estratégia oficial de distribuição em camadas
- Added sections:
	- Estratégia Oficial de Distribuição e Instalação
- Removed sections:
	- None
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md
	- ✅ .specify/templates/spec-template.md
	- ✅ .specify/templates/tasks-template.md
	- ✅ .specify/templates/commands/*.md (não há arquivos)
	- ✅ README.md
- Follow-up TODOs:
	- None
-->

# Constituição do Projeto Emacs Acessível Installer

## Princípios Fundamentais

### Artigo I — Acessibilidade como requisito estrutural
A acessibilidade MUST ser tratada como requisito arquitetural. Todo comando,
mensagem, erro, confirmação, log e relatório MUST ser utilizável em terminal,
com leitor de tela e fluxo sem mouse. A saída textual MUST ser clara, linear e
objetiva. O fluxo principal de instalação MUST ser executável integralmente por
teclado e compreensível por saída textual linear. Rationale: o objetivo do
projeto é autonomia real de pessoas cegas ou
com baixa visão durante instalação e manutenção do ambiente.

### Artigo II — CLI como interface primária
A interface principal MUST ser CLI e MUST cobrir todos os comportamentos
essenciais de instalação, diagnóstico, atualização, reparo e remoção. A CLI
MUST aceitar argumentos explícitos, oferecer modo interativo acessível,
oferecer modo não interativo para automação e permitir saída textual e JSON
quando aplicável. Rationale: CLI acessível é o caminho mais portátil, testável e
automatizável para este contexto.

### Artigo III — Instalação não destrutiva
O instalador MUST preservar configurações pessoais existentes por padrão e MUST
usar perfil isolado para o Emacs Acessível. Alterações destrutivas só MAY
ocorrer com consentimento explícito do usuário e mecanismo reversível definido.
Rationale: preservar o ambiente atual evita perda de configuração e reduz risco.

### Artigo IV — Multiplataforma com comportamento nativo
O projeto MUST funcionar em Windows, macOS e Linux, com adaptação explícita às
convenções de cada sistema. Regras comuns MUST ficar no núcleo Python e regras
específicas MUST ser isoladas em módulos de plataforma. Rationale: separação
clara reduz acoplamento e melhora manutenção de comportamentos nativos.

### Artigo V — Diagnóstico antes da instalação
O comando doctor MUST ser funcionalidade central desde o início. Antes de
instalar ou alterar qualquer componente, o sistema MUST diagnosticar ambiente,
dependências, TTS, Emacs/Emacspeak, permissões e riscos prováveis, sugerindo
ações concretas sem alterações automáticas não solicitadas. Rationale:
diagnóstico antecipado evita falhas opacas e suporte reativo.

### Artigo VI — Python como núcleo canônico e scripts como adaptadores
O projeto MUST ter um pacote Python multiplataforma como formato canônico de
código-fonte e distribuição técnica. O núcleo de decisão MUST ser implementado
em Python modular e testável. Scripts de shell/PowerShell MAY existir para
bootstrap, automação, suporte técnico e desenvolvimento, mas MUST NOT conter a
regra de negócio principal do instalador. Rationale: centralização de regras em
um núcleo único facilita testes, rastreabilidade e evolução multiplataforma.

### Artigo VII — Testes antes de implementação
Funcionalidades de produção MUST ter comportamento especificado e validação
automatizada antes da implementação principal. Protótipos exploratórios MAY ser
criados sem teste prévio, mas MUST ser convertidos em especificação, teste e
documentação antes de entrar na branch principal. O ciclo mínimo para código de
produção MUST ser: especificar -> escrever teste -> observar falha inicial
quando aplicável -> implementar -> validar -> documentar. Rationale: reduz
regressões e dá segurança para mudanças em fluxos críticos de instalação e
configuração sem bloquear exploração técnica controlada.

### Artigo VIII — Segurança, consentimento e reversibilidade
Operações com privilégio, alteração de PATH, modificação de arquivos existentes,
download de binários e remoções MUST exigir confirmação explícita. Alterações
MUST ser reversíveis sempre que tecnicamente viável. Rationale: o instalador
atua sobre o ambiente local do usuário e precisa de postura conservadora.

### Artigo IX — Modularidade e perfis
Distribuição de recursos MUST ser orientada por perfis e módulos opcionais.
Perfis iniciais recomendados são minimal, java, python, latex, ai e full. O
perfil padrão MUST ser funcional, acessível e mínimo, evitando carga excessiva.
Rationale: modularidade permite adoção progressiva sem comprometer usabilidade.

### Artigo X — Observabilidade e suporte remoto
Execuções relevantes MUST gerar logs textuais úteis para suporte remoto e
diagnóstico assistido. Logs MUST ocultar segredos e dados sensíveis, mantendo
contexto técnico necessário para análise. Rationale: visibilidade operacional é
parte essencial da acessibilidade e manutenção comunitária.

### Artigo XI — Documentação como parte da entrega
Nenhuma funcionalidade é completa sem documentação mínima. Cada comando MUST
incluir ajuda CLI, exemplo de uso, descrição de efeitos, riscos conhecidos e
estratégia de reversão quando aplicável. Rationale: documentação operacional é
parte do produto e não um artefato opcional.

### Artigo XII — Estratégia oficial de distribuição em camadas
A estratégia oficial MUST priorizar pacote Python multiplataforma como base
canônica, com instalação preferencial via `pipx` para usuários técnicos.
Executáveis autônomos gerados do mesmo código-fonte (por exemplo,
`emacs-a11y.exe` via PyInstaller) MAY ser oferecidos para usuários finais,
especialmente no Windows. Qualquer executável empacotado MUST incluir runtime
Python e dependências necessárias, sem exigir instalação prévia de Python, pip
ou pipx. A instalação via `pipx` MAY exigir Python previamente instalado.
A evolução recomendada MUST seguir esta ordem: pacote Python local durante
desenvolvimento -> instalação via `pipx` -> executáveis empacotados -> pacotes
nativos (MSI, PKG, DEB, APT, Homebrew, AppImage) -> GUI opcional. Rationale:
uma cadeia progressiva preserva simplicidade operacional e amplia adoção sem
fragmentar o núcleo técnico.

## Escopo e Restrições de Arquitetura

- O escopo inicial MUST cobrir detecção de SO, verificação de Emacs,
	configuração de perfil isolado, integração com o fork do Emacspeak mantido
	pela A11yDevs, configuração do servidor de voz/TTS adequado à plataforma,
	gerenciamento de pacotes e comandos de diagnóstico/instalação/atualização/
	reparo/remoção.
- O núcleo de código MUST manter separação entre módulos comuns e módulos de
	plataforma para evitar condicionais espalhados.
- A primeira versão funcional MUST priorizar os comandos `--help`, `doctor`,
	`install` com perfil mínimo, configuração de TTS, atualização e remoção.

## Estratégia Oficial de Distribuição e Instalação

- A distribuição técnica canônica MUST ser um pacote Python multiplataforma.
- A instalação recomendada para usuários técnicos MUST ser via `pipx`.
- Distribuições autônomas para usuários finais MAY ser publicadas a partir do
	mesmo código-fonte, com prioridade inicial para Windows.
- Executáveis autônomos MUST embutir runtime Python e dependências, e MUST
	executar sem Python/pip/pipx pré-instalados.
- Scripts auxiliares (`.ps1`, `.sh` e equivalentes) MAY suportar bootstrap e
	operações de manutenção, mas MUST NOT substituir o núcleo lógico do instalador.

## Fluxo de Entrega e Gates de Qualidade

- Mudanças não triviais MUST seguir o fluxo spec -> plan -> tasks antes da
	implementação.
- Toda especificação MUST explicitar problema, objetivos, histórias, requisitos,
	critérios de aceitação, riscos, plano de teste e impacto em acessibilidade.
- Todo plano técnico MUST justificar dependências, impacto multiplataforma,
	impacto em acessibilidade, estratégia de teste, reversão e riscos de segurança.
- Toda entrega MUST passar em validação automatizada, apresentar saída acessível
	em terminal, preservar configurações pessoais por padrão e atualizar
	documentação operacional.

## Governance
- Esta constituição é a referência normativa para especificações, planos,
	tarefas, revisão e implementação neste repositório.
- Emendas MUST incluir justificativa explícita, análise de impacto em templates
	e revisão por mantenedor.
- Política de versionamento desta constituição:
	- MAJOR: mudanças incompatíveis em princípios fundamentais.
	- MINOR: adição de princípios ou seções normativas.
	- PATCH: correções textuais e esclarecimentos sem mudança normativa.
- Revisões de conformidade MUST ocorrer na aprovação do plano e na revisão de
	pull request; exceções MUST ser registradas com justificativa e aprovação.

**Version**: 2.1.0 | **Ratified**: 2026-06-01 | **Last Amended**: 2026-06-01
