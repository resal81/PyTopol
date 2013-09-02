
import os


pdb_files = {
    '2M0Z': {
         'path': os.path.abspath(os.path.join('tests/data/pdb', '2M0Z.pdb')),
         'nmolecules':2,
         'nchains':2,
         'nresidues':98,
         'natoms':1468,
         'nmodels':20,
     },
}


psf_files = {
    '1lyz': {
         'path': os.path.abspath(os.path.join('test/systems/protein', '1lyz_nowat_autopsf.psf')),
         'nmolecules':1,
         'nchains':1,
         'nresidues':129,
         'natoms':1966,
         'nbonds': 1987,
         'nangles':3547,
         'ndihedrals':5184,
         'nimpropers':351,
    },
}

par_files = {
    'chol': {
        'path': os.path.abspath(os.path.join('test/systems/par', 'par_chol.par')),
        'nbonds':14,
        'nangles':61,
        'ndihedrals':145,
        'nimpropers':0,
        'ncmaps':0,
        'nnonbonding':0,
    }
}

