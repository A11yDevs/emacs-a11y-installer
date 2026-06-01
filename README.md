# emacs-a11y-installer

Instalador multiplataforma para o Emacs Acessível, com foco em acessibilidade
estrutural, operação por teclado e diagnósticos em modo somente leitura.

## Para que serve

O projeto ajuda você a validar o ambiente antes de instalar ou ajustar o Emacs
Acessível, reduzindo falhas e tornando o processo mais previsível.

Hoje, a principal funcionalidade disponível é o comando de diagnóstico
`doctor`, com saída textual acessível e saída JSON para automação/suporte.

## Instalação rápida

### Opção recomendada para usuários técnicos (`pipx`)

```bash
pipx install .
```

### Opção para desenvolvimento local

```bash
python -m pip install -e .
```

## Uso básico

### Modo interativo contextual

```bash
emacs-a11y
```

Ao abrir sem argumentos, a CLI entra no contexto raiz `emacs-a11y>` e mostra a
ajuda do contexto automaticamente.

### Diagnóstico textual (somente leitura)

```bash
emacs-a11y doctor
```

### Diagnóstico JSON (somente leitura)

```bash
emacs-a11y doctor --json
```

## Segurança e não destrutividade

No escopo atual de diagnóstico, a ferramenta:

- não instala pacotes;
- não altera arquivos de configuração;
- não baixa binários;
- não altera PATH;
- não solicita privilégios administrativos.

## Estratégia de distribuição

- Formato canônico: pacote Python multiplataforma.
- Instalação preferencial para usuários técnicos: `pipx`.
- Distribuição opcional para usuários finais: executáveis autônomos gerados do
  mesmo código-fonte (por exemplo, `emacs-a11y.exe`), com runtime Python embutido.

## Documentação

- Guia funcional do comando doctor: [docs/doctor-cli.md](docs/doctor-cli.md)
- Documentação para contribuidores: [docs/README.md](docs/README.md)
