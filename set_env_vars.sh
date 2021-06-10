if [ -n "$1" ]; then
  echo "Setting env vars from this file $1"
  set -o allexport
  source $1
  set +o allexport
  echo "done"
else
  echo "Missing env vars file parameter"
fi