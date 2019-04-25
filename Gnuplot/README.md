# Plot CDF using Gnuplot.py

The plot.py contais a simple example of how to plot a CDF using the python package Gnuplot.py.

## Installation
One needs to install the Gnuplot program and the Gnuplot.py package first before running the code. Please refer to the following links for installation instructions.

* Gnuplot: [http://people.duke.edu/~hpgavin/gnuplot.html](http://people.duke.edu/~hpgavin/gnuplot.html)
* Gnuplot.py Package: [http://gnuplot-py.sourceforge.net/](http://gnuplot-py.sourceforge.net/)

__Notes for Windows user__: According to the README file in the Gnuplot.py package, because the main Windows Gnuplot executable (wgnuplot.exe) doesn't accept commands on standard input, Gnuplot.py cannot communicate with it. However, there is a simple little program called pgnuplot.exe that accepts commands on stdin and passes them to wgnuplot. So to run Gnuplot.py on Windows, you need to make sure that pgnuplot.exe is installed. It comes with gnuplot since at least version 3.7.1. However, __the pgnuplot.exe has been replace by gnuplot.exe__ at least since version 5.0.0. If you have installed the latest version of Gnuplot, you need to replace the pgnuplot.exe with gnuplot.exe in the source codes of Gnuplot.py package before installation.

## Quick Start Tutorials

* Gnuplot: [http://people.duke.edu/~hpgavin/gnuplot.html](http://people.duke.edu/~hpgavin/gnuplot.html)
* Gnuplot.py Package: the package comes with a simple demonstration demo.py. One of the examples is probably similar to what you want to do.