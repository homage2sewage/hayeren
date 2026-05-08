#!/usr/bin/env bash
set -euo pipefail

# Allowed identity tokens (case-insensitive substring match against names/emails/trailers).
ALLOWED='(homage2sewage|alexey)'

# Paths that look like caches / build artifacts / secrets / editor cruft.
# We block these from being committed even if .gitignore doesn't already.
BLOCK_PATTERNS=(
  '(^|/)\.?cache(s)?(/|$)'
  '(^|/)__pycache__(/|$)'
  '(^|/)node_modules(/|$)'
  '(^|/)\.venv(/|$)'
  '(^|/)venv(/|$)'
  '(^|/)\.tox(/|$)'
  '(^|/)\.pytest_cache(/|$)'
  '(^|/)\.mypy_cache(/|$)'
  '(^|/)\.ruff_cache(/|$)'
  '(^|/)\.next(/|$)'
  '(^|/)\.nuxt(/|$)'
  '(^|/)\.parcel-cache(/|$)'
  '(^|/)\.gradle(/|$)'
  '(^|/)\.idea(/|$)'
  '(^|/)dist(/|$)'
  '(^|/)build(/|$)'
  #'(^|/)out(/|$)'
  '(^|/)target(/|$)'
  '(^|/)\.scratch(/|$)'
  '\.pyc$'
  '\.pyo$'
  '\.class$'
  '\.o$'
  '\.so$'
  '\.log$'
  '\.tmp$'
  '\.swp$'
  '~$'
  '(^|/)\.DS_Store$'
  '(^|/)Thumbs\.db$'
  '(^|/)\.env($|\.)'
  '\.pem$'
  '\.key$'
  '(^|/)id_[rd]sa($|\.)'
  '(^|/)\.netrc$'
  '(^|/)\.aws(/|$)'
)
block_re="$(IFS='|'; echo "${BLOCK_PATTERNS[*]}")"

cd "$(git rev-parse --show-toplevel)"

scan_paths() {
  {
    git diff --name-only
    git diff --cached --name-only
    git ls-files --others --exclude-standard
  } | sort -u
}

check_blocked() {
  local label="$1"; shift
  local bad=()
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    if [[ "$f" =~ $block_re ]]; then
      bad+=("$f")
    fi
  done
  if (( ${#bad[@]} > 0 )); then
    echo "[block] $label — cache/ephemeral/secret-shaped paths detected:" >&2
    printf '  %s\n' "${bad[@]}" >&2
    echo "Add them to .gitignore or remove them, then re-run." >&2
    exit 1
  fi
}

scan_paths | check_blocked "pre-stage"

git add -A

git diff --cached --name-only | check_blocked "post-stage"

if git diff --cached --quiet; then
  echo "[info] nothing staged after add — no commit"
else
  msg="${1:-snapshot $(date +%Y-%m-%d_%H:%M:%S)}"
  git commit -m "$msg"
fi

upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
if [[ -z "$upstream" ]]; then
  echo "[error] no upstream tracking branch" >&2
  exit 1
fi
range="$upstream..HEAD"

problems=()

while IFS=$'\t' read -r sha an ae cn ce; do
  [[ -z "$sha" ]] && continue
  for v in "$an" "$ae" "$cn" "$ce"; do
    if ! [[ "${v,,}" =~ $ALLOWED ]]; then
      problems+=("$sha: identity '$v' not in allowlist")
    fi
  done
done < <(git log "$range" --format='%H%x09%an%x09%ae%x09%cn%x09%ce')

while IFS= read -r line; do
  if [[ "$line" =~ ^[[:space:]]*(Co-[Aa]uthored-[Bb]y|Signed-off-by|Reviewed-by|Helped-by|Acked-by)[[:space:]]*: ]]; then
    val="${line#*:}"
    if ! [[ "${val,,}" =~ $ALLOWED ]]; then
      problems+=("trailer not in allowlist: ${line## }")
    fi
  fi
done < <(git log "$range" --format='%B')

if (( ${#problems[@]} > 0 )); then
  echo "[block] identity check failed for commits in $range:" >&2
  printf '  %s\n' "${problems[@]}" >&2
  exit 1
fi

if git diff --quiet "$upstream"..HEAD -- 2>/dev/null && [[ -z "$(git log "$range" --oneline)" ]]; then
  echo "[info] nothing to push"
  exit 0
fi

git push
