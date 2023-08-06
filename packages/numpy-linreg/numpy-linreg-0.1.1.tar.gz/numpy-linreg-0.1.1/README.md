[![PyPI version](https://badge.fury.io/py/numpy-linreg.svg)](https://badge.fury.io/py/numpy-linreg)

# numpy-linreg
Linear Regression with numpy only.


## Installation
The `numpy-linreg` [git repo](http://github.com/ulf1/numpy-linreg) is available as [PyPi package](https://pypi.org/project/numpy-linreg)

```sh
pip install numpy-linreg
pip install git+ssh://git@github.com/ulf1/numpy-linreg.git
```


## Usage
Ridge Regression

```py
import numpy_linreg.ridge as ridge
import numpy_linreg.metrics as metrics
beta = ridge.lu(y, X)
rmse = metrics.rmse(y, X, beta)
```

OLS Regression

```py
import numpy_linreg.ols as ols
beta = ols.lu(y, X)
beta = ols.pinv(y, X)
beta = ols.qr(y, X)
beta = ols.svd(y, X)
```

Check the [examples](http://github.com/ulf1/numpy-linreg/tree/master/examples) folder for notebooks.


## Appendix

### Commands
Install a virtual environment

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
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`

### Clean up 

```
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```

### Support
Please [open an issue](https://github.com/ulf1/numpy-linreg/issues/new) for support.

### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/numpy-linreg/compare/).
