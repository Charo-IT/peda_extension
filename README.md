# peda_extension
This adds some features to [PEDA](https://github.com/longld/peda) without modifying peda.py itself.

Works on Python 3 only.

## Features
* Patch `PEDA.read_int` and `PEDA.write_int`. (These wasn't working properly on Python 3.)
* Fixed an issue that PEDA fails to get pid while remote debugging.
* Add command
    * `pdisasret` -- Do `pdisass` until "ret" or "hlt" appears. Useful for stripped binaries.
* Add function
    * `PEDA.read_string` -- Do `PEDA.readmem` until null-byte appears.

## Installation
After installing PEDA,
```
git clone https://github.com/Charo-IT/peda_extension.git ~/peda_extension
echo "source ~/peda_extension/peda_extension.py" >> ~/.gdbinit
```
