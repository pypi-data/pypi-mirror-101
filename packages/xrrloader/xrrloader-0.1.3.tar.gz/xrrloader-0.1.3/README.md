# _xrrloader_ Python package

## Description

This package is designed to extract reflectivity scans from a SPEC file to a text file,
transform them into _q_ space and apply footprint correction. It contains a command line
script which allows its usage without writing any python code.

The command line script uses different modules from the package that are also directly
accesible for other python code if the package is imported.

## Installation

### Prerequisites
Please make sure you have at least Python 3.7 installed on your computer and you have the
ability to install new packages from the internet via pip (or an alternative package
manager). It is also recommended that you create a virtual environment (e.g. via _venv_)
to separate the dependencies for this package from your normal Python installation.

### Using a local copy

The fastest way to use _xrrloader_ is to just download and unzip the whole project and
do all of your work inside the project folder.

1. Download the package and unzip it somewhere on your computer where you want to use it
2. Change your working directory to the _xrrloader_ top-level folder which contains the
readme file
3. Install a virtual environment e.g. via `python3.7 -m venv env`
4. Activate the virtual environment with `activate env/bin/activate` (Linux/macOS) or `env/
   scripts/activate.bat` (Windows)
5. Install the package requirements via `pip install -r requirements.txt`

### Installation via pip

If you want to install _xrrloader_ to an already existing python environment (so that it
can be important from any script that uses that environment) you can install it via pip.

1. Download the package and unzip it somewhere on your computer
2. Make sure you have the environment of your choice activated (see above)
3. Install the package with pip install `/<folderpath>/xrrloader-master/` where
   `<folderpath>` is the path to the folder where you unzipped the package into

## Usage

### Command line script

To be able to extract reflectivity scans from a SPEC file via the command line you need
the `extract_refl.py` script which is contained within the package folder. If you are
using a local copy of _xrrloader_, the script has to be located within the folder. If
you have installed the package via pip, the script can be anywhere. In both cases, please
make sure the corresponding environment is activated.

Execute the script via `python extract_refl.py <arguments>`.

Use `python extract_refl.py -h` for help on what optional and mandatory arguments can be
passed. Arguments that contain spaces need to be encapsulated with apostrophes.

Example:
```
python extract_refl.py Probe18_DNTT_100.spec 7 1 detcorr 'Two Theta' -n max -f 0.05 10 -o output.dat
```

### Extended package usage

To be able to use all features of this package, it can be imported into any other python
script or Jupyter notebook via `import xrrloader`. However, if the package was not
installed via pip, any file using the `import` statement must be located within the
package folder. Thus, for this extended use, installing the package is recommended.