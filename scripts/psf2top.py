#!/usr/bin/env python

'''
This scritp automates the conversion of PSF file to GROMACS topology.

'''


import sys
import logging
from pytopol import charmmpar, grotop, psf


def _setup_logging(debug_level=logging.DEBUG):
    """ Setup initial logging.

    Args:
        debug_level: the level for debugging
    Returns:
        a logging.Logger instance

    """

    lgr = logging.getLogger('mainapp')
    lgr.setLevel(debug_level)

    frmt = logging.Formatter('%(name)-30s - %(levelname)-8s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(debug_level)

    ch.setFormatter(frmt)

    lgr.addHandler(ch)
    return lgr


def main():
    """ Main function. """

    if len(sys.argv) <= 2:
        usage = 'python psf2top.py psffile charmm_prm1 [charmm_prm2 ...]'
        print('\nUsage:\n\t %s \n' % usage)
        return

    # the first element should be the path to the psf file
    psffile = sys.argv[1]

    if len(sys.argv) >= 3:
        if sys.argv[-1] == '-v':
            debug_level = logging.DEBUG
            prmfiles = sys.argv[2:-1]
        else:
            debug_level = logging.ERROR
            prmfiles = sys.argv[2:]

    # setup logging
    lgr = _setup_logging(debug_level)
    lgr.debug('>> started main')

    # read the PSF file
    psfsys = psf.PSFSystem(psffile, pdbfile=None, each_chain_is_molecule=True)
    if len(psfsys.molecules) == 0:
        lgr.error("could not build PSF system - see above")
        return

    # read all the parameter files
    par = charmmpar.CharmmPar(*prmfiles)

    # add parameters to the system
    par.add_params_to_system(
        psfsys, panic_on_missing_param=True, forcefield='charmm')

    # convert system to gromacs format
    grotop.SystemToGroTop(psfsys)

    lgr.debug('<< done \n')


main()
