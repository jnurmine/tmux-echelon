#!/bin/bash
. ~/bin/echelon-py/bin/activate

if [[ -z "${ECHELON_LOG}" ]]; then
    # no logging
    ECHELON_LOG=/dev/null
fi

tee $ECHELON_LOG | python ~/bin/echelon.py $1 $2 $3
