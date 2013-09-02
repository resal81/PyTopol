
from pytopol import charmmpar
from config import par_files as ref

# set up the charmmpars
pars = {}
for name in list(ref.keys()):
    path = ref[name]['path']
    pars[name] = charmmpar.CharmmPar(path)


def test_nbonds():
	for name in list(ref.keys()):
		assert len(pars[name].bondpars) == ref[name]['nbonds']


def test_nangles():
	for name in list(ref.keys()):
		assert len(pars[name].anglepars) == ref[name]['nangles']

def test_dihedrals():
	for name in list(ref.keys()):
		ndih = sum([len(v) for v in list(pars[name].dihedralpars._data.values())])
		assert ndih == ref[name]['ndihedrals']

def test_nimpropers():
	for name in list(ref.keys()):
		assert len(pars[name].improperpars) == ref[name]['nimpropers']

def test_nnonbonding():
	for name in list(ref.keys()):
		assert len(pars[name].nonbonding) == ref[name]['nnonbonding']

def test_ncmaps():
	for name in list(ref.keys()):
		assert len(pars[name].cmappars) == ref[name]['ncmaps']

