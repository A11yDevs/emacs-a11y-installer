# emacs-a11y-installer

Instalador multiplataforma para o Emacs Acessível, com foco em acessibilidade
estrutural, operação por teclado e diagnósticos em modo somente leitura.

## Para que serve

O projeto ajuda você a validar o ambiente antes de instalar ou ajustar o Emacs
Acessível, reduzindo falhas e tornando o processo mais previsível.

Hoje, a principal funcionalidade disponível é o comando de diagnóstico
`doctor`, com saída textual acessível e saída JSON para automação/suporte.

## Instalação rápida

### One-liner para usuários finais

#### Unix (bash)

```bash
curl -fsSL https://raw.githubusercontent.com/A11yDevs/emacs-a11y-installer/main/scripts/install-emacs-a11y.sh | bash
```

O instalador Unix usa `pipx` quando disponivel e cai para `pip --user` como
fallback. Funciona em Linux e macOS com Python 3.11+.

#### Windows (PowerShell)

```powershell
iwr -useb https://raw.githubusercontent.com/A11yDevs/emacs-a11y-installer/main/scripts/install-emacs-a11y.ps1 | iex
```

Instalar uma versão especifica:

```bash
EMACS_A11Y_VERSION=0.1.2 curl -fsSL https://raw.githubusercontent.com/A11yDevs/emacs-a11y-installer/main/scripts/install-emacs-a11y.sh | bash
```

```powershell
$env:EMACS_A11Y_VERSION = "v0.1.1"; iwr -useb https://raw.githubusercontent.com/A11yDevs/emacs-a11y-installer/main/scripts/install-emacs-a11y.ps1 | iex
```

### Opção recomendada para usuários técnicos (`pipx`)

```bash
pipx install emacs-a11y-installer
```

Ou, antes de publicar no PyPI, diretamente do GitHub:

```bash
pipx install "git+https://github.com/A11yDevs/emacs-a11y-installer.git"
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
- Instalação preferencial para usuários técnicos: `pipx` ou `pip`.
- Distribuição opcional para usuários finais no Windows: executável autônomo
  `emacs-a11y.exe`, com runtime Python embutido.

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
que publica assets finais por release e envia o pacote Python automaticamente ao
PyPI:

- Windows (`windows-x64`): executável standalone em `.zip`
- Wheel Python portável (`py3-none-any`)
- Sdist (`tar.gz`) com código-fonte

Como publicar uma release:

1. Crie e publique uma tag no formato `v*` (ex.: `v0.2.0`).
2. O workflow compila o executável Windows e gera `wheel` + `sdist` do pacote Python.
3. O pipeline publica:
  - `emacs-a11y-<tag>-windows-x64.zip`
  - `emacs_a11y_installer-<versao>-py3-none-any.whl`
  - `emacs_a11y_installer-<versao>.tar.gz`
4. A release também inclui o arquivo `SHA256SUMS.txt` para verificação.
5. Em tags `v*`, o workflow também publica o pacote Python no PyPI via Trusted Publishing.

Observação:

- O workflow `build-windows-exe.yml` continua disponível para builds manuais
  ad-hoc apenas de Windows.
- Para a automação do PyPI funcionar, é preciso cadastrar este repositório e o
  workflow como Trusted Publisher no projeto do PyPI.

## Documentação

- Guia funcional do comando doctor: [docs/doctor-cli.md](docs/doctor-cli.md)
- Documentação para contribuidores: [docs/README.md](docs/README.md)
