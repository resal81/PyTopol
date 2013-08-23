
from pytopol import blocks
from pytopol.utils import build_res_chain
import os, logging, time



module_logger = logging.getLogger('mainapp.pdb')



class PDBSystem(object):

    def __init__(self, pdbfile, guess_mols=False):
        """ PDB parser.

        Attributes:
            pdbfile : str, path to the pdb file
            molecules: tuple Molecules
            atoms : tuple of Atoms
            lgt : logging.Logger

        """


        self.lgr = logging.getLogger('mainapp.pdb.PDBSystem')
        self.lgr.debug(">> entering PDBSystem")

        self.pdbfile = pdbfile
        self.atoms   = tuple([])
        self.molecules = tuple([])

        self._parse(self.pdbfile, guess_mols)

        self.lgr.debug("<< leaving PDBsystem")

    def _parse(self, pdbfile, guess_mols):
        self.lgr.debug("parsing pdb file: %s" % pdbfile)

        t1 = time.time()

        if not os.path.exists(pdbfile):
            self.lgr.error("the pdbfile doesn't exist")
            return

        _first_model_finished = False
        atoms     = []
        molecules = []
        _i = 0   # a counter for atom index
        _alt_loc_warning = False

        # read the file and create atoms list
        M = blocks.Molecule()
        molecules.append(M)
        with open(pdbfile) as f:
            for line in f:
                line = line.strip()
                if line.startswith('ENDMDL'):
                    _first_model_finished = True   # set by first ENDMDL
                    _i = 0   # reset _i

                if _first_model_finished:
                    # just read the coordinates
                    if line.startswith(('ATOM', 'HETATM')):
                        c = list(map(float, (line[30:38], line[38:46], line[46:54])))
                        atoms[_i].coords.append(c)
                        _i += 1
                else:
                    if line.startswith(('ATOM', 'HETATM')):
                        a = blocks.Atom()
                        a.flag   = line[0:6].strip()
                        a.number = self.conv_atom_number(line[6:11])
                        a.name   = line[12:16].strip()
                        a.altloc = line[16].strip()
                        if a.altloc != '' and _alt_loc_warning is False:
                            _alt_loc_warning = True
                        a.resname= line[17:21].strip()
                        a.chain  = line[21].strip()
                        a.resnumb= int(line[22:26])
                        c = list(map(float, (line[30:38], line[38:46], line[46:54])))
                        a.coords = [tuple(c)]  # a list of (x,y,z) tuples, each tuple for one model

                        #TODO occup, bfactor, ...

                        if guess_mols:
                            if len(atoms) > 0:
                                if line.startswith('HETATM'):
                                    if a.resname != atoms[-1].resname or a.resnumb != atoms[-1].resnumb:
                                        M = blocks.Molecule()
                                        molecules.append(M)
                                else: # ATOM
                                    if atoms[-1].flag == 'HETATM':
                                        M = blocks.Molecule()
                                        molecules.append(M)

                        # record a in the local atoms and M.atoms
                        atoms.append(a)
                        M.atoms.append(a)

        if len(atoms) == 0:
            self.lgr.warning("no atoms were found in the pdb file")
            return

        self.atoms = tuple(atoms)

        if _alt_loc_warning:
            self.lgr.warning("there are atom records with altloc flags - fix this")

        # make sure all the atomic coordinates are the same length
        for a in atoms:
            assert len(a.coords) == len(atoms[0].coords)

        # build residue and chains
        for m in molecules:
            build_res_chain(m)

        self.molecules = tuple(molecules)


        t2 = time.time()
        self.lgr.debug("parsing took %4.1f seconds" % (t2-t1))

    @staticmethod
    def conv_atom_number(s):
        try:
            numb = int(s)
        except ValueError:
            numb = int(s, 16)
        return numb

    def __repr__(self):
        natoms = sum([len(m.atoms) for m in self.molecules])
        return "PDBSystem with %6d atoms and %2d molecules" % (natoms, len(self.molecules))







if __name__ == '__main__':
    import sys, time

    t1 = time.time()
    p = PDBSystem(sys.argv[1])
    dt = time.time() - t1
    print(p)
    print('> parsed in %4.1f seconds' % dt)




