#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -d $DIR/venv ]; then
    virtualenv "$DIR/venv"
    echo "export PYTHONPATH=$DIR" >> $DIR/venv/bin/activate
fi

pip install -r requirements.txt
