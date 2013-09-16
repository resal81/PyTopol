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


def build_londons(m):
    # the m.atomtypes must be present

    assert len(set(m.atomtypes)) == len(m.atomtypes)   # sanity check - no duplicates

    for i in range(len(m.atomtypes)):
        for j in range(len(m.atomtypes)):
            london = blocks.london()
            pass






