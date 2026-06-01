# Doctor CLI Design Notes

## Visao geral
O comando `emacs-a11y doctor` e o primeiro gate do instalador. Ele coleta sinais
do ambiente em modo somente leitura e apresenta um relatorio acessivel com:

- seções lineares para leitores de tela;
- severidades explicitas (`CRITICAL`, `WARNING`, `INFO`);
- proximos passos acionaveis;
- saida JSON opcional com o mesmo significado da saida textual.

## Comandos disponiveis

- `emacs-a11y` (inicia modo interativo contextual)
- `emacs-a11y doctor`
- `emacs-a11y doctor --json`
- `emacs-a11y --help`
- `emacs-a11y doctor --help`

## Modo interativo contextual

Quando executada sem argumentos, a CLI entra no prompt interativo raiz.

- prompt raiz: `emacs-a11y>`
- prompt de diagnostico: `emacs-a11y doctor>`
- comandos globais em qualquer contexto: `help`, `back`, `exit`

### Ajuda contextual (raiz)

Formato linear, sem dependencia de cor:

- `help - ajuda de comandos`
- `doctor - Executa diagnóstico de ambiente em modo estritamente somente leitura.`
- `back - sair`
- `exit - sair`

### Comandos do contexto doctor

- `run - executa diagnóstico textual`
- `json - executa diagnóstico em JSON`
- `explain - explica checks de diagnóstico`
- `help - ajuda de comandos`
- `back - sair`
- `exit - sair`

### Tratamento de comandos invalidos

- Mensagem textual curta e linear.
- Orientacao explicita para executar `help`.
- Sugestoes de comandos proximos (quando aplicavel).

## Exemplos reais de uso

### Instalacao local (desenvolvimento)
```bash
python -m pip install -e .
```

### Instalacao recomendada para usuarios tecnicos
```bash
pipx install .
```

### Diagnostico textual acessivel
```bash
emacs-a11y doctor
```

### Diagnostico estruturado para automacao/suporte
```bash
emacs-a11y doctor --json
```

## Matriz de verificacao por plataforma

| Check | Windows | macOS | Linux |
|------|---------|-------|-------|
| SO e arquitetura | Yes | Yes | Yes |
| Emacs e versao | Yes | Yes | Yes |
| Git (nao bloqueante) | Yes | Yes | Yes |
| Python (bloqueante para distribuicao canonica) | Yes | Yes | Yes |
| Perfil Emacs Acessivel | Yes | Yes | Yes |
| Configuracao pessoal do Emacs | Yes | Yes | Yes |
| Sinais iniciais de TTS | Yes | Yes | Yes |
| Sinais de Emacspeak | Yes | Yes | Yes |

## Regras de seguranca e nao destrutividade

- Nao cria diretorios.
- Nao modifica arquivos.
- Nao baixa binarios.
- Nao instala dependencias.
- Nao altera PATH.
- Nao solicita privilegios administrativos.
- O modo interativo `doctor` continua estritamente somente leitura.

## Casos de uso textuais

### UC-01 Executar diagnostico textual
- Ator principal: Pessoa usuaria.
- Objetivo: verificar prontidao do ambiente antes da instalacao.
- Fluxo principal:
  1. Pessoa usuaria executa `emacs-a11y doctor`.
  2. Orquestrador executa checks comuns + adaptador de plataforma.
  3. Renderizador textual exibe `Resumo`, `Criticos`, `Avisos`, `Info`, `Proximos passos`.
- Pos-condicao: relatorio exibido sem alterar sistema.

### UC-00 Navegar no menu interativo contextual
- Ator principal: Pessoa usuaria.
- Objetivo: explorar e executar comandos por contexto, usando somente teclado.
- Fluxo principal:
  1. Pessoa usuaria executa `emacs-a11y`.
  2. CLI entra em `emacs-a11y>` e exibe ajuda automatica.
  3. Pessoa usuaria executa `doctor` para entrar em `emacs-a11y doctor>`.
  4. Pessoa usuaria executa `run`, `json` ou `explain`.
  5. Pessoa usuaria executa `back` para retornar ou `exit` para encerrar.
- Pos-condicao: sessao encerrada sem alteracoes destrutivas no sistema.

### UC-02 Executar diagnostico JSON
- Ator principal: Pessoa mantenedora/suporte.
- Objetivo: consumir diagnostico estruturado.
- Fluxo principal:
  1. Pessoa mantenedora executa `emacs-a11y doctor --json`.
  2. Mesma avaliacao do fluxo textual.
  3. JSON final segue schema oficial.

### UC-03 Interpretar proximos passos
- Ator principal: Pessoa usuaria.
- Objetivo: agir sobre falhas/avisos sem operacoes automaticas destrutivas.

## Roadmap de superficie de comandos (alinhamento constitucional)

- Coberto nesta feature: `doctor` e suporte de ajuda CLI.
- Planejado para features seguintes: `install`, `update`, `remove` com contratos,
  testes e garantias de reversibilidade dedicadas.

## Paridade entre canais de distribuicao

- Canal canonico: pacote Python instalavel localmente e via `pipx`.
- Canal opcional futuro: executavel standalone.
- Criterio de paridade: mesmo conjunto de checks, severidades, proximos passos
  e mapeamento de codigos de saida para cenarios equivalentes.

## Artefatos PlantUML
- `docs/plantuml/doctor-use-cases.puml`
- `docs/plantuml/doctor-sequence-text.puml`
- `docs/plantuml/doctor-sequence-json.puml`
- `docs/plantuml/doctor-architecture.puml`
- `docs/plantuml/doctor-functional-flow.puml`
