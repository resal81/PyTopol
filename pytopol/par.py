

from collections import defaultdict
import logging

module_logger = logging.getLogger('mainapp.par')

class ParType(object):
    '''
    For CHARMM, the self.data is a dictionary with the following format:

        - bonds
                !V(bond) = Kb(b - b0)**2
                !
                !Kb: kcal/mole/A**2
                !b0: A
                !
                !atom type Kb          b0

            self.data = { (atype1, atype2) : [ (Kb, b0 ) ] }

        - angles
                !V(angle) = Ktheta(Theta - Theta0)**2
                !
                !V(Urey-Bradley) = Kub(S - S0)**2
                !
                !Ktheta: kcal/mole/rad**2
                !Theta0: degrees
                !Kub: kcal/mole/A**2 (Urey-Bradley)
                !S0: A
                !
                !atom types     Ktheta    Theta0   Kub     S0

            self.data = { (atype1, atype2, atype3) : [ (Ktheta, Theta0, Kub or None, S0 or None) ]


        - dihedrals
                !V(dihedral) = Kchi(1 + cos(n(chi) - delta))
                !
                !Kchi: kcal/mole
                !n: multiplicity
                !delta: degrees
                !
                !atom types             Kchi    n   delta

            self.data = { (atype1, atype2, atype3, atype4) : [ (Kchi, n, delta) ]


        - impropers
                !V(improper) = Kpsi(psi - psi0)**2
                !
                !Kpsi: kcal/mole/rad**2
                !psi0: degrees
                !note that the second column of numbers (0) is ignored
                !
                !atom types           Kpsi    ignored        psi0

            self.data = { (atype1, atype2, atype3, atype4) : [ (Kpsi, psi0) ]


        - nonbonding
                !V(Lennard-Jones) = Eps,i,j[(Rmin,i,j/ri,j)**12 - 2(Rmin,i,j/ri,j)**6]
                !
                !epsilon: kcal/mole, Eps,i,j = sqrt(eps,i * eps,j)
                !Rmin/2: A, Rmin,i,j = Rmin/2,i + Rmin/2,j
                !
                !atom  ignored    epsilon      Rmin/2   ignored   eps,1-4       Rmin/2,1-4

            self.data = { atype : [ (epsilon, Rmin/2, eps14 or None, Rmin14 or None) ] }

    '''



    def __init__(self, sym=False, mult=False, name=''):
        self.symmetric_keys         = sym
        self.multiple_value_per_key = mult

        assert name in ['bond', 'angle', 'dihedral', 'improper', 'nonbonding', 'cmap']
        self.name = name

        self._data = defaultdict(list)      # (atype1, atype2) : [(coeffs)]
        self._key_set = set()

        self.lgr = logging.getLogger('mainapp.par.Par')


    def __len__(self):
        return len(self._data)


    def add_parameter(self, key, value):
        if self.multiple_value_per_key:
            # no check - append new values
            self._data[key].append(value)
        else:
            # no mutliple values - maximum one value per key - either write or overwrite
            key1 = key
            key2 = key[::-1] if (isinstance(key, tuple) and self.symmetric_keys) else key

            old_keys = list(self._data.keys())

            if not key1 in old_keys and not key2 in old_keys:
                self._data[key1].append(value)
            else:
                key = key1 if key1 in old_keys else key2
                if self._data[key][0] != value:
                    self.lgr.warning('overwritten: %s -> key: %s' % ( self.name, key))
                    self.lgr.warning('  from: %s, to: %s' % (self._data[key], value))
                    self._data[key][0] = value


    def get_parameter(self, key):
        if len(self._key_set) == 0 and len(list(self._data.keys())) > 0:
            self._key_set = set(self._data.keys())


        if key in self._key_set:
            return self._data[key]
        else:
            if isinstance(key, tuple) and self.symmetric_keys:
                if key[::-1] in self._key_set:
                    return self._data[key[::-1]]

        return []



    def get_charmm_dihedral_wildcard(self, key):
        # X-atomtype2-atomtype3-X
        result = self.get_parameter(key)
        if result != []:
            return result
        else:
            return self.get_parameter( ('X', key[1], key[2], 'X') )


    def get_charmm_improper_wildcard(self,key):
        # atomtype1-X-X-atomtype4
        result = self.get_parameter(key)
        if result != []:
            return result
        else:
            return self.get_parameter( (key[0], 'X', 'X', key[3]) )

