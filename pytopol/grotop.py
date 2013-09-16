

import logging

module_logger = logging.getLogger('mainapp.grotop')


class GroTop:
    pass


class SystemToGroTop(object):

    formats = {
        'atomtypes'    : '{:<7s} {:3d} {:>7.4f}   {:4.1f}   {:3s}     {:14.12f}     {:10.7f}  \n',
        'atoms'        : '{:6d} {:>10s} {:6d} {:6s} {:6s} {:6d} {:11.4f} {:11.4f} \n',
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
    toptemplate += "[ atomtypes ]      \n*ATOMTYPES*    \n"
    toptemplate += "[ nonbond_params ] \n*NONBOND_PARAM* \n"
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

        top = '[ defaults ] ; \n'
        top += ';nbfunc    comb-rule    gen-pairs    fudgeLJ    fudgeQQ \n'

        if self.system.forcefield == 'charmm':
            top += '1          2           yes          1.0       1.0 \n'

        self.lgr.debug("making atom/pair/bond/angle/dihedral/improper types")
        top += self.toptemplate
        top = top.replace('*ATOMTYPES*',     ''.join( self._make_atomtypes(self.system)) )
        top = top.replace('*NONBOND_PARAM*', ''.join( self._make_nonbond_param(self.system)) )
        top = top.replace('*PAIRTYPES*',     ''.join( self._make_pairtypes(self.system)) )
        top = top.replace('*BONDTYPES*',     ''.join( self._make_bondtypes(self.system)) )
        top = top.replace('*ANGLETYPES*',    ''.join( self._make_angletypes(self.system)))
        top = top.replace('*DIHEDRALTYPES*', ''.join( self._make_dihedraltypes(self.system)) )
        top = top.replace('*IMPROPERTYPES*', ''.join( self._make_impropertypes(self.system)) )
        top = top.replace('*CMAPTYPES*',     ''.join( self._make_cmaptypes(self.system)) )

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

        result = []
        for at in m.atomtypes:
            at.convert('gromacs')
            prot = get_prot(at.atype)
            ljl  = at.gromacs['param']['ljl']
            lje  = at.gromacs['param']['lje']
            line = self.formats['atomtypes'].format(at.atype, prot, at.mass, at.charge, 'A', ljl, lje)
            result.append(line)

        return result

    def _make_nonbond_param(self, m):
        result = []
        for pr in m.interactiontypes:
            at1 = pr.atype1
            at2 = pr.atype2

            pr.convert('gromacs')
            eps = pr.gromacs['param']['lje']
            sig = pr.gromacs['param']['ljl']

            fu = 1  # TODO
            line = self.formats['pairtypes'].format(at1, at2, fu, sig, eps)
            result.append(line)

        return result

    def _make_pairtypes(self,m):

        if m.forcefield == 'charmm':
            mix_e = lambda x, y: (x*y)**0.5
            mix_l = lambda x, y: (x+y)* 0.5


        inter_at_types = {(h.atype1, h.atype2):h for h in m.interactiontypes}
        inter_keys = list(inter_at_types.keys())

        result = []
        for i in range(len(m.atomtypes)):
            m.atomtypes[i].convert('gromacs')

            for j in range(i, len(m.atomtypes)):
                m.atomtypes[j].convert('gromacs')

                at1 = m.atomtypes[i].atype
                at2 = m.atomtypes[j].atype

                if (at1, at2) in inter_keys:
                    inter_at_types[(at1,at2)].convert('gromacs')
                    e14 = inter_at_types[(at1,at2)].gromacs['param']['lje']
                    l14 = inter_at_types[(at1,at2)].gromacs['param']['ljl']
                elif (at2, at1) in inter_keys:
                    inter_at_types[(at2,at1)].convert('gromacs')
                    e14 = inter_at_types[(at2,at1)]['param']['lje']
                    l14 = inter_at_types[(at2,at1)]['param']['ljl']
                else:
                    i_lje14 = m.atomtypes[i].gromacs['param']['lje14']
                    j_lje14 = m.atomtypes[j].gromacs['param']['lje14']
                    i_ljl14 = m.atomtypes[i].gromacs['param']['ljl14']
                    j_ljl14 = m.atomtypes[j].gromacs['param']['ljl14']

                    if i_lje14 and j_lje14:
                        e14 = mix_e(i_lje14, j_lje14)
                        l14 = mix_l(i_ljl14, j_ljl14)
                    elif i_lje14:
                        j_lje = m.atomtypes[j].gromacs['param']['lje']
                        j_ljl = m.atomtypes[j].gromacs['param']['ljl']
                        e14 = mix_e(i_lje14, j_lje)
                        l14 = mix_l(i_ljl14, j_ljl)
                    elif j_lje14:
                        i_lje = m.atomtypes[i].gromacs['param']['lje']
                        i_ljl = m.atomtypes[i].gromacs['param']['ljl']
                        e14 = mix_e(i_lje, j_lje14)
                        l14 = mix_l(i_ljl, j_ljl14)
                    else:
                        continue

                fu = 1 # TODO

                line = self.formats['pairtypes'].format(at1, at2, fu, l14, e14)
                result.append(line)

        return result


    def _make_bondtypes(self,m):
        result = []
        for bond in m.bondtypes:
            at1 = bond.atype1
            at2 = bond.atype2
            bond.convert('gromacs')

            kb = bond.gromacs['param']['kb']
            b0 = bond.gromacs['param']['b0']
            fu = bond.gromacs['func']

            line = self.formats['bondtypes'].format(at1, at2, fu, b0, kb)
            result.append(line)

        return result


    def _make_angletypes(self,m):
        result = []
        for ang in m.angletypes:
            at1 = ang.atype1
            at2 = ang.atype2
            at3 = ang.atype3
            ang.convert('gromacs')

            ktetha = ang.gromacs['param']['ktetha']
            tetha0 = ang.gromacs['param']['tetha0']
            kub    = ang.gromacs['param']['kub']
            s0     = ang.gromacs['param']['s0']

            fu = ang.gromacs['func']

            line = self.formats['angletypes'].format(at1, at2, at3, fu, tetha0, ktetha, s0, kub)
            result.append(line)

        return result

    def _make_dihedraltypes(self,m):
        result = []
        for dih in m.dihedraltypes:
            at1 = dih.atype1
            at2 = dih.atype2
            at3 = dih.atype3
            at4 = dih.atype4

            dih.convert('gromacs')
            fu = dih.gromacs['func']

            for dpar in dih.gromacs['param']:
                kchi = dpar['kchi']
                n    = dpar['n']
                delta= dpar['delta']

                line = self.formats['dihedraltypes'].format(at1, at2, at3, at4, fu, delta, kchi, n)
                result.append(line)

        return result

    def _make_impropertypes(self,m):
        result = []
        for imp in m.impropertypes:
            at1 = imp.atype1
            at2 = imp.atype2
            at3 = imp.atype3
            at4 = imp.atype4
            imp.convert('gromacs')

            kpsi = imp.gromacs['param']['kpsi']
            psi0 = imp.gromacs['param']['psi0']

            fu = imp.gromacs['func']
            line = self.formats['impropertypes'].format(at1, at2, at3, at4, fu, psi0, kpsi)
            result.append(line)

        return result

    def _make_cmaptypes(self, m):
        result = []
        for cmap in m.cmaptypes:
            at1 = cmap.atype1
            at2 = cmap.atype2
            at3 = cmap.atype3
            at4 = cmap.atype4
            at5 = cmap.atype5
            at6 = cmap.atype6
            at7 = cmap.atype7
            at8 = cmap.atype8

            cmap.convert('gromacs')

            fu = cmap.gromacs['func']
            line = '%s %s %s %s %s %d 24 24' % (at1, at2, at3, at4, at8, fu)
            for i,c in enumerate(cmap.gromacs['param']):
                if i%10 == 0:
                    line += '\\\n'
                else:
                    line += ' '
                line += '%12.8f' % c

            line += '\n\n'
            result.append(line)

        return result

    def _make_moleculetype(self,m, molname):
        return ['; Name \t\t  nrexcl \n %s    3 \n' % molname]

    def _make_atoms(self,m):
        result = []
        #i = 1
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

        result = []
        for pr in m.pairs:
            fu = 1
            p1 = pr.atom1.number
            p4 = pr.atom2.number

            line = self.formats['pairs'].format(p1, p4, fu)
            result.append(line)

        result.insert(0,'; %5d pairs\n' % len(result))
        return result


    def _make_bonds(self,m):
        result = []
        for bond in m.bonds:
            fu = 1
            line = self.formats['bonds'].format(bond.atom1.number, bond.atom2.number, fu)
            result.append(line)

        result.insert(0,'; %5d bonds\n' % len(result))
        return result

    def _make_angles(self,m):
        result = []
        for ang in m.angles:
            fu = 5
            line = self.formats['angles'].format(ang.atom1.number, ang.atom2.number, ang.atom3.number, fu)
            result.append(line)

        result.insert(0,'; %5d angles\n' % len(result))
        return result

    def _make_dihedrals(self,m):
        result = []
        for dih in m.dihedrals:
            fu = 9
            line = self.formats['dihedrals'].format(
                    dih.atom1.number, dih.atom2.number, dih.atom3.number, dih.atom4.number, fu)
            result.append(line)

        result.insert(0,'; %5d dihedrals\n' % len(result))
        return result

    def _make_impropers(self,m):
        result = []
        for imp in m.impropers:
            fu = 2
            line = self.formats['impropers'].format(
                    imp.atom1.number, imp.atom2.number, imp.atom3.number, imp.atom4.number, fu)
            result.append(line)

        result.insert(0,'; %5d impropers\n' % len(result))
        return result

    def _make_cmaps(self, m):
        result = []

        for cmap in m.cmaps:
            fu = 1
            line = '%5d %5d %5d %5d %5d   %d\n' % (
                cmap.atom1.number, cmap.atom2.number, cmap.atom3.number, cmap.atom4.number,
                cmap.atom8.number, fu)
            result.append(line)

        result.insert(0,'; %5d cmaps\n' % len(result))
        return result









