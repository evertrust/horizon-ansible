set -e
set -o pipefail
set -u

function main()
{
  readonly template="$1"; shift
  readonly content="$(cat "$template")"

  eval "echo \"$content\""
}

main "$@"