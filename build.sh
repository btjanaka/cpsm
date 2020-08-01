# Build script for uploading to PyPI

rm -rf dist
python setup.py sdist bdist_wheel
twine upload dist/*
