# FtApi

## Usage
You need to have uid and secret from 42 application panel
tons of love for the dev Team who makde RESTful API.
You guys rock !!!

```
pip install FtApi
```

## Example

![example](https://github.com/ryaoi/ftApi/blob/master/img/example.png)

### For myself
```
launch 42api_creator.py
cp FtApi.py inside the folder FtApi
vim CHANGES.txt #update the information
vim setup.py #change version of the package
python3 setup.py sdist bdist_wheel
python3 -m twine upload --skip-existing --repository-url https://upload.pypi.org/legacy/ dist/*
```
