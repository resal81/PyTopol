
from pytopol import psf
from config import psf_files as ref


# set up the systems
psf_systems = {}
for name in list(ref.keys()):
    path = ref[name]['path']
    psf_systems[name] = psf.PSFSystem(path, each_chain_is_molecule=True)


def test_parsing_psf_files():
    assert psf_systems != {}
    for name in list(psf_systems.keys()):
        assert isinstance(psf_systems[name].molecules, tuple)
        assert len(psf_systems[name].molecules) == ref[name]['nmolecules']

def test_nmolecules():
    for name in list(psf_systems.keys()):
        assert len(psf_systems[name].molecules) == ref[name]['nmolecules']

def test_natoms():
    for name in list(psf_systems.keys()):
        natoms = sum([len(m.atoms) for m in psf_systems[name].molecules])
        assert natoms == ref[name]['natoms']

def test_nresidues():
    for name in list(psf_systems.keys()):
        nresidues = sum([len(m.residues) for m in psf_systems[name].molecules])
        assert nresidues == ref[name]['nresidues']

def test_nchains():
    for name in list(psf_systems.keys()):
        nchains = sum([len(m.chains) for m in psf_systems[name].molecules])
        assert nchains == ref[name]['nchains']

def test_nbonds():
    for name in list(psf_systems.keys()):
        nbonds = sum([len(m.bonds) for m in psf_systems[name].molecules])
        assert nbonds == ref[name]['nbonds']

def test_nangles():
    for name in list(psf_systems.keys()):
        nangles = sum([len(m.angles) for m in psf_systems[name].molecules])
        assert nangles == ref[name]['nangles']

def test_ndihedrals():
    for name in list(psf_systems.keys()):
        ndihedrals = sum([len(m.dihedrals) for m in psf_systems[name].molecules])
        assert ndihedrals == ref[name]['ndihedrals']

def test_nimpropers():
    for name in list(psf_systems.keys()):
        nimpropers = sum([len(m.impropers) for m in psf_systems[name].molecules])
        assert nimpropers == ref[name]['nimpropers']



