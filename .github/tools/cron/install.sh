#!/bin/bash

set -e

echo "Upgrading pip and setuptools"
pip install --upgrade pip setuptools

echo "Installing numpy, scipy and cython"
dev_url=https://7933911d6844c6c53a7d-47bd50c35cd79bd838daf386af554a83.ssl.cf2.rackcdn.com
pip install --pre --upgrade --timeout=60 -f $dev_url numpy scipy cython

echo "Installing scikit-learn"
dev_url=https://pypi.anaconda.org/scipy-wheels-nightly/simple
pip install --pre --upgrade --timeout=60 -i $dev_url scikit-learn

echo "Installing pytest"
pip install pytest==4.6.4 pytest-cov

echo "Installing codecov"
pip install --upgrade codecov

python --version
python -c "import numpy; print('NumPy {0}'.format(numpy.__version__))"
python -c "import scipy; print('SciPy {0}'.format(scipy.__version__))"
python -c "import cython; print('Cython {0}'.format(cython.__version__))"
python -c "import sklearn; print('Scikit-learn {0}'.format(sklearn.__version__))"

python setup.py develop
