[![PyPI version](https://badge.fury.io/py/lagmat.svg)](https://badge.fury.io/py/lagmat)

# lagmat
Lagmatrix. Create array with time-lagged copies of the features.


## Installation
The `lagmat` [git repo](http://github.com/ulf1/lagmat) is available as [PyPi package](https://pypi.org/project/lagmat)

```sh
pip install lagmat
```


## Usage

```py
import numpy as np
A = (np.random.rand(7,3) * 10 + 10).round(1)

from lagmat import lagmat
B = lagmat(A, lags=[0,1,2])  # 0: copy itself, 1: one time-lag, 2: two time-lags
```


Check the [examples](http://github.com/ulf1/lagmat/examples) folder for notebooks.


## Appendix

### Install a virtual environment

```sh
python3.6 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
pip3 install -r requirements-demo.txt
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `python -W ignore -m unittest discover`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`

### Clean up 

```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```

### Support
Please [open an issue](https://github.com/ulf1/lagmat/issues/new) for support.

### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/lagmat/compare/).
