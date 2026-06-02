#!/usr/bin/env sh
set -eu

REPO="A11yDevs/emacs-a11y-installer"
INSTALL_DIR="${EMACS_A11Y_INSTALL_DIR:-$HOME/.local/bin}"
VERSION="${EMACS_A11Y_VERSION:-}"

cleanup() {
  if [ -n "${TMP_DIR:-}" ] && [ -d "${TMP_DIR}" ]; then
    rm -rf "${TMP_DIR}"
  fi
}

fail() {
  printf '%s\n' "ERROR: $1" >&2
  exit 1
}

fetch_latest_tag() {
  API_URL="https://api.github.com/repos/${REPO}/releases/latest"

  if command -v curl >/dev/null 2>&1; then
    RESPONSE="$(curl -fsSL "$API_URL")" || fail "Nao foi possivel consultar releases no GitHub."
  elif command -v wget >/dev/null 2>&1; then
    RESPONSE="$(wget -qO- "$API_URL")" || fail "Nao foi possivel consultar releases no GitHub."
  else
    fail "Instale curl ou wget para continuar."
  fi

  TAG="$(printf '%s\n' "$RESPONSE" | sed -n 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
  [ -n "$TAG" ] || fail "Nao foi possivel detectar tag da release mais recente."
  printf '%s\n' "$TAG"
}

download_file() {
  URL="$1"
  OUTPUT="$2"

  if command -v curl >/dev/null 2>&1; then
    curl -fL "$URL" -o "$OUTPUT" || fail "Falha ao baixar asset: $URL"
  elif command -v wget >/dev/null 2>&1; then
    wget -O "$OUTPUT" "$URL" || fail "Falha ao baixar asset: $URL"
  else
    fail "Instale curl ou wget para continuar."
  fi
}

OS_NAME="$(uname -s)"
case "$OS_NAME" in
  Darwin) PLATFORM_DIR="macos" ;;
  Linux) PLATFORM_DIR="linux" ;;
  *) fail "Sistema nao suportado por este instalador: $OS_NAME" ;;
esac

TAG="$VERSION"
if [ -z "$TAG" ]; then
  TAG="$(fetch_latest_tag)"
fi

ASSET_NAME="emacs-a11y-${TAG}-unix-bundle.tar.gz"
ASSET_URL="https://github.com/${REPO}/releases/download/${TAG}/${ASSET_NAME}"

TMP_DIR="$(mktemp -d 2>/dev/null || mktemp -d -t emacs-a11y-install)"
trap cleanup EXIT INT TERM

ARCHIVE_PATH="${TMP_DIR}/${ASSET_NAME}"
download_file "$ASSET_URL" "$ARCHIVE_PATH"

tar -xzf "$ARCHIVE_PATH" -C "$TMP_DIR" || fail "Falha ao extrair pacote unix."

SOURCE_BIN="${TMP_DIR}/${PLATFORM_DIR}/emacs-a11y"
[ -f "$SOURCE_BIN" ] || fail "Binario nao encontrado no pacote para ${PLATFORM_DIR}."

mkdir -p "$INSTALL_DIR"

if command -v install >/dev/null 2>&1; then
  install -m 0755 "$SOURCE_BIN" "$INSTALL_DIR/emacs-a11y"
else
  cp "$SOURCE_BIN" "$INSTALL_DIR/emacs-a11y"
  chmod 0755 "$INSTALL_DIR/emacs-a11y"
fi

printf '%s\n' "Instalacao concluida: ${INSTALL_DIR}/emacs-a11y"

case ":$PATH:" in
  *":$INSTALL_DIR:"*)
    printf '%s\n' "PATH OK. Execute: emacs-a11y --help"
    ;;
  *)
    printf '%s\n' "Adicione ao PATH e abra um novo terminal:"
    printf '%s\n' "  export PATH=\"${INSTALL_DIR}:\$PATH\""
    ;;
esac
