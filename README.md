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

### Gerar executável para Windows (.exe)

#### Opção recomendada: GitHub Actions

Este repositório inclui o workflow `.github/workflows/build-windows-exe.yml`.

Como usar:

1. Abra a aba **Actions** no GitHub.
2. Execute o workflow **Build Windows Executable** manualmente (`workflow_dispatch`) ou publique uma tag `v*`.
3. Baixe o artefato `emacs-a11y-windows-x64` ao final do job.

#### Opção local (em máquina Windows)

No PowerShell, dentro do repositório:

```powershell
./scripts/build-windows-exe.ps1 -Clean
```

Saída esperada:

- `dist/emacs-a11y.exe`

### CI/CD de releases

Este repositório inclui o workflow `.github/workflows/release-installers.yml`
que publica dois assets finais por release:

- Windows (`windows-x64`): executável standalone em `.zip`
- Unix bundle (`linux + macOS`): pacote único em `.tar.gz` contendo binários
  separados por sistema

Como publicar uma release:

1. Crie e publique uma tag no formato `v*` (ex.: `v0.2.0`).
2. O workflow compila binários com PyInstaller para Windows, Linux e macOS.
3. O pipeline publica:
  - `emacs-a11y-<tag>-windows-x64.zip`
  - `emacs-a11y-<tag>-unix-bundle.tar.gz` (com `linux` + `macos`)
4. A release também inclui o arquivo `SHA256SUMS.txt` para verificação.

Observação:

- O workflow `build-windows-exe.yml` continua disponível para builds manuais
  ad-hoc apenas de Windows.

## Documentação

- Guia funcional do comando doctor: [docs/doctor-cli.md](docs/doctor-cli.md)
- Documentação para contribuidores: [docs/README.md](docs/README.md)
