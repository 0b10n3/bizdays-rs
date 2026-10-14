set shell := ["bash", "-euo", "pipefail", "-c"]

# List the recipes
default:
    @just --list

# Install the Python environment (all groups) and show the Rust toolchain
setup:
    uv sync --all-groups
    rustup show

# Format Rust and Python code
fmt:
    cargo fmt --all
    uv run ruff format .

# Check formatting without changing files
fmt-check:
    cargo fmt --all --check
    uv run ruff format --check .

# Lint Rust (clippy, warnings are errors) and Python (ruff)
lint:
    cargo clippy --workspace --all-targets -- -D warnings
    uv run ruff check .

# Run Rust tests (e.g. `just test -p bizdays name`)
test *args:
    cargo test {{ args }}

# Run Python tests
test-py *args:
    uv run pytest {{ args }}

# Build the core crate docs, warnings are errors
doc:
    RUSTDOCFLAGS="-D warnings" cargo doc --no-deps -p bizdays

# Check licenses, advisories and sources with cargo-deny
deny:
    @if command -v cargo-deny >/dev/null; then cargo deny check; else echo "warning: cargo-deny not installed; skipping (CI runs it)"; fi

# Validate the holiday calendars in crates/bizdays/data
data-check:
    uv run python tools/data/validate_calendars.py

# Regenerate the oracle fixtures in crates/bizdays/tests/fixtures
fixtures:
    uv run python tools/oracle/generate_fixtures.py

# Regenerate fixtures and fail if any CSV changed
fixtures-check: fixtures
    git diff --exit-code -- 'crates/bizdays/tests/fixtures/*.csv'

# Generate docs/stylesheets/syntaxis.css from the Syntaxis design tokens
brand tokens="docs/brand/tokens.json":
    uv run python tools/brand/tokens_to_css.py {{ tokens }} docs/stylesheets/syntaxis.css

# Build the documentation site (strict)
docs:
    uv run mkdocs build --strict

# Serve the documentation site locally
docs-serve:
    uv run mkdocs serve

# Build the abi3 wheel with maturin
wheel:
    uv run maturin build --release -m py-bizdays/Cargo.toml

# Coverage of the core crate with cargo-llvm-cov
cov:
    @if command -v cargo-llvm-cov >/dev/null; then cargo llvm-cov -p bizdays; else echo "warning: cargo-llvm-cov not installed (cargo install --locked cargo-llvm-cov)"; fi

# Toggle agent implementation mode in the learner zone: on | off | status
modo-implementacao estado:
    #!/usr/bin/env bash
    set -euo pipefail
    flag="{{ justfile_directory() }}/.agent-implementation-mode"
    case "{{ estado }}" in
        on) touch "$flag"; echo "modo implementação LIGADO: agentes podem editar a zona do aprendiz" ;;
        off) rm -f "$flag"; echo "modo implementação DESLIGADO: zona do aprendiz protegida" ;;
        status) if [[ -e "$flag" ]]; then echo "ligado"; else echo "desligado"; fi ;;
        *) echo "uso: just modo-implementacao on|off|status" >&2; exit 2 ;;
    esac

# Create a Git Flow work branch from develop (e.g. `just branch feature e1-s03-date-civil`)
branch tipo descricao:
    #!/usr/bin/env bash
    set -euo pipefail
    case "{{ tipo }}" in
        feature|bugfix|chore|data|spike) ;;
        *) echo "tipo: feature, bugfix, chore, data ou spike" >&2; exit 2 ;;
    esac
    name="{{ tipo }}/{{ descricao }}"
    uv run python tools/git/flow.py branch "$name"
    git switch -c "$name" develop

# Start release/<pacote>-<versao> from origin/develop (one open release at a time)
release-start pacote versao:
    #!/usr/bin/env bash
    set -euo pipefail
    name="release/{{ pacote }}-{{ versao }}"
    uv run python tools/git/flow.py branch "$name"
    [[ -z "$(git status --porcelain)" ]] || { echo "working tree is not clean" >&2; exit 1; }
    git fetch origin
    open="$(git branch -a --list '*release/*')"
    [[ -z "$open" ]] || { echo "a release branch is already open:$open" >&2; exit 1; }
    git switch -c "$name" origin/develop

# Start hotfix/<pacote>-<versao> from origin/main
hotfix-start pacote versao:
    #!/usr/bin/env bash
    set -euo pipefail
    name="hotfix/{{ pacote }}-{{ versao }}"
    uv run python tools/git/flow.py branch "$name"
    [[ -z "$(git status --porcelain)" ]] || { echo "working tree is not clean" >&2; exit 1; }
    git fetch origin
    git switch -c "$name" origin/main

# Tag <pacote>-v<versao> and push it; the tag triggers release.yml (final: on main; -rc.N: on its release branch)
release-finish pacote versao:
    #!/usr/bin/env bash
    set -euo pipefail
    version="{{ versao }}"
    [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-rc\.[0-9]+)?$ ]] || { echo "version must be X.Y.Z or X.Y.Z-rc.N" >&2; exit 2; }
    base="${version%%-rc.*}"
    manifest="$(uv run python tools/git/flow.py version {{ pacote }})"
    [[ "$manifest" == "$base" ]] || { echo "manifest has $manifest, expected $base" >&2; exit 1; }
    branch="$(git branch --show-current)"
    if [[ "$version" == *-rc.* ]]; then
        [[ "$branch" == "release/{{ pacote }}-$base" ]] || { echo "rc tags go on release/{{ pacote }}-$base (current: $branch)" >&2; exit 1; }
    else
        [[ "$branch" == main || "$branch" == support/{{ pacote }}-* ]] || { echo "final tags go on main or support/* (current: $branch)" >&2; exit 1; }
    fi
    [[ -z "$(git status --porcelain)" ]] || { echo "working tree is not clean" >&2; exit 1; }
    git fetch origin
    [[ "$(git rev-parse HEAD)" == "$(git rev-parse "origin/$branch")" ]] || { echo "HEAD differs from origin/$branch: pull or push first" >&2; exit 1; }
    tag="{{ pacote }}-v$version"
    git tag -a "$tag" -m "{{ pacote }} $version"
    git push origin "$tag"

# Run everything CI runs
ci: fmt-check lint test doc test-py data-check fixtures-check docs deny
