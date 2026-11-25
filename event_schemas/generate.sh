#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

command -v buf >/dev/null

buf lint

buf generate
