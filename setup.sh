#!/bin/bash

VIRTUAL_ENV="venv"

if [ ! -d $VIRTUAL_ENV ]; then
    virtualenv venv
fi

venv/bin/pip install -r requirements.txt

if [ ! -d logs ]; then
    mkdir logs
fi

echo ""
echo ""
echo "##########################################################################"
echo "##########################################################################"
echo "You should now run \"source venv/bin/activate\" to setup your python path."
echo "##########################################################################"
echo "##########################################################################"
