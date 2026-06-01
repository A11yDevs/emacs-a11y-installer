# Research: Doctor CLI Acessivel

## Decision 1: CLI library = Typer
- Decision: Use Typer for `emacs-a11y doctor` and `emacs-a11y doctor --json`.
- Rationale: Typer oferece API simples, tipada e previsivel para subcomandos, reduz boilerplate e facilita manutencao da CLI acessivel.
- Alternatives considered:
  - Click: estavel e maduro, mas com mais codigo manual para tipagem e ajuda estruturada.

## Decision 2: Arquitetura = composicional com OO leve
- Decision: Modelagem funcional/composicional baseada em checks independentes, com OO leve para entidades de dominio.
- Rationale: Checks puros e independentes sao mais testaveis, favorecem isolamento por plataforma e reduzem acoplamento.
- Alternatives considered:
  - Hierarquia OO pesada por tipo de check: maior complexidade e custo de evolucao para baixo ganho.

## Decision 3: Fonte de verdade unica para saidas
- Decision: Construir um `DiagnosticReport` unico e renderizar para texto ou JSON em camadas separadas.
- Rationale: Garante paridade semantica entre `doctor` e `doctor --json`.
- Alternatives considered:
  - Geração de texto e JSON por caminhos independentes: risco alto de divergencia funcional.

## Decision 4: Deteccao de ambiente com biblioteca padrao
- Decision: Priorizar `platform`, `pathlib`, `shutil`, `subprocess`, `json`, `dataclasses`, `typing`, `enum`.
- Rationale: Menos dependencias, melhor portabilidade e manutencao do pacote canônico.
- Alternatives considered:
  - Bibliotecas externas para detecao de sistema: ganho limitado para a fase inicial.

## Decision 5: Contrato JSON versionado
- Decision: Definir schema JSON explicito para o relatorio de diagnostico.
- Rationale: Estabiliza integracao de suporte/automacao e facilita testes de contrato.
- Alternatives considered:
  - JSON sem schema formal: maior risco de regressao silenciosa.

## Decision 6: Saida textual acessivel e linear
- Decision: Ordem fixa: resumo -> criticos -> avisos -> info -> proximos passos.
- Rationale: Leitores de tela e fluxo por teclado se beneficiam de estrutura previsivel.
- Alternatives considered:
  - Tabelas complexas ou organizacao visual baseada em cor: piora acessibilidade.

## Decision 7: So leitura estrita
- Decision: Nenhum check cria/modifica arquivos, instala pacotes, altera PATH, baixa binarios ou solicita privilegios.
- Rationale: Conformidade com doctor-first, nao-destrutivo e seguranca da constituicao.
- Alternatives considered:
  - Auto-correcao no comando doctor: conflita com escopo de diagnostico e seguranca.

## Decision 8: Distribuicao em camadas
- Decision: Pacote Python multiplataforma como formato canonico; `pipx` como instalacao preferencial; executaveis autonomos futuros derivados do mesmo codigo.
- Rationale: Preserva base tecnica unica e amplia acesso para publico final sem Python.
- Alternatives considered:
  - Priorizar executavel primeiro: aumenta custo de empacotamento antes de estabilizar o nucleo.
