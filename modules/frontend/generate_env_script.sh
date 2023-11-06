#!/bin/sh -eu

if [ -z "${PERSON_URL:-}" ]; then
  PERSON_URL=undefined
fi 

cat <<EOF
window.REACT_APP_PERSON_URL="$PERSON_URL";
EOF
