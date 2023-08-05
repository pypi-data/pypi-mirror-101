from typing import Callable

import setuptools
import qfile
import test
import inspect

print("testing")
test._test()

print("Creating README.md")

# Generate README.md
readme = """# qfile
%s

`pip install qfile`

Common file operations in python should be simpler and involve less boilerplate, while still delivering fairly powerful options.
qfile was created for just that purpose.

Some simple code examples:
```python
import qfile

# Write to a given file
qfile.write("text.txt", "my text here")

# Read the given file
text = qfile.read("text.txt") # text == "my text here"

# Move folder "a" to existing folder "b", merging it with "b" if it already exists
qfile.move("a", "b", force=True) # Setting force=True ensures files replace folders with the same name in "b".

# Rename folder/file "x" to "y", raising an error if "y" exists already
qfile.rename("x", "y")

# Clone folder "b" into folder "c", making folder "c" if it doesn't exist
qfile.clone("b", "c", into=True)

# Make a folder, not caring if it already exists
# The same as Path("x/y/z").mkdir(parents=True, exist_ok=True) or os.makedirs(exist_ok=True)
qfile.folder("x/y/z")

# Delete the folder or file named "deleteme"
qfile.delete("deleteme")

# Replace all instances of "old" with "new" in all the ".txt" files in the current working directory
qfile.replace(qfile.glob(".", "**/*.txt"), "old", "new")
```

qfile can do a whole lot more, just check out the [API documentation](API.md)

## Deeper Example

Here's a specific example task: let's say you wanted to write some code that does these things:
- Open up an directory given by the user (creating it if it doesn't exist)
- Write a dictionary to a file in that directory in json-based format
- Read from a file in that directory, and if that file does not exist, use some other default value instead, writing back to the file
- Delete the file/folder "deleteme" in that directory, regardless of if it is a folder or a file with no extension. Nothing should happen if the item doesn't exist.

Someone might write code to do this like so:
```python
from pathlib import Path
import json
import shutil

# Make the directory
path = Path(input("Enter a directory: "))
path.mkdir(parents=True, exist_ok=True)
# Write dictionary to file
path.join("data.json").write_text(json.dumps({"a": 1, "b": 2}))

# Read from file
file = path.join("text")
try:
    text = file.read_text("utf-8")
except FileNotFoundError:
    text = "default"
    file.write_text(text, "utf-8")

# Delete "deleteme"
badfile = path.join("deleteme")
if badfile.is_dir():
    shutil.rmtree(badfile)
elif badfile.is_file():
    os.remove(badfile)
```

qfile, at least in my opinion, makes this process much simpler and more readable:
```python
import qfile

path = input("Enter a directory")
# Make the directory
with qfile.wd(path):
    # Write dictionary to file
    qfile.write("data.json", {"a": 1, "b": 2}, 'j')
    
    # Read from file
    text = qfile.read("text.txt", err="default")
    
    # Delete "deleteme"
    qfile.delete("deleteme")
```
"""
# Write to file
qfile.write('README.md', readme % (inspect.getdoc(qfile)))



# API

api = """# API
This is the entire api for qfile. It matches with version 1.1.0.

- [Renamed Standard Functions](#renamed-standard-functions)
%s

## Renamed Standard Functions
These are simply renamed versions of standard functions for easy access:

| Function     | Standard Function |
| ------------ | ----------------- |
| qfile.exists | os.path.exists    |
| qfile.isdir  | os.path.isdir     |
| qfile.isfile | os.path.isfile    |
| qfile.islink | os.path.islink    |
| qfile.fsize  | os.path.getsize   |
| qfile.join   | os.path.join      |


## Globals
These are settings for the entire library.

### default_force
**default_force: bool = False**

Determines the default force mode for the functions in this library (You can specify the "force" parameter on supported function calls to overwrite this setting).

When a function's "force" mode is False, attempts to write/read to folders or make a folder where a file is already will raise an OSError of some kind. When "force" is True, these attempts will instead delete the folder/file and overwrite it with the proper file type. Note that sub-directories are automatically set to force mode.

### max_read_size
**max_read_size: int = -1**

Determines the maximum file size in bytes the read() function can handle. Attempting to read from a file larger than this number will cause the read function to raise a ValueError. Set to -1 (default) for no limit.

%s
"""

apiitems = []
toc = []

itemmd = "### %s\n**%s%s**\n\n%s\n\n"

itemgroups = {
    "Generic Operations": [
        "parent", "delete", "force", "uuid", "ftype", "rel", "failed"
    ],
    "Folder Operations": [
        "scan", "glob", "wd", "folder"
    ],
    "File Operations": [
        "touch", "write", "chunks", "lines", "read"
    ],
    "Relocating Operations": [
        "merge", "clone", "move"
    ],
    "Replace Operations": [
        "replace", "rename"
    ],
    "Clipboard-Like Operations": [
        "cut", "copy", "a_cut", "a_copy", "unmark", "paste"
    ],
    "Archiving Operations": [
        "archive", "extract"
    ]
}
# Turn items into documentation
for key, group in itemgroups.items():
    igdata = []
    for item in group:
        inspect.getdoc(item)
        moditem = getattr(qfile, item)
        igdata.append(itemmd % (
            item,
            item, str(inspect.signature(moditem)).replace("*", "\\*"),
            inspect.getdoc(moditem)
        ))
    apiitems.append("## "+key+"\n\n"+"".join(igdata))
    toc.append(f"- [{key}](#{key.lower().replace(' ', '-')})")

# Write to file
qfile.write("API.md", api % ("\n".join(toc), "\n\n".join(apiitems)))


# Get build number
build = str(int(qfile.read('build.txt', err=False) or 0) + 1)
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