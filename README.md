# PyTopol

.. image:: https://badge.fury.io/py/pytopol.png
    :target: http://badge.fury.io/py/pytopol
    
"A Library for converting molecular topologies"

Reza Salari [Brannigan Lab](http://branniganlab.org)

## Introduction 

PyTopol provides utilities to convert certain molecular topologies to 
each other. Currently it supports converting NAMD `PSF` files to GROMACS 
topology format. If you'd like to run GROMACS topologies in NAMD, plese 
see [here](http://google.com).

Note that PyTopl is currently in alpha stage. You are welcome to test it on your systems, 
but using the created topologies for production runs requires more testing. The 
results for some non-trivial systems are encouraging and provide below.

PyTopol is licensed under GNU GPL 3. 

Please submit your suggestions/questions at the [issues](github.com) page.


## Quickstart

1. Install PyTopol using either of the following methods: 

  * Using `pip`::

    $ pip install pytopol

  * Or clone the repo and add it to the python path::

    $ git clone 
    $ cd pytopol  
    $ export PYTHONPATH=`pwd`:$PYTHONPATH

2. Convert `PSF` files to GROMACS topologies using `psf2top.py`. This will
   create one `TOP`(`top.top`) file and one or multiple `ITP` files:

  * If you used `pip` to install PyTopol::

    $ psf2top psffile charmm_prm1 [charmm_prm2 ...] 

  * Or if you clone the repo::

    $ cd scripts
    $ psf2top psffile charmm_prm1 [charmm_prm2 ...] 


## Notes 

* `psf2top` converts each segment in the `PSF` file to one `ITP` file. 

* `psf2top` only accepts `NAMD` formatted `PSF` files, where the columns in the
  atoms section of the `PSF` file are separated by at least one space. If this
  is the case for your `PSF` file, make sure there is the `NAMD` keyword in the
  first line of the `PSF` file.

* You should provide all CHARMM parameter files for all the atoms in your `PSF`
  file. This typically is all the parameter files that you use for your system
  when running a NAMD simulation. 

* The CHARMM `str` files are not supported. These are files that typically
  include both topology and parameters for a molecule. For these cases put the
  parameter section in a separate file before giving it to `psf2top`.


## Test systems 

* I used `psf2top` to convert several `PSF` files to GROMACS format and then
  compared the resulting energies using NAMD and GROMACS. 

GROMACS `MDP` file: 
```

```





## TODO 

## Acknowlegement 


