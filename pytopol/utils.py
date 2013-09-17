import logging
from pytopol import blocks

lgr = logging.getLogger('mainapp.utils')


def build_res_chain(m):
    # using a molecule object with atoms, builds residues and chains
    R = None
    residues = []
    for i, a in enumerate(m.atoms):
        if R is None or (a.resname  != R.name or
                          a.resnumb != R.number or
                          a.chain   != R.chain_name):
            R = blocks.Residue()
            R.name = a.resname
            R.number = a.resnumb
            R.chain_name  = a.chain
            residues.append(R)

        R.atoms.append(a)
        a.residue = R

    m.residues = residues

    # chains
    C = None   # current chain object
    chains = []
    for i, r in enumerate(m.residues):
        if C is None or (r.chain_name != C.name):
            C = blocks.Chain()
            C.name = r.chain_name
            chains.append(C)

        C.residues.append(r)
        r.chain = C

    m.chains = chains

def build_pairs(m):
    # using a molecule with bonds, angles and dihedrals, build pairs
    print('building pairs with %d bonds, %d angles and %d dihedrals' % (
        len(m.bonds), len(m.angles), len(m.dihedrals)))

    _bonds = []
    for bond in m.bonds:
        _bonds.append((bond.atom1.number, bond.atom2.number))

    _angles = []
    for ang in m.angles:
        _angles.append((ang.atom1.number, ang.atom3.number))

    _bonds = set(_bonds)
    _angles = set(_angles)

    _pairs = set([])
    for dih in m.dihedrals:
        p1 = dih.atom1.number
        p4 = dih.atom4.number

        if (p1,p4) in _bonds or (p1,p4) in _angles or \
           (p4,p1) in _bonds or (p4,p1) in _angles:
            continue

        if (p1,p4) in _pairs or (p4,p1) in _pairs:
            continue

        _pairs.add((p1,p4))

        thispair = blocks.Pair()
        thispair.atom1 = dih.atom1
        thispair.atom2 = dih.atom4

        m.pairs.append(thispair)







