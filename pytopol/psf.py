"""
This module provides tools for working with PSF files.

"""

from pytopol.utils import build_res_chain, build_pairs
from pytopol.pdb import PDBSystem
from pytopol import blocks

import os
import logging
import time

# create logger
module_logger = logging.getLogger('mainapp.psf')



class PSFSystem(object):

    """ PSFSystem class povides functionality to parse PSF files. """



    def __init__(self, psffile, pdbfile=None, each_chain_is_molecule=False):
        """ Initialization of a PSF file.

        Args:
            psffile
                the path to the psf file
            pdbfile
                optional, the path to the pdb file
            each_chain_is_molecule
                bool, if True, each segment in the PSF file will be converted
                to one Molecule instance.

        Attributes:
            self.lgr        : logger.Logger
            self.psfile     : str, path to the psf file
            self.pdbfile    : str, path to the pdb file
            self.molecules  : a tuple of Molecule instances

        """

        self.lgr = logging.getLogger('mainapp.psf.PSFSystem')
        self.lgr.debug(">> entering PSFSystem")

        self.psffile = psffile
        self.molecules = tuple([])

        # parse the psf file and create one molecule
        mol = self._parse(self.psffile)

        if mol:
            self.lgr.debug("the psf molecule was parsed")

            # add pdb file
            if pdbfile:
                self.pdbfile = pdbfile
                self._add_pdbfile(pdbfile, mol)

            # break psf segments to one molecule
            if each_chain_is_molecule:
                sepmols = self._process_psf(mol)
                if sepmols:
                    self.molecules = tuple(sepmols)
                    self.lgr.debug(
                       "%d molecules were generated from the psf file" % len(sepmols))
                else:
                    self.lgr.warning(
                        "could not convert psf segments to molecules")
            else:
                self.molecules = tuple([mol])

        self.lgr.debug("<< leaving PSFSystem")



    def __repr__(self):
        natoms = sum([len(m.atoms) for m in self.molecules])
        return 'PSF file with %6d atoms and %2d molecules' % (
            natoms, len(self.molecules))



    def _add_pdbfile(self, pdbfile, mol):
        """ add coordinates form a pdb file to the system."""

        pdb = PDBSystem(pdbfile, guess_mols=False)

        if len(pdb.atoms) == len(mol.atoms):
            for i, atom in enumerate(mol.atoms):
                atom.coords = pdb.atoms[i].coords
            self.lgr.debug("coordinates from pdb file were added")
        else:
            self.lgr.error("the number of atoms in the pdb and psf files doesn't match: %6d vs %6d" % (
                len(pdb.atoms), len(mol.atoms)))



    def _parse(self, psffile):
        """ Parse a psf file.

        Args:
            psffile : str, path to the psf file
        Returns:
            a Molecule instance or False

        """

        self.lgr.debug("parsing psf file: %s" % psffile)

        t1 = time.time()

        # check if the file exists
        if not os.path.exists(psffile):
            self.lgr.critical("file doesn't exist")
            return False

        # initialize empty list for data
        mol = blocks.Molecule()

        # supported formats
        psf_formats = {
            'NAMD': {
                'sections': {
                    '!NATOM':  {'type':'atom',    'n':(9,11),'multiple':False,'func':self._atom_line},
                    '!NBOND':  {'type':'bond',    'n':2,'multiple':True, 'func':self._badi_line},
                    '!NTHETA': {'type':'angle',   'n':3,'multiple':True, 'func':self._badi_line},
                    '!NPHI':   {'type':'dihedral','n':4,'multiple':True, 'func':self._badi_line},
                    '!NIMPHI': {'type':'improper','n':4,'multiple':True, 'func':self._badi_line},
                    '!NCRTERM':{'type':'cmap',    'n':8,'multiple':False,'func':self._badi_line},
                },
            },
        }


        # find the psf format
        with open(psffile) as f:
            for line in f:
                psffmt = self._find_psf_format(line)
                break

        # check if the format is valid
        if psffmt is False:
            # assume the format is 'NAMD'
            psffmt = 'NAMD'
            #return False

        elif psffmt not in list(psf_formats.keys()):
            self.lgr.error("psf format '%s' is not supported" % (psffmt))
            return False

        # parse the file
        _sec = None
        known_sections = list(psf_formats[psffmt]['sections'].keys())

        with open(psffile) as f:
            for line in f:
                line = line.strip()

                if line == '':
                    continue

                if '!' in line:
                    if line.split()[1].strip(':') in known_sections:
                        _sec = line.split()[1].strip(':')
                    else:
                        self.lgr.debug("skipping section`: '%s'" % line)
                        _sec = None
                    continue

                if _sec is not None:
                    _conf = psf_formats[psffmt]['sections'][_sec]
                    result = _conf['func'](psffmt, line, _conf, mol)
                    if result is False:
                        self.lgr.error("couldn't parse this line in '%s' section:\n  %s" % (_sec, line))
                        return False

        # build chain and residues
        build_res_chain(mol)
        build_pairs(mol)

        t2 = time.time()
        self.lgr.debug("parsing took %4.1f seconds" % (t2-t1))

        return mol



    def _process_psf(self, temp_mol):
        """Convert a psf Molecule to multiple Molecules.

        Using this function only makes sense if the segments in the PSF file
            are not covalently bond (usually this the case).

        Args:
           temp_mol : a psf Molecule instance

        Returns:
           list of Molecules or False

        """

        self.lgr.debug("converting psf to multiple molecules based on chains")

        unique_chains = set([chain.name for chain in temp_mol.chains])
        if len(unique_chains) != len(temp_mol.chains):
            self.lgr.error("the name of the chains is not unique")
            return False


        # counter for different elements in the psf file
        _NA= _B = _A = _D = _I = _C = _NP = 0
        molecules = []


        # Atom:Chain.name dictionary for easy lookup
        _AC_map = {}
        for atom in temp_mol.atoms:
            _AC_map[atom] = atom.residue.chain.name


        for chain in temp_mol.chains:
            m = blocks.Molecule()
            chainname = chain.name

            for res in chain.residues:
                for atom in res.atoms:
                    m.atoms.append(atom)
                    _NA += 1

            for b in temp_mol.bonds:
                if _AC_map[b.atom1] == chainname and _AC_map[b.atom2] == chainname:

                    m.bonds.append(b)
                    _B += 1

            for a in temp_mol.angles:
                if _AC_map[a.atom1] == chainname and _AC_map[a.atom2] == chainname and \
                   _AC_map[a.atom3] == chainname:

                    m.angles.append(a)
                    _A += 1

            for d in temp_mol.dihedrals:
                if _AC_map[d.atom1] == chainname and _AC_map[d.atom2] == chainname and \
                   _AC_map[d.atom3] == chainname and _AC_map[d.atom4] == chainname:

                    m.dihedrals.append(d)
                    _D += 1

            for i in temp_mol.impropers:
                if _AC_map[i.atom1] == chainname and _AC_map[i.atom2] == chainname and \
                   _AC_map[i.atom3] == chainname and _AC_map[i.atom4] == chainname:

                    m.impropers.append(i)
                    _I += 1


            for c in temp_mol.cmaps:
                if _AC_map[c.atom1] == chainname and _AC_map[c.atom2] == chainname and \
                   _AC_map[c.atom3] == chainname and _AC_map[c.atom4] == chainname and \
                   _AC_map[c.atom5] == chainname and _AC_map[c.atom6] == chainname and \
                   _AC_map[c.atom7] == chainname and _AC_map[c.atom8] == chainname:

                    m.cmaps.append(c)
                    _C += 1

            for p in temp_mol.pairs:
                if _AC_map[b.atom1] == chainname and _AC_map[b.atom2] == chainname:

                    m.pairs.append(p)
                    _NP += 1

            build_res_chain(m)
            #build_pairs(m)
            m.renumber_atoms()
            molecules.append(m)

        # make sure we used all the enteties in the temp_mol
        assert len(temp_mol.atoms)     == _NA
        assert len(temp_mol.bonds)     == _B
        assert len(temp_mol.angles)    == _A
        assert len(temp_mol.dihedrals) == _D
        assert len(temp_mol.impropers) == _I
        assert len(temp_mol.cmaps)     == _C
        assert len(temp_mol.pairs)     == _NP

        return molecules



    def _find_psf_format(self, first_line):
        """Find the PSF format.

        Args:
            first_line: str, the first line in the psf file

        Returns:
            'NAMD' or False

        """
        _line = first_line.strip()
        if not _line.startswith('PSF'):
            self.lgr.error("the first line of psf file doesn't start with 'PSF'")
            return False
        else:
            fields = _line.split()
            if 'NAMD' in fields:
                return 'NAMD'
            else:
                self.lgr.warning("could not find NAMD keywork in "
                                 "the first line in the psf file")
                return False



    def _atom_line(self, psffmt, line, conf, m):
        """Parse an ATOM line in the psf file.

       Args:
           psffmt: str, 'NAMD'
           line:  str, a psf ATOM line
           conf: dict
           m:  Molecule

        """
        if psffmt == 'NAMD':
            f = line.split()
            if len(f) not in conf['n']:
                self.lgr.error("(e) the number of elements in atom line is '%d, expected to be %d" % (
                    len(f), conf['n']))
                return False

            if len(f) == 9:
                atnumb, segname, resnumb, resname, atname, attype, charge, mass, tmp = f
            elif len(f) == 11:
                atnumb, segname, resnumb, resname, atname, attype, charge, mass, tmp1, tmp2, tmp3 = f
            else:
                raise NotImplementedError
            a = blocks.Atom()
            a.name      = atname
            a.number    = int(atnumb)
            a.atomtype  = attype
            a.chain     = segname
            a.resname   = resname
            a.resnumb   = int(resnumb)
            a.charge    = float(charge)
            a.mass      = float(mass)

            m.atoms.append(a)
            return True

        else:
            raise NotImplementedError



    def _badi_line(self, psffmt, line, conf, m):

        if psffmt == 'NAMD':

            f = line.split()

            # check the number of elements in the line
            if conf['multiple']:
                assert len(f) % conf['n'] == 0
            else:
                assert len(f) == conf['n']

            # read the elements
            for i in range(int(len(f)/conf['n'])):
                if conf['type'] == 'bond':
                    _m = i * conf['n']
                    _n = i * conf['n'] + 1

                    b = blocks.Bond()
                    atom1 = m.anumb_to_atom(int(f[_m]))
                    atom2 = m.anumb_to_atom(int(f[_n]))

                    if atom1 and atom2:
                        b.atom1 = atom1
                        b.atom2 = atom2

                        m.bonds.append(b)
                    else:
                        raise TypeError

                elif conf['type'] == 'angle':
                    _m = i * conf['n']
                    _n = i * conf['n'] + 1
                    _o = i * conf['n'] + 2

                    a = blocks.Angle()
                    atom1 = m.anumb_to_atom(int(f[_m]))
                    atom2 = m.anumb_to_atom(int(f[_n]))
                    atom3 = m.anumb_to_atom(int(f[_o]))

                    if atom1 and atom2 and atom3:
                        a.atom1 = atom1
                        a.atom2 = atom2
                        a.atom3 = atom3

                        m.angles.append(a)
                    else:
                        raise TypeError

                elif conf['type'] in ('dihedral', 'improper'):
                    _m = i * conf['n']
                    _n = i * conf['n'] + 1
                    _o = i * conf['n'] + 2
                    _p = i * conf['n'] + 3

                    if conf['type'] == 'dihedral':
                        d = blocks.Dihedral()
                        cont = m.dihedrals
                    else:
                        d = blocks.Improper()
                        cont = m.impropers

                    atom1 = m.anumb_to_atom(int(f[_m]))
                    atom2 = m.anumb_to_atom(int(f[_n]))
                    atom3 = m.anumb_to_atom(int(f[_o]))
                    atom4 = m.anumb_to_atom(int(f[_p]))

                    if atom1 and atom2 and atom3 and atom4:
                        d.atom1 = atom1
                        d.atom2 = atom2
                        d.atom3 = atom3
                        d.atom4 = atom4

                        cont.append(d)
                    else:
                        raise TypeError

                elif conf['type'] == 'cmap':
                    _m = i * conf['n']
                    _n = i * conf['n'] + 1
                    _o = i * conf['n'] + 2
                    _p = i * conf['n'] + 3
                    _q = i * conf['n'] + 4
                    _r = i * conf['n'] + 5
                    _s = i * conf['n'] + 6
                    _t = i * conf['n'] + 7

                    cm = blocks.CMap()
                    atom1 = m.anumb_to_atom(int(f[_m]))
                    atom2 = m.anumb_to_atom(int(f[_n]))
                    atom3 = m.anumb_to_atom(int(f[_o]))
                    atom4 = m.anumb_to_atom(int(f[_p]))
                    atom5 = m.anumb_to_atom(int(f[_q]))
                    atom6 = m.anumb_to_atom(int(f[_r]))
                    atom7 = m.anumb_to_atom(int(f[_s]))
                    atom8 = m.anumb_to_atom(int(f[_t]))

                    if all([atom1, atom2, atom3, atom4, atom5, atom6, atom7, atom8]):
                        cm.atom1 = atom1
                        cm.atom2 = atom2
                        cm.atom3 = atom3
                        cm.atom4 = atom4
                        cm.atom5 = atom5
                        cm.atom6 = atom6
                        cm.atom7 = atom7
                        cm.atom8 = atom8

                        m.cmaps.append(cm)
                    else:
                        raise TypeError

                else:
                    raise ValueError("unknown type : '%s'" % conf['type'])

            return True

        else:
            # psffmt other than 'NAMD'
            raise NotImplementedError



if __name__ == '__main__':
    import sys, time

    ts = time.time()
    if len(sys.argv) == 2:
        p = PSFSystem(sys.argv[1], each_chain_is_molecule=True)
    elif len(sys.argv) == 3:
        p = PSFSystem(sys.argv[1], pdbfile=sys.argv[2], each_chain_is_molecule=False)
    dt = time.time() - ts

    print(p)
    print('> parsed in %4.1f seconds' % dt)



