from typing import Callable

import setuptools
import qfile
import inspect

print("testing")
qfile._test()

print("Creating README.md")
# Generate README.md
readme = """# qfile
%s

`pip install qfile`

Common file operations in python should be simpler and involve less boilerplate; this library was made to enable just that. Consider the following code:
```python
import os, shutil, json

# Create a folder and enter it
owd = os.getcwd()
if not os.path.exists("myFolder"):
    os.mkdir("myFolder")
os.chdir("myFolder")

# Try catch loop to make sure the folder is reset
try:
    os.mkdir("data")
    
    # Write some json data to a file
    with open("data/myFile.json", "w") as file:
        json.dump({"a": 1, "b": 2}, file)
    
    # Read some stuff
    try:
        with open("data/thing.txt", "r") as file:
            data = file.read()
    except OSError:
        data = "default"
finally:
    os.chdir(owd)
```

With qfile, this code can become a lot simpler:
```python
import qfile

# Create a folder and enter it
with qfile.wd("myFolder"):
    # Write some json to a file
    qfile.write("data/myFile.json", {"a": 1, "b": 2}, "j")
    
    # Read some stuff
    data = qfile.read("data/thing.txt") or "default"
```

qfile also has the safeguard option to "force" write to a file or folder, which will overwite anything in that location (normally trying to write like this raises an error):
```
qfile.default_force = True
qfile.folder("myFolder.txt") # Makes a folder named "myFolder.txt"
qfile.write("myFolder.txt", "text") # Overwrites the folder with a file
```

## API
Here's all the global data and functions available:


%s
"""

itemmd = """### %s%s

%s
"""

# API
api = []

apidata = {
    "default_force": ("default_force", ":bool", 'Determines the default force mode for the methods in this library (You can specify the "force" parameter on supported function calls to overwrite this setting).\n\nWhen a method\'s "force" mode is False, attempts to write/read to folders or make a folder where a file is already will raise an OSError of some kind. When "force" is True, these attempts will instead delete the folder/file and overwrite it with the proper file type. Note that sub-directories are automatically set to force mode.)')
}

for name in qfile.__all__:
    item = getattr(qfile, name)
    if isinstance(item, Callable):
        api.append(itemmd % (name, str(inspect.signature(item)), inspect.getdoc(item)))
    else:
        api.append(itemmd % apidata[name])

# Write to file
qfile.write('README.md', readme % (inspect.getdoc(qfile), '\n\n'.join(api)))



# Get build number
build = str(int(qfile.read('build.txt') or 0) + 1)
qfile.write('build.txt', build)

# Setup module for pip
setuptools.setup(
    name='qfile',
    packages=['qfile'],
    version=qfile.__version__+'.'+build,
    author='Zach K (mathgeniuszach)',
    author_email='huntingmanzach@gmail.com',
    description=inspect.getdoc(qfile),
    long_description='A python library for simplifying common file operations. Check out the `github page <https://github.com/xMGZx/qfile>`_ for more info.',
    url='https://github.com/xMGZx/qfile',
    classifiers=[
        'Programming Language :: Python :: 3'
    ]
)