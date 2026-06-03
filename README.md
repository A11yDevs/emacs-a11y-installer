# emacs-a11y-installer

Instalador multiplataforma para o Emacs Acessível, com foco em acessibilidade
estrutural, operação por teclado e diagnósticos em modo somente leitura.

## Para que serve

O projeto ajuda você a validar o ambiente antes de instalar ou ajustar o Emacs
Acessível, reduzindo falhas e tornando o processo mais previsível.

Hoje, a principal funcionalidade disponível é o comando de diagnóstico
`doctor`, com saída textual acessível e saída JSON para automação/suporte.

## Instalação rápida

### Opção mais simples (PyPI)

#### pipx (recomendado)

```bash
pipx install emacs-a11y-installer
```

```powershell
pipx install emacs-a11y-installer
```

#### pip

```bash
python3 -m pip install --user --upgrade emacs-a11y-installer
```

```powershell
python -m pip install --user --upgrade emacs-a11y-installer
```

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

O instalador PowerShell usa `pipx` quando disponivel e cai para `pip --user`
como fallback.

Instalar uma versão especifica:

```bash
EMACS_A11Y_VERSION=0.1.2 curl -fsSL https://raw.githubusercontent.com/A11yDevs/emacs-a11y-installer/main/scripts/install-emacs-a11y.sh | bash
```

```powershell
$env:EMACS_A11Y_VERSION = "0.1.2"; iwr -useb https://raw.githubusercontent.com/A11yDevs/emacs-a11y-installer/main/scripts/install-emacs-a11y.ps1 | iex
```

### Opção recomendada para usuários técnicos (`pipx`)

```bash
pipx install emacs-a11y-installer
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
  `emacs-a11y.exe` (asset de release), com runtime Python embutido.

## Documentação

- Guia funcional do comando doctor: [docs/doctor-cli.md](docs/doctor-cli.md)
- Documentação para contribuidores: [docs/README.md](docs/README.md)
