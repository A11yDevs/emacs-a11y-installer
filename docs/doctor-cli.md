# Doctor CLI Design Notes

## Visao geral
A feature `emacs-a11y doctor` e o ponto de entrada de diagnostico pre-instalacao,
com saida textual acessivel e opcao de saida JSON para automacao e suporte.

## Casos de uso textuais

### UC-01 Executar diagnostico textual
- Ator principal: Pessoa usuaria.
- Objetivo: verificar prontidao do ambiente antes da instalacao.
- Pre-condicoes: comando instalado e executavel no ambiente atual.
- Fluxo principal:
  1. Pessoa usuaria executa `emacs-a11y doctor`.
  2. CLI coleta estado de ambiente em modo somente leitura.
  3. Orquestrador executa checks comuns e checks da plataforma.
  4. Sistema agrega resultados e gera resumo por severidade.
  5. Renderizador textual apresenta resultado linear e proximos passos.
- Fluxos alternativos:
  - A1: check inconclusivo de TTS retorna `UNKNOWN` com recomendacao de verificacao manual.
  - A2: erro interno de execucao retorna codigo 3 com mensagem de suporte.
- Pos-condicoes: relatorio textual exibido sem alterar o sistema.
- Criterios de aceitacao: saida acessivel, sem escrita em disco, severidade clara e proxima acao objetiva.

### UC-02 Executar diagnostico JSON
- Ator principal: Pessoa mantenedora/suporte.
- Objetivo: consumir diagnostico estruturado para automacao e suporte remoto.
- Pre-condicoes: comando disponivel e flag `--json` suportada.
- Fluxo principal:
  1. Pessoa mantenedora executa `emacs-a11y doctor --json`.
  2. Orquestrador executa os mesmos checks do modo textual.
  3. Renderizador JSON serializa `DiagnosticReport` conforme schema.
  4. Processo finaliza com exit code correspondente.
- Fluxos alternativos:
  - A1: schema interno invalido (erro de programacao) resulta em exit code 3.
- Pos-condicoes: payload JSON valido para contrato da feature.
- Criterios de aceitacao: paridade semantica com modo textual e conformidade de schema.

### UC-03 Interpretar proximos passos
- Ator principal: Pessoa usuaria.
- Objetivo: entender o que fazer apos identificar falhas ou avisos.
- Pre-condicoes: diagnostico executado com ao menos um resultado `FAIL` ou `UNKNOWN`.
- Fluxo principal:
  1. Pessoa usuaria revisa secao de proximos passos.
  2. Sistema apresenta instrucoes por check afetado.
  3. Pessoa usuaria toma acao externa ao comando.
- Fluxos alternativos:
  - A1: multiplos checks geram passos redundantes; agregador remove duplicatas.
- Pos-condicoes: pessoa usuaria tem roteiro de correcao sem alteracoes automaticas.
- Criterios de aceitacao: instrucoes concretas, curtas e mapeadas aos checks falhos.

## Artefatos PlantUML
- `docs/plantuml/doctor-use-cases.puml`
- `docs/plantuml/doctor-sequence-text.puml`
- `docs/plantuml/doctor-sequence-json.puml`
- `docs/plantuml/doctor-architecture.puml`
- `docs/plantuml/doctor-functional-flow.puml`
