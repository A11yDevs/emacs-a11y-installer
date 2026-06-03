# CI/CD e Publicação de Releases

Este documento centraliza o fluxo de build/publicação para contribuidores.

## Workflows

- `.github/workflows/release-installers.yml`: pipeline oficial de release.
- `.github/workflows/build-windows-exe.yml`: build manual ad-hoc de executável Windows.

## Build de executável Windows

### Via GitHub Actions

1. Abra a aba **Actions** no GitHub.
2. Execute o workflow **Build Windows Executable** manualmente (`workflow_dispatch`) ou publique uma tag `v*`.
3. Baixe o artefato `emacs-a11y-windows-x64` ao final do job.

### Via máquina local Windows

No PowerShell, dentro do repositório:

```powershell
./scripts/build-windows-exe.ps1 -Clean
```

Saída esperada:

- `dist/emacs-a11y.exe`

## Assets publicados por release

O workflow oficial publica os seguintes artefatos no GitHub Releases:

- `emacs-a11y-<tag>-windows-x64.zip`
- `emacs_a11y_installer-<versao>-py3-none-any.whl`
- `emacs_a11y_installer-<versao>.tar.gz`
- `SHA256SUMS.txt`

## Publicação no PyPI

A publicação no PyPI é automática para tags no formato `v*`, usando Trusted Publishing.

Pré-requisito:

- O projeto no PyPI deve ter este repositório/workflow cadastrado como Trusted Publisher.

## Como publicar nova versão

1. Garanta que a branch `main` esteja atualizada.
2. Crie e publique uma tag no formato `v*` (por exemplo `v0.2.0`).
3. Aguarde a execução do workflow `Release Installers`.
4. Valide no fim:
- presença dos assets esperados no GitHub Release;
- pacote publicado no PyPI.

## Observações operacionais

- A distribuição canônica é Python (`wheel` + `sdist`).
- O executável Windows é uma distribuição opcional para usuários finais.
- Para diagnósticos de falha de release, verifique primeiro os jobs:
- `Build Python package`
- `Build windows-x64`
- `Publish GitHub Release`
- `Publish package to PyPI`
