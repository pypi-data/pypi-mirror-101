awk -F=  '{if ($1 =="version ") print $2}' setup.cfg | awk -F. '{print ++$3}'
rm -rf dist
python3 -m build
python3 -m twine upload dist/*
