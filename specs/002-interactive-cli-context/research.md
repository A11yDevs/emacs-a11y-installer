# Research: Interactive CLI Context Mode

## Decision 1: Loop interativo dirigido por árvore de contextos
- Decision: Implementar um loop REPL simples baseado em pilha de contextos (`root` -> `doctor`) com comandos globais (`help`, `back`, `exit`) resolvidos antes dos comandos locais.
- Rationale: Mantém navegação previsível, reduz ambiguidade e facilita acessibilidade por leitor de tela com prompt explícito por contexto.
- Alternatives considered: Fluxo de menus numerados fixos (rejeitado por baixa flexibilidade); shell externo com parser complexo (rejeitado por custo e acoplamento desnecessário).

## Decision 2: Reuso de Typer sem duplicação de regra de negócio
- Decision: Encapsular execução de diagnóstico em funções de aplicação reutilizáveis e reutilizar as mesmas funções tanto no caminho Typer não interativo quanto no caminho interativo.
- Rationale: Garante paridade funcional para `emacs-a11y doctor` e `emacs-a11y doctor --json`, reduz regressões e evita drift de comportamento.
- Alternatives considered: Reinvocar Typer internamente via parsing de strings (rejeitado por complexidade e mensagens de erro menos controláveis); duplicar handlers (rejeitado por risco de divergência).

## Decision 3: Modelo de dados explícito para contexto/comando/resultado
- Decision: Definir modelos de domínio para `CommandContext`, `CommandDefinition`, `CommandResult` e `NavigationAction`.
- Rationale: Tipagem explícita permite testes unitários diretos de roteamento, navegação e mensagens sem depender de I/O de terminal.
- Alternatives considered: Estruturas ad-hoc em dicionários (rejeitado por baixa clareza e manutenção difícil).

## Decision 4: Estratégia de acessibilidade textual linear
- Decision: Padronizar saída com blocos curtos e previsíveis: cabeçalho de contexto, lista de comandos (`nome - descrição`), mensagens de erro objetivas e sugestões de próximo passo.
- Rationale: Atende constituição (acessibilidade estrutural), evita dependência de cor e melhora compreensão por sintetizadores de voz.
- Alternatives considered: Tabelas com formatação rica/caixas visuais (rejeitado por leitura menos linear em screen readers).

## Decision 5: Tratamento de comandos inválidos com sugestão contextual
- Decision: Para entrada inválida, retornar mensagem `Comando inválido no contexto X` + `Use help` + lista curta de sugestões por similaridade textual e comandos válidos do contexto.
- Rationale: Diminui atrito de aprendizagem e mantém fluxo de exploração por teclado.
- Alternatives considered: Mensagem genérica sem sugestão (rejeitado por baixa usabilidade).

## Decision 6: Cobertura de testes em duas camadas
- Decision: Criar testes unitários para parsing, resolução e navegação; e testes de integração para sessão interativa com sequência de entradas e validação de saídas.
- Rationale: Isola regras de negócio do transporte (stdin/stdout) e valida experiência real de uso.
- Alternatives considered: Apenas integração E2E (rejeitado por baixa granularidade de diagnóstico de falhas).

## Decision 7: Escopo de documentação e diagramas
- Decision: Atualizar documentação operacional e PlantUML no mesmo change set da implementação: fluxo de sequência interativo e arquitetura da árvore de comandos.
- Rationale: Atende constituição (documentação como parte da entrega) e reduz dívida documental.
- Alternatives considered: Atualização posterior (rejeitado por risco de descompasso com comportamento implementado).

## Resolved Clarifications
- Linguagem/versão: Python 3.11+.
- Framework CLI: Typer existente, preservado.
- Persistência: não aplicável; sessão interativa é efêmera.
- Compatibilidade: modo não interativo (`doctor`, `doctor --json`) permanece obrigatório.
- Escopo funcional: somente contexto raiz e contexto `doctor`; contextos `install`, `update` e `remove` apenas modelados como extensões futuras.
