


paths = {
    #'gromacs': '/Users/Reza/Programs/gromacs/4.5.7/bin',
    'gromacs': '/Users/Reza/Programs/gromacs/4.6.3/double/bin',
    'namd'   : '/Users/Reza/Workspace/Programs/namd/2.9',
    'psf2top': '/Users/Reza/Devel/pytopol/scripts/psf2top.py',
}


systems = {
    '01': {
        'psf':'peptide/p1_A_autopsf.psf',
        'pdb':'peptide/p1_A_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'A in vacuum',
        'skip':True,
    },
    '02': {
        'psf':'peptide/p2_AD_autopsf.psf',
        'pdb':'peptide/p2_AD_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'AD in vacuum',
        'skip':True,
    },
    '03': {
        'psf':'peptide/p3_ADL_autopsf.psf',
        'pdb':'peptide/p3_ADL_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ADL in vacuum',
        'skip':True,
    },
    '04': {
        'psf':'peptide/p4_ADLK_autopsf.psf',
        'pdb':'peptide/p4_ADLK_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ADLK in vacuum',
        'skip':True,
    },
    '05': {
        'psf':'peptide/p5_ADLKR_autopsf.psf',
        'pdb':'peptide/p5_ADLKR_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ADLKR in vacuum',
        'skip':True,
    },
    '06': {
        'psf':'peptide/p2_AR_autopsf.psf',
        'pdb':'peptide/p2_AR_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'AR in vacuum',
        'skip':True,
    },
    '07': {
        'psf':'peptide/p3_ARP_autopsf.psf',
        'pdb':'peptide/p3_ARP_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ARP in vacuum',
        'skip':True,
    },
    '08': {
        'psf':'peptide/p4_ARPA_autopsf.psf',
        'pdb':'peptide/p4_ARPA_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ARPA in vacuum',
        'skip':True,
    },
    '09': {
        'psf':'peptide/p1_P_autopsf.psf',
        'pdb':'peptide/p1_P_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'P in vacuum',
        'skip':True,
    },
    '10': {
        'psf':'peptide/p3_GPG_autopsf.psf',
        'pdb':'peptide/p3_GPG_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'GPG in vacuum',
        'skip':True,
    },
    '21': {
        'psf':'membrane/popc_autopsf.psf',
        'pdb':'membrane/popc_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
               ],
        'info': 'POPC membrane in vaccum (CHARMM 36, 74 POPC, 9916 atoms)',
        'skip': True,
    },
    '22': {
        'psf':'membrane/dopc_autopsf.psf',
        'pdb':'membrane/dopc_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
               ],
        'info': 'DOPC membrane in vaccum (CHARMM 36, 76 DOPC, 10488 atoms)',
        'skip': True,
    },
    '31': {
        'psf':'protein/1lyz_nowat_autopsf.psf',
        'pdb':'protein/1lyz_nowat_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': '1LYZ in vacuum (CHARMM 27+CMAP, 129 residues, 1966 atoms)',
        'skip': True,
    },
    '41': {
        'psf':'ligand/chol_nowat_autopsf.psf',
        'pdb':'ligand/chol_nowat_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
                'par/par_all36_cgenff.prm',
                'par/par_chol.par',
               ],
        'info': 'Cholestrol in vacuum (CHARMM 36, 74 atoms)',
        'skip': False,
    },
    '42': {
        'psf':'other/onlywater_autopsf.psf',
        'pdb':'other/onlywater_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm',
               ],
        'info': 'Water box (CHARMM 27, 3732 atoms)',
        'skip': True,
    },
    '43': {
        'psf':'other/wmol_autopsf.psf',
        'pdb':'other/wmol_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm',
               ],
        'info': '10 water molecule (CHARMM 27, 30 atoms)',
        'skip': True,
    },
    '44': {
        'psf':'other/wat_autopsf.psf',
        'pdb':'other/wat_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm',
               ],
        'info': 'Water box + 4 ions (CHARMM 27, 3736 atoms)',
        'skip': True,
    },
    '51': {
        'psf':'glucl/glucl_autopsf.psf',
        'pdb':'glucl/glucl_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
               ],
        'info': 'GluCl + POPC memb in vacuum (CHARMM 36, 64247 atoms)',
        'skip': True,
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
