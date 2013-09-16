

class Molecule(object):

    def __init__(self):
        self.chains    = []
        self.atoms     = []
        self.residues  = []

        self.atomtypes = []

        self.bonds     = []
        self.angles    = []
        self.dihedrals = []
        self.impropers = []
        self.cmaps     = []
        self.londons   = []

        self.forcefield=  None
        self._anumb_to_atom = {}


    def anumb_to_atom(self, anumb):
        '''Returns the atom object corresponding to an atom number'''

        assert isinstance(anumb, int), "anumb must be integer"

        if len(self._anumb_to_atom) == 0:   # empty dictionary

            if len(self.atoms) != 0:
                for atom in self.atoms:
                    self._anumb_to_atom[atom.number] = atom
                return self._anumb_to_atom[anumb]
            else:
                print("no atoms in the molecule")
                return False

        else:
            if anumb in self._anumb_to_atom:
                return self._anumb_to_atom[anumb]
            else:
                print("no such atom number (%d) in the molecule" % (anumb))
                return False


    def renumber_atoms(self):

        if len(self.atoms) != 0:

            # reset the mapping
            self._anumb_to_atom = {}

            for i,atom in enumerate(self.atoms):
                atom.number = i+1   # starting from 1

        else:
            print("the number of atoms is zero - no renumbering")


class Chain(object):
    """
        name    = str,
        residues= list,
        molecule= Molecule
    """

    def __init__(self):
        self.residues = []


class Residue(object):
    """
        name    = str,
        number  = int,
        chain   = Chain,
        chain_name = str,
        atoms   = list,
    """

    def __init__(self):
        self.atoms  = []


class Atom(object):
    """
        name    = str,
        number  = int,
        flag    = str,        # HETATM
        coords  = list,
        residue = Residue,
        occup   = float,
        bfactor = float,
        altlocs = list,
        atomtype= str,
        radius  = float,
        charge  = radius,
        mass    = float,
        chain   = str,
        resname = str,
        resnumb = int,
        altloc  = str,         # per atoms

    """

    def __init__(self):

        self.coords = []        # a list of coordinates (x,y,z) of models
        self.altlocs= []        # a list of (altloc_name, (x,y,z), occup, bfactor)




    def get_atomtype(self):
        if hasattr(self, 'atomtype'):
            return self.atomtype
        else:
            print("atom %s doesn't have atomtype" % self)
            return False



class Bond:
    def __init__(self):
        self.atom1 = None
        self.atom2 = None

class Angle:
    def __init__(self):
        self.atom1 = None
        self.atom2 = None
        self.atom3 = None

class Dihedral:
    def __init__(self):
        self.atom1 = None
        self.atom2 = None
        self.atom3 = None
        self.atom4 = None

class Improper:
    def __init__(self):
        self.atom1 = None
        self.atom2 = None
        self.atom3 = None
        self.atom4 = None

class CMap:
    def __init__(self):
        self.atom1 = None
        self.atom2 = None
        self.atom3 = None
        self.atom4 = None
        self.atom5 = None
        self.atom6 = None
        self.atom7 = None
        self.atom8 = None



class Param:
    def convert(self, reqformat):
        assert reqformat in ('charmm', 'gromacs')

        if reqformat == self.format:
            if reqformat == 'charmm':
                return self.charmm
            elif reqformat == 'gromacs':
                return self.gromacs
            else:
                raise NotImplementedError

        if isinstance(self, AtomType):
            if reqformat == 'gromacs' and self.format == 'charmm':
                pass
            else:
                raise NotImplementedError

        elif isinstance(self, BondType):
            if reqformat == 'gromacs' and self.format == 'charmm':
                pass
            else:
                raise NotImplementedError

        elif isinstance(self, AngleType):
            if reqformat == 'gromacs' and self.format == 'charmm':
                pass
            else:
                raise NotImplementedError

        elif isinstance(self, DihedralType):
            if reqformat == 'gromacs' and self.format == 'charmm':
                pass
            else:
                raise NotImplementedError

        elif isinstance(self, ImproperType):
            if reqformat == 'gromacs' and self.format == 'charmm':
                pass
            else:
                raise NotImplementedError

        elif isinstance(self, CMapType):
            if reqformat == 'gromacs' and self.format == 'charmm':
                pass
            else:
                raise NotImplementedError

        elif isinstance(self, InteractionType):
            if reqformat == 'gromacs' and self.format == 'charmm':
                pass
            else:
                raise NotImplementedError

        else:
            raise NotImplementedError


class AtomType(Param):
    def __init__(self, format):
        assert format in ('charmm', 'gromacs')
        self.format = format
        self.atype  = None
        self.mass   = None

        self.charmm = {'param': {'lje':None, 'ljl':None, 'lje14':None, 'ljl14':None} }
        self.gromacs= {'param': {'lje':None, 'ljl':None, 'lje14':None, 'ljl14':None} }


class BondType(Param):
    def __init__(self, format):
        assert format in ('charmm', 'gromacs')
        self.format = format
        self.atype1 = None
        self.atype2 = None

        self.charmm = {'param': {} }
        self.gromacs= {'param': {}, 'func':None}


class AngleType(Param):
    def __init__(self, format):
        assert format in ('charmm', 'gromacs')
        self.format = format

        self.atype1 = None
        self.atype2 = None
        self.atype3 = None

        self.charmm = {}
        self.gromacs= {}


class DihedralType(Param):
    def __init__(self, format):
        assert format in ('charmm', 'gromacs')
        self.format = format

        self.atype1 = None
        self.atype2 = None
        self.atype3 = None
        self.atype4 = None

        self.charmm = {}
        self.gromacs= {}


class ImproperType(Param):
    def __init__(self, format):
        assert format in ('charmm', 'gromacs')
        self.format = format

        self.atype1 = None
        self.atype2 = None
        self.atype3 = None
        self.atype4 = None

        self.charmm = {}
        self.gromacs= {}


class CMapType(Param):
    def __init__(self, format):
        assert format in ('charmm', 'gromacs')
        self.format = format

        self.atype1 = None
        self.atype2 = None
        self.atype3 = None
        self.atype4 = None
        self.atype5 = None
        self.atype6 = None
        self.atype7 = None
        self.atype8 = None

        self.charmm = {}
        self.gromacs= {}


class InteractionType(Param):
    def __init__(self, format):
        assert format in ('charmm', 'gromacs')
        self.format = format

        self.atype1 = None
        self.atype2 = None

        self.charmm = {'param': {'lje':None, 'ljl':None, 'lje14':None, 'ljl14':None} }
        self.gromacs= {'param': {'lje':None, 'ljl':None, 'lje14':None, 'ljl14':None} }

