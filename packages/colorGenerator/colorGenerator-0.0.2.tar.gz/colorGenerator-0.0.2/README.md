# Color Generator
Following this [course](https://packaging.python.org/tutorials/packaging-projects/)

## Coding steps
Make sure you have the latest versions of PyPA’s build installed:
```bash
pip install --upgrade build
```
This command should output a lot of text and once completed should generate two files in the dist directory:
```bash
python -m build
```
### Uploading the distribution archives
You can use twine to upload the distribution packages. You’ll need to install Twine:
```bash
pip install --upgrade twine
```
Once installed, run Twine to upload all of the archives under dist:
```bash
twine upload dist/*
```