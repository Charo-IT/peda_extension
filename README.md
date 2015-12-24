# peda_extension
This adds some features to [PEDA](https://github.com/longld/peda) without modifying peda.py itself.

Works with Python 3 only.

## Features
* Patch `PEDA.read_int` and `PEDA.write_int`. (These wasn't working properly with Python 3.)
* Add command
    * `pdisasret` -- Do `pdisass` until "ret" or "hlt" appears. Useful for stripped binaries.

## Installation
After installing peda,
```
git clone https://github.com/Charo-IT/peda_extension.git ~/peda_extension
echo "source ~/peda_extension/peda_extention.py" >> ~/.gdbinit
```
