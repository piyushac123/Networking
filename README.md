## Networking Practice
### Network Security
#### Assignment 1 - [link](https://drive.google.com/file/d/1QtHWcWm_dAkmzgp97AHHrwtikY6n2QgW/view?usp=sharing)
### AdHoc Network

**Virtual Environment setup**

- Install pip
    - `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` - Download and store get-pip.py
    - `python3 get-pip.py` - execute downloaded file to install pip
    - `pip -V` - test pip installation
    - `pip uninstall pip && sudo apt-get remove python-pip` - uninstall pip

- Install pip package
    - `pip install {package}` - install {package} in system
    - `pip show {package}` - show details of installed {package} in system
    - `pip uninstall {package}` - uninstall {package} in system

- Install and setup virtual environment
    - `pip install virtualenv` - install virtualenv
    - `virtualenv --version` - test virtualenv installation
    - `virtualenv my_name` - create virtualenv
    - `virtualenv -p /usr/bin/python{v} my_name` - create virtualenv with specific python version {v}
    - `source my_name/bin/activate` - activate virtualenv
    - `(virtualenv)$ deactivate` - deactivate virtualenv

- Code formatter - black
    - `black {source_file_or_directory}` - format one or many files in-place

- Executable example 
    - `sh {project}/exec.sh` - execute shell script