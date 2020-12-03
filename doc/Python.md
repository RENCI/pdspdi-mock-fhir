# Installing Python for Linux

Check the native version of python:
```
python --version
```

If the version dosen't meet requirements, we recommend installing
Miniconda locally, adding libraries to a virtual environment with
conda as needed. This has the advantage of allowing multiple, minmal
deployment environments, each of which can be configured for different
purposes.

Detailed instructions for Miniconda install can be found here:
https://docs.conda.io/en/latest/miniconda.html

For example, the following works for RHEL 7.9:

    # To install tx-functional, pandas, python-dateutil, requests, tqdm, joblib:
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    sha256sum Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh
    conda create --name pds_venv
    conda activate pds_venv
    pip3 install update pip
    pip3 install tx-functional pandas
    conda install python-dateutil requests tqdm joblib
