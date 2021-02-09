#!/usr/bin/env bash

set -o errtrace
set -o nounset
set -o errexit
set -o pipefail

# shellcheck disable=SC2034
{
  declare -r FATAL='\033[0;31m'
  declare -r ERROR='\033[0;31m'
  declare -r WARNING='\033[0;33m'
  declare -r INFO='\033[0m'
  declare -r DEFAULT='\033[0m'
}

function feedback() {
  color="${1:-DEFAULT}"
  case "${1}" in
    FATAL)
      >&2 echo -e "${!color}${1}:  ${2}${DEFAULT}"
      exit 1
      ;;
    ERROR)
      >&2 echo -e "${!color}${1}:  ${2}${DEFAULT}"
      exit 1
      ;;
    WARNING)
      >&2 echo -e "${!color}${1}:  ${2}${DEFAULT}"
      ;;
    *)
      echo -e "${!color}${1}:  ${2}${DEFAULT}"
      ;;
  esac
}

cd /opt/pysaml2/example
pipenv install
pipenv run ./all.sh start
