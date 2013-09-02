


paths = {
    'gromacs': '/Users/Reza/Programs/gromacs/4.5.7/bin',
    'namd'   : '/Users/Reza/Workspace/Programs/namd/2.9',
    'psf2top': '/Users/Reza/Devel/pytopol/scripts/psf2top.py',
}


systems = {
    '01': {
        'psf':'prep/p1_A_autopsf.psf',
        'pdb':'prep/p1_A_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'A in vacuum',
        'skip':False,
    },
    '02': {
        'psf':'prep/p2_AD_autopsf.psf',
        'pdb':'prep/p2_AD_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'AD in vacuum',
        'skip':False,
    },
    '03': {
        'psf':'prep/p3_ADL_autopsf.psf',
        'pdb':'prep/p3_ADL_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ADL in vacuum',
        'skip':False,
    },
    '04': {
        'psf':'prep/p4_ADLK_autopsf.psf',
        'pdb':'prep/p4_ADLK_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ADLK in vacuum',
        'skip':False,
    },
    '05': {
        'psf':'prep/p5_ADLKR_autopsf.psf',
        'pdb':'prep/p5_ADLKR_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ADLKR in vacuum',
        'skip':False,
    },
    '06': {
        'psf':'prep/p2_AR_autopsf.psf',
        'pdb':'prep/p2_AR_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'AR in vacuum',
        'skip':False,
    },
    '07': {
        'psf':'prep/p3_ARP_autopsf.psf',
        'pdb':'prep/p3_ARP_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ARP in vacuum',
        'skip':False,
    },
    '08': {
        'psf':'prep/p4_ARPA_autopsf.psf',
        'pdb':'prep/p4_ARPA_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ARPA in vacuum',
        'skip':False,
    },
    '09': {
        'psf':'prep/p1_P_autopsf.psf',
        'pdb':'prep/p1_P_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'P in vacuum',
        'skip':False,
    },
    '10': {
        'psf':'prep/p3_GPG_autopsf.psf',
        'pdb':'prep/p3_GPG_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'GPG in vacuum',
        'skip':False,
    },
    '21_lys': {
        'psf':'prep/1lyz_nowat_autopsf.psf',
        'pdb':'prep/1lyz_nowat_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': '1LYZ in vacuum using CHARMM 27 and CMAP (PDB ID: 1LYZ, 1966 atoms)',
        'skip':False,
    },

}

systems2 = {
    '1_ala4': {
        'psf':'prep/ala4_autopsf.psf',
        'pdb':'prep/ala4_autopsf.pdb',
        'pars':['par/par_all36_prot.prm'],
        'info': 'Alanine peptide in vacuum (CHARMM 36, 4 resiudes, )',
        'skip':False,
    },
    '2_pept7': {
        'psf':'prep/peptide7_autopsf.psf',
        'pdb':'prep/peptide7_autopsf.pdb',
        'pars':['prep/par_all36_prot.prm'],
        'info': 'Short peptide in vaccum (CHARMM 36, 7 residues, )',
        'skip': False,
    },
    '3_args': {
        'psf':'prep/arg_autopsf.psf',
        'pdb':'prep/arg_autopsf.pdb',
        'pars':['prep/par_all27_prot_lipid.prm'],
        'info': 'Arg in vaccum (CHARMM 27, 1 residues, )',
        'skip': False,
    },
    '4_p2': {
        'psf':'prep/p2_autopsf.psf',
        'pdb':'prep/p2_autopsf.pdb',
        'pars':['prep/par_all27_prot_lipid.prm'],
        'info': 'RP in vaccum (CHARMM 27, 2 residues, )',
        'skip': False,
    },

    '3_pept26': {
        'psf':'prep/peptide26_autopsf.psf',
        'pdb':'prep/peptide26_autopsf.pdb',
        'pars':['prep/par_all36_prot.prm'],
        'info': 'Short peptide in vaccum (CHARMM 36, 26 residues, )',
        'skip': True,
    },
    '3_memb': {
        'psf':'prep/memb_38popc_autopsf.psf',
        'pdb':'prep/memb_38popc_autopsf.pdb',
        'pars':['prep/par_all36_prot.prm',
                'prep/par_all36_lipid.prm',
               ],
        'info': 'POPC membrane in vaccum (CHARMM 36, 38 POPC, )',
        'skip': True,
    },
    '4_memb': {
        'psf':'prep/memb_popc_dopc_autopsf.psf',
        'pdb':'prep/memb_popc_dopc_autopsf.pdb',
        'pars':['prep/par_all36_prot.prm',
                'prep/par_all36_lipid.prm',
               ],
        'info': 'POPC/DOPC membrance in vaccum (CHARMM 36, 19 POPC, 19 DOPC)',
        'skip':True,
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
