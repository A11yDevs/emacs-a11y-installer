# Documentação para Contribuidores

Este guia é voltado para quem deseja desenvolver, testar e evoluir o
emacs-a11y-installer.

## Visão de arquitetura

- Código-fonte principal: [src/emacs_a11y](../src/emacs_a11y)
- Testes: [tests](../tests)
- Especificações e planejamento: [specs](../specs)
- Documentação funcional do doctor: [docs/doctor-cli.md](docs/doctor-cli.md)
- Diagramas PlantUML: [docs/plantuml](docs/plantuml)

## Requisitos de ambiente

- Python 3.11+
- pip (ou pipx para testes de distribuição)

## Setup de desenvolvimento

1. Instale em modo editável:

```bash
python -m pip install -e .
```

2. (Opcional) Instale ferramentas de teste/lint, se ainda não estiverem no ambiente:

```bash
python -m pip install pytest jsonschema ruff
```

## Executar testes

Rodar suíte completa:

```bash
python -m pytest -q
```

Rodar apenas uma área (exemplo):

```bash
python -m pytest -q tests/integration
```

## Fluxo de contribuição sugerido

1. Crie uma branch de feature a partir de main.
2. Atualize/adicione especificação em [specs](../specs) quando a mudança for não trivial.
3. Implemente com foco em:
- acessibilidade textual linear;
- não destrutividade;
- compatibilidade de fluxo não interativo existente.
4. Atualize documentação no mesmo change set.
5. Execute testes antes de abrir PR.

## Convenções importantes do projeto

- CLI é a interface primária.
- Diagnóstico (`doctor`) deve permanecer somente leitura.
- Evite duplicar regra de negócio entre caminhos interativo e não interativo.
- Scripts auxiliares em [scripts](../scripts) devem ser bootstrap/automação, não núcleo de negócio.

## Atualização de documentação

Ao mudar fluxo de CLI, atualize também:

- [README.md](../README.md) (visão para usuário final)
- [docs/doctor-cli.md](docs/doctor-cli.md)
- Diagramas em [docs/plantuml](docs/plantuml)
- Artefatos de especificação relevantes em [specs](../specs)

## Pull Request

No PR, inclua:

- resumo da mudança;
- impacto em acessibilidade;
- confirmação de não destrutividade;
- evidência de testes executados.
