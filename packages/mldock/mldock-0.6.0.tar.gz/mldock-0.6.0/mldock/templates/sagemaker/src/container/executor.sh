#!/usr/bin/env bash
script_name="$1"
shift
if [ "$script_name" = "train" ]; then
    python ./container/training/train.py $@
else
    python ./container/prediction/serve.py
fi
