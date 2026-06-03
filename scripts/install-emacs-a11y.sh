#!/usr/bin/env sh
set -eu

PACKAGE_NAME="emacs-a11y-installer"
VERSION="${EMACS_A11Y_VERSION:-}"

fail() {
  printf '%s\n' "ERROR: $1" >&2
  exit 1
}

resolve_python() {
  if command -v python3 >/dev/null 2>&1; then
    printf '%s\n' python3
    return
  fi

  if command -v python >/dev/null 2>&1; then
    printf '%s\n' python
    return
  fi

  fail "Python 3.11+ nao encontrado. Instale Python ou pipx para continuar."
}

normalize_version() {
  printf '%s\n' "$1" | sed 's/^v//'
}

PACKAGE_SPEC="$PACKAGE_NAME"
if [ -n "$VERSION" ]; then
  PACKAGE_SPEC="$PACKAGE_NAME==$(normalize_version "$VERSION")"
fi

if command -v pipx >/dev/null 2>&1; then
  pipx install --force "$PACKAGE_SPEC" || fail "Falha ao instalar via pipx."
  printf '%s\n' "Instalacao concluida via pipx. Execute: emacs-a11y --help"
  exit 0
fi

PYTHON_BIN="$(resolve_python)"
"$PYTHON_BIN" -m pip install --user --upgrade "$PACKAGE_SPEC" || fail "Falha ao instalar via pip."

USER_BASE="$($PYTHON_BIN -c 'import site; print(site.USER_BASE)')"
USER_BIN_DIR="${USER_BASE}/bin"

printf '%s\n' "Instalacao concluida via pip: ${PACKAGE_SPEC}"

case ":$PATH:" in
  *":$USER_BIN_DIR:"*)
    printf '%s\n' "PATH OK. Execute: emacs-a11y --help"
    ;;
  *)
    printf '%s\n' "Adicione ao PATH e abra um novo terminal:"
    printf '%s\n' "  export PATH=\"${USER_BIN_DIR}:\$PATH\""
    ;;
esac
