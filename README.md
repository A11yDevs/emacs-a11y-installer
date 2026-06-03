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

Se você ainda não tem `pipx`, instale uma vez:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

Abra um novo terminal após `ensurepath`.

```bash
pipx install emacs-a11y-installer
```

```powershell
pipx install emacs-a11y-installer
```

#### pip (não recomendado para usuário final)

A instalação via `pip` funciona, mas o executável `emacs-a11y` pode não ficar no `PATH` automaticamente. Nesses casos, é necessário ajustar o `PATH` manualmente.

```bash
python3 -m pip install --user --upgrade emacs-a11y-installer
```

```powershell
python -m pip install --user --upgrade emacs-a11y-installer
```

Passo a passo para usar `pip` no macOS/Linux:

1. Instale o pacote:

```bash
python3 -m pip install --user --upgrade emacs-a11y-installer
```

2. Adicione o diretório de scripts ao `PATH`:

```bash
echo 'export PATH="$HOME/Library/Python/3.11/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

3. Valide:

```bash
emacs-a11y --help
```

Passo a passo para usar `pip` no Windows (PowerShell):

1. Instale o pacote:

```powershell
python -m pip install --user --upgrade emacs-a11y-installer
```

2. Descubra o diretório de scripts do usuário:

```powershell
python -c "import site; print(site.USER_BASE)"
```

3. Adicione `<USER_BASE>\\Scripts` ao `Path` de usuário e abra novo terminal.

4. Valide:

```powershell
emacs-a11y --help
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
(iwr -useb https://raw.githubusercontent.com/A11yDevs/emacs-a11y-installer/main/scripts/install-emacs-a11y.ps1).Content | iex
```

O instalador PowerShell usa `pipx` quando disponivel e cai para `pip --user`
como fallback.

Instalar uma versão especifica:

```bash
EMACS_A11Y_VERSION=0.1.2 curl -fsSL https://raw.githubusercontent.com/A11yDevs/emacs-a11y-installer/main/scripts/install-emacs-a11y.sh | bash
```

```powershell
$env:EMACS_A11Y_VERSION = "0.1.2"; (iwr -useb https://raw.githubusercontent.com/A11yDevs/emacs-a11y-installer/main/scripts/install-emacs-a11y.ps1).Content | iex
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
