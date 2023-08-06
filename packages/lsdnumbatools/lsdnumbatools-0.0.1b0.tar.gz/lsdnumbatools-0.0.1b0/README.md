# lsdnumbatools
**MASSIVE REFACTORING IN PROGRESS (23/12/2020): Moving all the main objects to `xarray` data structure**

**DISCLAIMER**: early and WIP, do not use if you don't know what you are doing!

Provides numba framework for topographic analysis within the LSDTopoTools ecosystem. It aims to provdide full python access to the main algorithms of LSDTopoTools while avoiding the neeeds of c++. It does not replace or provide numba portage of the full LSDTopoTools, just the main one for quick use or quick developments.

**License:** Free software: MIT license

## What-Why-How?

`Numba` is a Just-in-time (JIT) compiler for python code, which means that it translates at runtime some pieces of code into assembly language using LLVM engine. It has the power to make some (straightforward) `python` functions as performant as `C` code under few conditions. Although it does not allow as much flexibility and power as `C++` does, it is powerful for function with simple data-structure (numpy arrays). The huge advantage is that it fits in the interpreted python language and allow very quick development/debugging/distribution of code without the need of compiling for different platform and making bindings between `python` and `C`, making it an ideal tool for (i) testing algorithms before implementing them in heavier languages and (ii) develop a *light* version of the `LSDTopoTools` framework usable in full-python when the full stack of `LSDTopoTools` are not needed.

## Features

### Node graph

So far I mostly worked on the node graph object, which build on demand neighbouring info (Queen, King); single (Braun et al. 2013) and multiple (see `fastscapelib-fortran`](https://github.com/fastscape-lem/fastscapelib-fortran) ) flow topological order, and periodic/closed boundary conditions.

## Installation

If I start using this package more seriously, I will make a `conda-forge` package. Otherwise, clone this repository, and install the following dependencies: `numba, numpy, matplotlib, pandas` and it should do the trick. I recommend using `conda` as python environment manager. 

## Quick Start

As a quick start, I added a jupyter notebook in the notebook folder.

## Credits

Contact: Boris Gailleton (boris.gailleton@gfz-potsdam.de)

Some of the core functions have been adapted from `xarray-topo` by Benoit Bovy
This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
