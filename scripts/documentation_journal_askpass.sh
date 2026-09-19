#!/bin/sh
# Git requests this helper only for the fixed same-repository HTTPS fetch.
case "$1" in
  *Username*) printf '%s\n' 'x-access-token' ;;
  *Password*) [ -n "${GITHUB_TOKEN:-}" ] || exit 1; printf '%s\n' "$GITHUB_TOKEN" ;;
  *) exit 1 ;;
esac
