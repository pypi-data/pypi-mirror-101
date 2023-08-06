# apikey

## Installation 
The `apikey` [git repo](http://github.com/ulf1/apikey) is available as [PyPi package](https://pypi.org/project/apikey)

```
pip install "apikey>=0.2.1"
pip install git+ssh://git@github.com/ulf1/apikey.git
```

## Usage
Store in default location `$HOME/.apikey-store` 

```python
import apikey

apikey.save("service1", "supersecret")
apikey.save("service2", "donttellanyone")
apikey.save("service3", "aboutthiskey")

key1 = apikey.load("service1")
key2 = apikey.load("service2")
key3 = apikey.load("service3")
```

Store in a specific file

```python
apikey.save("service42", "topsecretkey", filename="/srv/.secretkeys")
key = apikey.load("service42", filename="/srv/.secretkeys")
```


## Appendix

### Install a virtual environment

```sh
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt
```


### Python commands

* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `pytest`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`
