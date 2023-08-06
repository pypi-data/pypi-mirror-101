##Userlibrary Spin D
This library was written by Moritz Goerzen to handle the Spin Dynamic simulations more efficient.
For descriptions see LIBRARY_DOCUMENTATION_072020.pdf

Can be installed via
'pip install userlib-spinD'.

##Updating library on package index PyPi
1. upgrade setuptools:
'pip install --upgrade setuptools wheel' and 'pip install --upgrade setuptools twine'
2. remove all files in old distribution file (dist/)
3. build: 'python setup.py sdist bdist_wheel'
4. distribute: 'python -m twine upload dist/*
5. enter username and password