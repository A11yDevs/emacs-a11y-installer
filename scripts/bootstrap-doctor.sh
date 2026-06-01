#!/usr/bin/env sh
set -eu

# Wrapper only: no diagnostic business rules here.
exec emacs-a11y doctor "$@"
