


paths = {
    'gromacs': '/Users/Reza/Programs/gromacs/4.5.7/bin',
    'namd'   : '/Users/Reza/Workspace/Programs/namd/2.9',
    'psf2top': '/Users/Reza/Devel/pytopol/scripts/psf2top.py',
}


systems = {
    '1_memb': {
        'psf':'prep/memb_nowat.psf',
        'pdb':'prep/memb_nowat.pdb',
        'pars':['prep/par_all27_prot_lipid.prm'],
        'info': 'POCP Membrane in vacuum using CHARMM 27 (38 POPC, 5092 atoms)',
    },
    '2_lys': {
        'psf':'prep/1lyz_nowat_autopsf.psf',
        'pdb':'prep/1lyz_nowat_autopsf.pdb',
        'pars':['prep/par_all27_prot_lipid.prm'],
        'info': '1LYZ in vacuum using CHARMM 27 and CMAP (PDB ID: 1LYZ, 1966 atoms)',
    },
    '3_chol': {
        'psf':'prep/chol.psf',
        'pdb':'prep/chol.pdb',
        'pars':['prep/par_all36_prot.prm', 'prep/par_all36_lipid.prm',
                'prep/par_all36_cgenff.prm', 'prep/par_chol.par',
                'prep/par_wation.par'],
        'info': 'Cholestrol in TIP3P water using CHARMM 36 (3810 atoms)',
    },
    '0_glucl': {
        'psf':'prep/glucl.psf',
        'pdb':'prep/glucl.pdb',
        'pars':['prp/par_all36_prot.prm', 'prep/par_all36_lipid.prm',
                'prep/par_all36_cgenff.prm', 'prep/par_wation.par'],
        'info': 'GluCl in TIP3P water and POPC membrane using CHARMM 36 (163394 atoms)',
    },

}


namd_conf = """
structure          %s
coordinates        %s

paratypecharmm      on
%s       ;# parameters
exclude             scaled1-4
1-4scaling          1.0

switching           off
cutoff              1000
pairlistdist        1000
timestep            1.0
outputenergies      1
outputtiming        1
binaryoutput        no

outputname          namd
dcdfreq             1
temperature         300
run                 0
"""


gmx_mdp = """
integrator    = md
nsteps        = 0
nstlog        = 1
nstlist       = 0
ns_type       = simple
rlist         = 0
coulombtype   = cut-off
rcoulomb      = 0
rvdw          = 0
pbc           = no
"""
