

from pytopol.psf import PSFSystem
from pytopol import blocks
import os, logging


module_logger = logging.getLogger('mainapp.grotop')


class GroTop:
    pass


class SystemToGroTop(object):

    functions = {
        'charmm':{
             'bonds':      1,
             'angles':     5,
             'dihedrals':  9,
             'impropers':  2,
             'pairs':      1,
             'cmaps':      1,
        },
    }

    formats = {
        'atomtypes'    : '{:<7s} {:3d} {:>7.4f}   {:4.1f}   {:3s}     {:14.12f}     {:10.7f}  \n',
        'atoms'        : '{:6d} {:>10s} {:6d} {:6s} {:6s} {:6d} {:10.3f} {:10.3f} \n',
        'bondtypes'    : '{:5s}  {:5s}  {:1d}  {:6.4f}  {:6.1f}\n',
        'bonds'        : '{:3d}  {:3d}   {:1d}\n',
        'pairtypes'    : '{:6s} {:6s}   {:d}    {:14.12f}     {:14.12f}    \n',
        'pairs'        : '{:3d} {:3d}   {:1d}\n',
        'angletypes'   : '{:6s} {:6s} {:6s} {:1d}    {:8.4f}    {:10.5f}    {:9.5f}    {:11.5f}\n',
        'angles'       : '{:3d} {:3d} {:3d}   {:1d}\n',
        'dihedraltypes': '{:6s} {:6s} {:6s} {:6s}   {:1d}    {:6.2f}    {:10.5f}    {:d}\n',
        'dihedrals'    : '{:3d} {:3d} {:3d} {:3d}   {:1d}\n',
        'impropertypes': '{:6s} {:6s} {:6s} {:6s} {:1d} {:6.2f} {:8.4f} \n',
        'impropers'    : '{:3d} {:3d} {:3d} {:3d}   {:1d}\n',
    }


    toptemplate = ""
    toptemplate += "[ atomtypes ]    \n*ATOMTYPES*    \n"
    toptemplate += "[ pairtypes ]    \n*PAIRTYPES*    \n"
    toptemplate += "[ bondtypes ]    \n*BONDTYPES*    \n"
    toptemplate += "[ angletypes ]   \n*ANGLETYPES*   \n"
    toptemplate += "[ dihedraltypes ]\n*DIHEDRALTYPES*\n"
    toptemplate += "[ dihedraltypes ]\n*IMPROPERTYPES*\n"
    toptemplate += "[ cmaptypes ]    \n*CMAPTYPES*\n"

    itptemplate = ""
    itptemplate += "[ moleculetype ] \n*MOLECULETYPE* \n"
    itptemplate += "[ atoms ]        \n*ATOMS*        \n"
    itptemplate += "[ bonds ]        \n*BONDS*        \n"
    itptemplate += "[ pairs ]        \n*PAIRS*        \n"
    itptemplate += "[ angles ]       \n*ANGLES*       \n"
    itptemplate += "[ dihedrals ]    \n*DIHEDRALS*    \n"
    itptemplate += "[ dihedrals ]    \n*IMPROPERS*    \n"
    itptemplate += "[ cmap ]        \n*CMAPS*    \n"




    def __init__(self, psfsystem):
        self.lgr = logging.getLogger('mainapp.grotop.SystemToGroTop')
        self.lgr.debug(">> entering SystemToGroTop")

        self.system   = psfsystem
        self.assemble_topology()

        self.lgr.debug("<< leaving SystemToGroTop")


    @staticmethod
    def _redefine_atomtypes(mol):

        i = 1

        for atom in mol.atoms:
            atom.atomtype = 'at%03d' % i
            i += 1


    def assemble_topology(self, redefine_atom_types = False):

        self.lgr.debug("starting to assemble topology...")

        # check that we support the forcefield
        for m in self.system.molecules:
            assert m.forcefield in list(self.functions.keys())


        self.lgr.debug("generating a temporary molecule to create forcefield types...")
        _temp_mol = blocks.Molecule()

        for m in self.system.molecules:
            _temp_mol.atoms += m.atoms
            _temp_mol.bonds += m.bonds
            _temp_mol.angles += m.angles
            _temp_mol.dihedrals += m.dihedrals
            _temp_mol.impropers += m.impropers
            _temp_mol.cmaps    += m.cmaps

        _temp_mol.forcefield = self.system.molecules[0].forcefield

        if redefine_atom_types:
            self.lgr.debug("redefining the atom types")
            self._redefine_atomtypes(_temp_mol)

        self.lgr.debug("number of atoms in the '_temp_mol' is %d" % len(_temp_mol.atoms))

        top = '[ defaults ] ; \n'
        top += ';nbfunc    comb-rule    gen-pairs    fudgeLJ    fudgeQQ \n'

        if self.system.molecules[0].forcefield == 'charmm':
            top += '1          2           yes          1.0       1.0 \n'

        self.lgr.debug("making atom/pair/bond/angle/dihedral/improper types")
        top += self.toptemplate
        top = top.replace('*ATOMTYPES*',     ''.join( self._make_atomtypes(_temp_mol)) )
        top = top.replace('*PAIRTYPES*',     ''.join( self._make_pairtypes(_temp_mol)) )
        top = top.replace('*BONDTYPES*',     ''.join( self._make_bondtypes(_temp_mol)) )
        top = top.replace('*ANGLETYPES*',    ''.join( self._make_angletypes(_temp_mol)))
        top = top.replace('*DIHEDRALTYPES*', ''.join( self._make_dihedraltypes(_temp_mol)) )
        top = top.replace('*IMPROPERTYPES*', ''.join( self._make_impropertypes(_temp_mol)) )
        top = top.replace('*CMAPTYPES*',     ''.join( self._make_cmaptypes(_temp_mol)) )

        for i, m in enumerate(self.system.molecules):
            molname = 'mol_%02d' % (i+1)
            top += '#include "itp_%s.itp" \n' % molname

        top += '\n[system]  \nConvertedSystem\n\n'
        top += '[molecules] \n'

        for i, m in enumerate(self.system.molecules):
            molname = 'mol_%02d' % (i+1)
            top += '%s     1\n' % molname
        top += '\n'

        with open('top.top', 'w') as f:
            f.writelines([top])

        self.lgr.debug('writing top finished')


        # --------------


        self.lgr.debug("generating atom/pair/bond/angle/dihedral/improper for the itp files")


        for i,m in enumerate(self.system.molecules):
            molname = 'mol_%02d' % (i+1)
            itp = self.itptemplate
            itp = itp.replace('*MOLECULETYPE*',  ''.join( self._make_moleculetype(m, molname))  )
            itp = itp.replace('*ATOMS*',         ''.join( self._make_atoms(m))  )
            itp = itp.replace('*BONDS*',         ''.join( self._make_bonds(m))  )
            itp = itp.replace('*PAIRS*',         ''.join( self._make_pairs(m))  )
            itp = itp.replace('*ANGLES*',        ''.join( self._make_angles(m)) )
            itp = itp.replace('*DIHEDRALS*',     ''.join( self._make_dihedrals(m)) )
            itp = itp.replace('*IMPROPERS*',     ''.join( self._make_impropers(m)) )
            itp = itp.replace('*CMAPS*',         ''.join( self._make_cmaps(m)) )

            with open('itp_%s.itp' % molname, 'w') as f:
                f.writelines([itp])

        self.lgr.debug('writing %d itp files finished' % (i+1))




    def _make_atomtypes(self,m):
        def get_prot(at):
            # TODO improve this
            _protons = {'C':6, 'H':1, 'N':7, 'O':8, 'S':16, 'P':15}
            if at[0] in list(_protons.keys()):
                return _protons[at[0]]
            else:
                return 0


        _added = {}
        result = []
        for atom in m.atoms:
            at = atom.get_atomtype()
            if at in list(_added.keys()):
                assert _added[at] == (atom.mass, atom.lje, atom.ljl), '%s: %s != %s' % (at,
                        _added[at], (atom.mass, atom.lje, atom.ljl))
                continue

            # not checking atom.charge => it can be different for the same atom type
            _added[at] = (atom.mass, atom.lje, atom.ljl)

            prot = get_prot(at)
            line = self.formats['atomtypes'].format(
                    at, prot, atom.mass, atom.charge, 'A', atom.ljl, atom.lje)
            result.append(line)

        return result


    def _make_pairtypes(self,m):
        _added = {}
        result = []
        for dih in m.dihedrals:
            atom1 = dih.atom1
            atom4 = dih.atom4

            at1 = atom1.get_atomtype()
            at4 = atom4.get_atomtype()

            if m.forcefield == 'charmm':
                mix_e = lambda x, y: (x*y)**0.5
                mix_l = lambda x, y: (x+y)* 0.5

                if   hasattr(atom1, 'lje14') and hasattr(atom4, 'ljl14'):
                    e14 = mix_e(atom1.lje14, atom4.lje14)
                    l14 = mix_l(atom1.ljl14, atom4.ljl14)

                elif hasattr(atom1, 'lje14'):
                    e14 = mix_e(atom1.lje14, atom4.lje)
                    l14 = mix_l(atom1.ljl14, atom4.ljl)

                elif hasattr(atom4, 'lje14'):
                    e14 = mix_e(atom1.lje, atom4.lje14)
                    l14 = mix_l(atom1.ljl, atom4.ljl14)

                else:
                    continue
            else:
                raise NotImplementedError

            key = [at1,at4]
            key.sort()
            key = tuple(key)
            if key in list(_added.keys()):
                assert _added[key] == (e14, l14)
                continue

            _added[key] = (e14, l14)
            fu = self.functions[m.forcefield]['pairs']
            line = self.formats['pairtypes'].format(at1, at4, fu, l14, e14)
            result.append(line)

        return result


    def _make_bondtypes(self,m):
        _added = {}
        result = []
        for bond in m.bonds:
            at1 = bond.atom1.get_atomtype()
            at2 = bond.atom2.get_atomtype()

            key = [at1, at2]
            key.sort()
            key = tuple(key)

            if m.forcefield == 'charmm':
                kb, b0 =  bond.param.coeffs

            if key in list(_added.keys()):
                assert _added[key] == (kb,b0)
                continue

            _added[key] = (kb, b0)
            _added[key[::-1]] = (kb, b0)

            fu = self.functions[m.forcefield]['bonds']
            line = self.formats['bondtypes'].format(at1, at2, fu, b0, kb)
            result.append(line)

        return result


    def _make_angletypes(self,m):
        _added = {}
        result = []
        for ang in m.angles:
            at1 = ang.atom1.get_atomtype()
            at2 = ang.atom2.get_atomtype()
            at3 = ang.atom3.get_atomtype()

            key = [at1, at2, at3]
            #key.sort()
            key = tuple(key)

            if m.forcefield == 'charmm':
                ktetha, tetha0, kub, s0 = ang.param.coeffs

            if key in list(_added.keys()):
                assert _added[key] == (ktetha, tetha0, kub, s0), '%s -> %s != %s' % (key, _added[key],
                        (ktetha, tetha0, kub, s0))
                continue

            _added[key] = (ktetha, tetha0, kub, s0)
            _added[key[::-1]] = (ktetha, tetha0, kub, s0)

            fu = self.functions[m.forcefield]['angles']
            line = self.formats['angletypes'].format(at1, at2, at3, fu, tetha0, ktetha, s0, kub)
            result.append(line)

        return result

    def _make_dihedraltypes(self,m):
        _added = {}
        result = []
        for dih in m.dihedrals:
            at1 = dih.atom1.get_atomtype()
            at2 = dih.atom2.get_atomtype()
            at3 = dih.atom3.get_atomtype()
            at4 = dih.atom4.get_atomtype()

            key = [at1, at2, at3, at4]
            #key.sort()
            key = tuple(key)

            if m.forcefield == 'charmm':
                for coeff in dih.charmm_param:
                    kchi, n, delta = coeff

                    if key not in list(_added.keys()):
                        _added[key] = []
                        _added[key[::-1]] = []

                    if (kchi, n, delta) not in _added[key]:
                        _added[key].append((kchi, n, delta))
                        _added[key[::-1]].append((kchi, n, delta))
                        fu = self.functions[m.forcefield]['dihedrals']
                        line = self.formats['dihedraltypes'].format(
                                at1, at2, at3, at4, fu, delta, kchi, n)
                        result.append(line)
                    else:
                        continue

        return result

    def _make_impropertypes(self,m):
        _added = {}
        result = []
        for imp in m.impropers:
            at1 = imp.atom1.get_atomtype()
            at2 = imp.atom2.get_atomtype()
            at3 = imp.atom3.get_atomtype()
            at4 = imp.atom4.get_atomtype()

            key = [at1, at2, at3, at4]
            #key.sort()
            key = tuple(key)

            if m.forcefield == 'charmm':
                kpsi, psi0 = imp.param.coeffs

            if key in list(_added.keys()):
                assert _added[key] == (kpsi, psi0)
                continue

            _added[key] = (kpsi, psi0)
            _added[key[::-1]] = (kpsi, psi0)

            fu = self.functions[m.forcefield]['impropers']
            line = self.formats['impropertypes'].format(at1, at2, at3, at4, fu, psi0, kpsi)
            result.append(line)

        return result

    def _make_cmaptypes(self, m):
        _added = []
        result = []
        for cmap in m.cmaps:
            at1 = cmap.atom1.get_atomtype()
            at2 = cmap.atom2.get_atomtype()
            at3 = cmap.atom3.get_atomtype()
            at4 = cmap.atom4.get_atomtype()
            at5 = cmap.atom5.get_atomtype()
            at6 = cmap.atom6.get_atomtype()
            at7 = cmap.atom7.get_atomtype()
            at8 = cmap.atom8.get_atomtype()

            key = (at1, at2, at3, at4, at5, at6, at7, at8)
            if key in _added:
                continue
            _added.append(key)

            fu = self.functions[m.forcefield]['cmaps']
            line = '%s %s %s %s %s %d 24 24' % (at1, at2, at3, at4, at8, fu)
            for i,c in enumerate(cmap.param.coeffs):
                if i%10 == 0:
                    line += '\\\n'
                else:
                    line += ' '
                line += '%0.8f' % c

            line += '\n\n'
            result.append(line)

        return result



    def _make_moleculetype(self,m, molname):
        return ['; Name \t\t  nrexcl \n %s    3 \n' % molname]

    def _make_atoms(self,m):
        result = []
        i = 1
        for atom in m.atoms:
            numb = cgnr = atom.number
            atype = atom.get_atomtype()
            assert atype!= False and hasattr(atom, 'charge') and hasattr(atom, 'mass')
            line = self.formats['atoms'].format(
                    numb, atype, atom.residue.number, atom.residue.name, atom.name, cgnr, atom.charge, atom.mass)
            result.append(line)

        result.insert(0,'; %5d atoms\n' % len(result))
        return result

    def _make_pairs(self,m):
        _bonds = []
        for bond in m.bonds:
            _bonds.append((bond.atom1.number, bond.atom2.number))

        _angles = []
        for ang in m.angles:
            _angles.append((ang.atom1.number, ang.atom3.number))

        _bonds = set(_bonds)
        _angles = set(_angles)

        _pairs = []

        result = []
        for dih in m.dihedrals:
            fu = self.functions[m.forcefield]['pairs']
            p1 = dih.atom1.number
            p4 = dih.atom4.number

            if (p1,p4) in _bonds or (p1,p4) in _angles or \
               (p4,p1) in _bonds or (p4,p1) in _angles:
                continue

            if (p1,p4) in _pairs or (p4,p1) in _pairs:
                continue

            _pairs.append((p1,p4))

            line = self.formats['pairs'].format(p1, p4, fu)
            result.append(line)

        result.insert(0,'; %5d pairs\n' % len(result))
        return result


    def _make_bonds(self,m):
        result = []
        for bond in m.bonds:
            fu = self.functions[m.forcefield]['bonds']
            line = self.formats['bonds'].format(bond.atom1.number, bond.atom2.number, fu)
            result.append(line)

        result.insert(0,'; %5d bonds\n' % len(result))
        return result

    def _make_angles(self,m):
        result = []
        for ang in m.angles:
            fu = self.functions[m.forcefield]['angles']
            line = self.formats['angles'].format(ang.atom1.number, ang.atom2.number, ang.atom3.number, fu)
            result.append(line)

        result.insert(0,'; %5d angles\n' % len(result))
        return result

    def _make_dihedrals(self,m):
        result = []
        for dih in m.dihedrals:
            fu = self.functions[m.forcefield]['dihedrals']
            line = self.formats['dihedrals'].format(
                    dih.atom1.number, dih.atom2.number, dih.atom3.number, dih.atom4.number, fu)
            result.append(line)

        result.insert(0,'; %5d dihedrals\n' % len(result))
        return result

    def _make_impropers(self,m):
        result = []
        for imp in m.impropers:
            fu = self.functions[m.forcefield]['impropers']
            line = self.formats['impropers'].format(
                    imp.atom1.number, imp.atom2.number, imp.atom3.number, imp.atom4.number, fu)
            result.append(line)

        result.insert(0,'; %5d impropers\n' % len(result))
        return result

    def _make_cmaps(self, m):
        result = []

        for cmap in m.cmaps:
            fu = self.functions[m.forcefield]['cmaps']
            line = '%5d %5d %5d %5d %5d   %d\n' % (
                cmap.atom1.number, cmap.atom2.number, cmap.atom3.number, cmap.atom4.number,
                cmap.atom8.number, fu)
            result.append(line)

        result.insert(0,'; %5d cmaps\n' % len(result))
        return result









