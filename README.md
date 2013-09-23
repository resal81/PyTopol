# PyTopol

Reza Salari - [Brannigan Lab](http://branniganlab.org)

### Introduction

**PyTopol** provides utilities to convert certain molecular topologies.
It follows a different approach than the force-field conversion tools and
is intended to convert the full-topology of a molecule from one format to
another. This allows conversion of custom-parameterized topologies across
MD packages.

Currently PyTopol includes the following utilities:

* **psf2top.py** : for converting CHARMM `psf` files to GROMACS topology format. The
reverse conversion of GROMACS topologies to NAMD is planned an will be implemented. Also see
[here](http://www.ks.uiuc.edu/Research/namd/2.9/ug/node14.html).


### Current stage

Current version is 0.1.6.

All 0.1.x versions will be considered **alpha**. See the results for the current tests below.


### Feedback
If you have a question, found a bug or have a suggestion, please submit it
[here](http://github.com/resal81/pytopol/issues).

### License
PyTopol is licensed under [GNU GPLv3](http://www.gnu.org/licenses/gpl.html).



## Quickstart

#### Installation
[How to install PyTopol](https://github.com/resal81/PyTopol/wiki/PyTopol-Installation)


#### PSF to GROMACS topology conversion
[How to use psf2top.py](https://github.com/resal81/PyTopol/wiki/psf2top-Usage)

**Table 1**. Summary of the rmsd of potential energy terms between GROMACS 4.6.3 and NAMD 2.9 (kcal/mol). Single and double correspond to the single and double-precision versions of GROMCAS.

```
--------------------------  -----------------  -----------------
              natoms  ff    GMX-NAMD (double)  GMX-NAMD (single)
--------------------------  -----------------  -----------------
  AD peptide      22  CH27             0.000               0.000
   POPC memb    9916  CH36             0.002               0.021
   DOPC memb   10488  CH36             0.005               0.014
    Lysozyme    1966  CH27             0.009               0.010
 Cholesterol      74  CH36             0.000               0.000
 Pr+Chol+Lip   27562  CH36             0.046               3.988
--------------------------  -----------------  -----------------
```
For the detailed results, please see [here](https://github.com/resal81/PyTopol/wiki/psf2top-Tests).


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



