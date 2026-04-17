# Jupyter kernel for Kap

This is a [Jupyter](http://jupyter.org/) kernel for the [Kap](https://kapdemo.dhsdevelopments.com/) array language. 

## Do you have any pre-made notebook documents?

Added a couple of demo notebooks to the [notebooks](https://github.com/kapitaali/kap_kernel/tree/main/notebooks) directory.

## Installation

### Pre-requisites:

- Python version 3.8 or later. Python can be installed in several ways. We recommend the standard download from https://www.python.org/downloads/. This kernel was created with Python from [Anaconda](https://anaconda.org/).
- Jupyter: see the [official documentation](https://jupyter.readthedocs.io/en/latest/install.html) for installation instructions.

### Installing the Dyalog kernel

Clone this repo somewhere, then cd kap-jupyter-kernel

In your terminal, run the follwing command:

```sh
./install_kernel.sh
```

You should now be able to see the `kap-jupyter-kernel` kernel listed:
```sh
jupyter kernelspec list

Available kernels:
  kap                   /home/theb/.local/share/jupyter/kernels/kap
  python3               /home/theb/.local/share/jupyter/kernels/python3
  rust                  /home/theb/.local/share/jupyter/kernels/rust  
```

Start Jupyter:

```sh
jupyter lab # or jupyter notebook
```
and you should now see Kap amongst your kernels. Click on the Kap icon.

# NOTICE

This kernel comes bundled with Kap Linux native executable. If the executable does not run, refer to [Kap](https://codeberg.org/loke/array) documentation how to build a Linux native Kap client. After building, copy the contents of the build directory and the standard library to a directory, and then copy the files from root dir of this repo to your directory and run `install_kernel.sh`.

