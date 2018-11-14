
VENV=.env
test -d ${VENV} || virtualenv ${VENV}

. ${VENV}/bin/activate
pip install -r requirements.txt
pip install -r dev-requirements.txt

export PYTHONPATH=$PWD
