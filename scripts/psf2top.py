#!/usr/bin/env python

'''
    psf2top.py - A library for converting molecular topologies
    Copyright (C) 2013  Reza Salari

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


'''
This scritp automates the conversion of PSF file to GROMACS topology.

'''

import argparse, sys, os
import logging
from pytopol import charmmpar, grotop, psf
from pytopol import __version__ as version


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


def print_note():
    note = '''
    ------------------------------------------------------------------------
    PyTopol version %s.

    Please note that this version is considered alpha and the generated
    topologies should be validated before being used in production
    simulations.

    For more info, please see: http://github.com/resal81/pytopol
    ------------------------------------------------------------------------
    '''

    print(note % version)

def main():
    print_note()

    if len(sys.argv) <= 1:
        usage = '\nUse -h for more info. Example run:\n'
        usage += '  psf2top.py -p psffile -c charmm_prm1 [charmm_prm2 ...] [-v]'
        print(usage)
        return

    # interface
    formatter = argparse.ArgumentDefaultsHelpFormatter
    p = argparse.ArgumentParser(formatter_class=formatter)
    p.add_argument('-p', type=str, help='psf file')
    p.add_argument('-c', default=[None], action='store', type=str, nargs='*',
    	help='charmm parameter files')
    p.add_argument('-v', action='store_true', help='verbose output', default=False)

    args = p.parse_args()

    # setup logging
    log_level = logging.DEBUG if args.v else logging.ERROR
    lgr = _setup_logging(log_level)
    lgr.debug('>> started main')

    # read the PSF file
    psffile = args.p
    psfsys = psf.PSFSystem(psffile, pdbfile=None, each_chain_is_molecule=True)
    if len(psfsys.molecules) == 0:
        lgr.error("could not build PSF system - see above")
        return

    # read all the parameter files
    prmfiles = args.c
    par = charmmpar.CharmmPar(*prmfiles)

    # add parameters to the system
    par.add_params_to_system(psfsys, panic_on_missing_param=True, forcefield='charmm')

    # convert system to gromacs format
    grotop.SystemToGroTop(psfsys)
    if not os.path.exists('top.top') or not os.path.exists('itp_mol_01.itp'):
    	lgr.error("could not build GROAMCS top file - see above")

    lgr.debug('<< exiting main \n')

    print('Done.')

main()



