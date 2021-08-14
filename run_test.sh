export PYTHONPATH=$(pwd):${PYTHONPATH}

echo "Python Path: ${PYTHONPATH}"

pytest -vvv tests/
