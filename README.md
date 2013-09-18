# PyTopol

Reza Salari - [Brannigan Lab](http://branniganlab.org)

### Introduction

**PyTopol** provides utilities to convert certain molecular topologies.
Currently it supports converting CHARMM `psf` files
to GROMACS topology format through the `psf2top.py` utility. If you'd like
to use GROMACS topologies in NAMD, please see
[here](http://www.ks.uiuc.edu/Research/namd/2.9/ug/node14.html).

PyTopol follows a different approach than the force-field conversion tools and
is intended to convert the full-topology of a molecule from one format to
another. This allows conversion of custom-parameterized topologies across
MD packages.


### Current stage
PyTopol is currently in *alpha stage*. The results for several
systems are shown below which are encouraging. However, before using it for
production simulations, more testing is needed.

Current version is 0.1.5. All 0.1.x versions will be considered alpha.


### Feedback
If you have a question, found a bug or have a suggestion, please submit it
[here](http://github.com/resal81/pytopol/issues).

### License
PyTopol is licensed under [GNU GPLv3](http://www.gnu.org/licenses/gpl.html).



## Quickstart

[PyTopol installation](https://github.com/resal81/PyTopol/wiki/PyTopol-Installation)

[psf2top usage](https://github.com/resal81/PyTopol/wiki/psf2top-Usage)

[psf2top tests](https://github.com/resal81/PyTopol/wiki/psf2top-Tests)

## Test Results

### psf2top.py

**Table 1.** Summary of the difference in potential energies (kcal/mol) between GROMACS 4.6.3 and NAMD 2.9 for
selected topologies converted from `psf`.  Percentages are shown in the parantheses. Single and double correspond to
the single and double-precision versions of GROMCAS.
```
--------------------------  -----------------  -----------------
              natoms  ff    GMX(double)-NAMD   GMX(single)-NAMD
--------------------------  -----------------  -----------------
  AD peptide      22  CH27  -0.000 ( 0.00 %)    -0.000 ( 0.00 %)
   POPC memb    9916  CH36  -0.001 ( 0.00 %)     0.063 ( 0.01 %)
   DOPC memb   10488  CH36   0.021 ( 0.00 %)     0.006 ( 0.00 %)
    Lysozyme    1966  CH27  -0.031 ( 0.00 %)    -0.028 ( 0.00 %)
 Cholesterol      74  CH36  -0.000 ( 0.00 %)    -0.000 ( 0.00 %)
Prot + Lipid   27562  CH36  -0.069 ( 0.00 %)    -0.906 ( 0.00 %)
--------------------------  -----------------  -----------------
```


## Contribution
There are many ways you can help to improve **PyTopol**:

* Convert your `psf` files to GROMACS format and compare NAMD and GROMACS energies.
  Use the issues page to let me know of the potential discrepancies.

* Run simulations using the generated topologies and see if the results make sense.

* Fork this repo, implement improvements and send me a pull request.


## Acknowledgement
* Energy conversion factors are from `charmm2gromacs-pvm.py` script by Par Bjelkmar,
Per Larsson, Michel Cuendet, Berk Hess and Erik Lindahl.

## Similar tools
* [charmm2gromacs](http://www.gromacs.org/@api/deki/files/185/=charmm2gromacs-pvm.py)
  is a tool for converting CHARMM force field to GROMACS.
* [psfgen-top](https://github.com/benlabs/psfgen-top) patches for psfgen (NAMD 2.7 and 2.8)
  to create gromacs topology.
* [SwissParam](http://www.swissparam.ch/) converts `mol2` format to CHARMM and GROMACS
  formats.



