

# ===================================================================
# Paths for the programs
# ===================================================================
paths = {
    # 'gromacs': '/Users/Reza/Programs/gromacs/4.5.7/bin',
    'gromacs': '/Users/Reza/Programs/gromacs/4.6.3/double/bin',
    'namd'   : '/Users/Reza/Workspace/Programs/namd/2.9',
    'psf2top': '/Users/Reza/Devel/pytopol/scripts/psf2top.py',
}


# ===================================================================
# For the systems:
#   0x      -> peptides
#   1x      -> lipids
#   2x      -> proteins
#   3x      -> small molecules
#   4x      -> water
#   5x      -> protein + ligand systems
# ===================================================================

# the system ids that tests should be skipped for
skip_systems = [
    '001', #'002',
    '003', '004', '005', '006', '007', '008', '009', '010',

    '101',    # popc memb
    '102',    # dopc memb

    # '201',    # Lysozyme
    # '301',    # cholestrol

    '401', '402', '403',

    '501',     # glucl

    '601',      # gic
    '602',      # vid : pr + chol + lipid
    '603',      # vid : pr + chol
    '604',      # vid : pr
    '605',      # vid : chol + lipid
    '606',      # vid : chol
    '607',      # vid : lipid
    '608',      # vid : one DOPC
]

systems = {

    # peptides

    '001': {
        'psf':'peptide/p1_A_autopsf.psf',
        'pdb':'peptide/p1_A_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'A in vacuum',
        'name': 'Alanine',
        'ff': 'CH27',
        'natoms':  -1,
        'nres': 1,
    },
    '002': {
        'psf':'peptide/p2_AD_autopsf.psf',
        'pdb':'peptide/p2_AD_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'AD in vacuum',
        'name': 'AD peptide',
        'ff': 'CH27',
        'natoms':  22,
        'nres':2,
    },
    '003': {
        'psf':'peptide/p3_ADL_autopsf.psf',
        'pdb':'peptide/p3_ADL_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ADL in vacuum',
        'name': 'ADL peptide',
        'ff': 'CH27',
        'natoms':  -1,
        'nres':3,
    },
    '004': {
        'psf':'peptide/p4_ADLK_autopsf.psf',
        'pdb':'peptide/p4_ADLK_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ADLK in vacuum',
        'name': 'ADLK peptide',
        'ff': 'CH27',
        'natoms':  -1,
        'nres':4,
    },
    '005': {
        'psf':'peptide/p5_ADLKR_autopsf.psf',
        'pdb':'peptide/p5_ADLKR_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ADLKR in vacuum',
        'name': 'ADLKR peptide',
        'ff': 'CH27',
        'natoms':  -1,
        'nres':5,
    },
    '006': {
        'psf':'peptide/p2_AR_autopsf.psf',
        'pdb':'peptide/p2_AR_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'AR in vacuum',
        'name': 'AR peptide',
        'ff': 'CH27',
        'natoms':  -1,
        'nres':2,
    },
    '007': {
        'psf':'peptide/p3_ARP_autopsf.psf',
        'pdb':'peptide/p3_ARP_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ARP in vacuum',
        'name': 'ARP peptide',
        'ff': 'CH27',
        'natoms':  -1,
        'nres':3,
    },
    '008': {
        'psf':'peptide/p4_ARPA_autopsf.psf',
        'pdb':'peptide/p4_ARPA_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'ARPA in vacuum',
        'name': 'ARPA peptide',
        'ff': 'CH27',
        'natoms':  -1,
        'nres':4,
    },
    '009': {
        'psf':'peptide/p1_P_autopsf.psf',
        'pdb':'peptide/p1_P_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'P in vacuum',
        'name': 'Proline',
        'ff': 'CH27',
        'natoms':  -1,
        'nres':1,
    },
    '010': {
        'psf':'peptide/p3_GPG_autopsf.psf',
        'pdb':'peptide/p3_GPG_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': 'GPG in vacuum',
        'name': 'GPG peptide',
        'ff': 'CH27',
        'natoms':  -1,
        'nres':3,
    },

    # lipids

    '101': {
        'psf':'membrane/popc_autopsf.psf',
        'pdb':'membrane/popc_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
               ],
        'info': 'POPC membrane in vaccum (CHARMM 36, 74 POPC, 9916 atoms)',
        'name': 'POPC memb',
        'ff': 'CH36',
        'natoms':  9916,
        'nres':74,
    },
    '102': {
        'psf':'membrane/dopc_autopsf.psf',
        'pdb':'membrane/dopc_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
               ],
        'info': 'DOPC membrane in vaccum (CHARMM 36, 76 DOPC, 10488 atoms)',
        'name': 'DOPC memb',
        'ff': 'CH36',
        'natoms':  10488,
        'nres':76,
    },

    # proteins

    '201': {
        'psf':'protein/lyz_autopsf.psf',
        'pdb':'protein/lyz_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm'],
        'info': '1LYZ in vacuum (CHARMM 27+CMAP, 129 residues, 1966 atoms)',
        'name': 'Lysozyme',
        'ff': 'CH27',
        'natoms':  1966,
        'nres':129,
    },


    # small organic molecules

    '301': {
        'psf':'ligand/chol_nowat_autopsf.psf',
        'pdb':'ligand/chol_nowat_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
                'par/par_all36_cgenff.prm',
                'par/par_chol.par',
               ],
        'info': 'Cholesterol in vacuum (CHARMM 36, 74 atoms)',
        'name': 'Cholesterol',
        'ff': 'CH36',
        'natoms':  74,
        'nres':1,
    },

    # water


    '401': {
        'psf':'other/onlywater_autopsf.psf',
        'pdb':'other/onlywater_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm',
               ],
        'info': 'Water box (CHARMM 27, 3732 atoms)',
        'name': 'water box',
        'ff': 'CH27',
        'natoms':  3732,
        'nres':-1,
    },
    '402': {
        'psf':'other/wmol_autopsf.psf',
        'pdb':'other/wmol_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm',
               ],
        'info': '10 water molecule (CHARMM 27, 30 atoms)',
        'name': '10 wat',
        'ff': 'CH27',
        'natoms':  30,
        'nres':10,
    },
    '403': {
        'psf':'other/wat_autopsf.psf',
        'pdb':'other/wat_autopsf.pdb',
        'pars':['par/par_all27_prot_lipid.prm',
               ],
        'info': 'water box + 4 ions',
        'name': 'wat + 4 ions',
        'ff': 'CH27',
        'natoms':  3736,
        'nres':-1,
    },

    # protein-membrane

    '501': {
        'psf':'glucl/glucl_autopsf.psf',
        'pdb':'glucl/glucl_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
               ],
        'info': 'GluCl + POPC memb in vacuum (CHARMM 36, 64247 atoms)',
        'name': 'GluCl+POPC',
        'ff': 'CH36',
        'natoms':  64247,
        'nres':-1,
    },

    # archive $ gic

    '601': {
       'psf':'archive/gic/D_system_nowat_autopsf.psf',
        'pdb':'archive/gic/D_system_nowat_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
                'par/par_all36_cgenff.prm',
                'archive/gic/lig.par',
               ],
        'info': 'Channel + lig + lipid',
        'name': 'Channel+POPC',
        'ff': 'CH36',
        'natoms':  -1,
        'nres':-1,
    },

    # archive # vid
    '602': {
       'psf':'archive/vid/1_prot_chol_lipid_autopsf.psf',
        'pdb':'archive/vid/1_prot_chol_lipid_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
                'par/par_all36_cgenff.prm',
                'par/par_chol.par',
               ],
        'info': 'Protein + chol + lipid',
        'name': 'P+C+L',
        'ff': 'CH36',
        'natoms':  27562,
        'nres':458,
    },
     '603': {
       'psf':'archive/vid/2_prot_chol_autopsf.psf',
        'pdb':'archive/vid/2_prot_chol_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
                'par/par_all36_cgenff.prm',
                'par/par_chol.par',
               ],
        'info': 'Protein + chol',
        'name': 'P+C',
        'ff': 'CH36',
        'natoms':  10324,
        'nres':298,
    },
     '604': {
       'psf':'archive/vid/3_prot_autopsf.psf',
        'pdb':'archive/vid/3_prot_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
               ],
        'info': 'Protein',
        'name': 'P',
        'ff': 'CH36',
        'natoms':  4294,
        'nres':282,
    },
    '605': {
       'psf':'archive/vid/4_chol_lipid_autopsf.psf',
        'pdb':'archive/vid/4_chol_lipid_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
                'par/par_all36_cgenff.prm',
                'par/par_chol.par',
               ],
        'info': 'Chol + lipid',
        'name': 'C+L',
        'ff': 'CH36',
        'natoms':  23264,
        'nres':176,
    },
    '606': {
       'psf':'archive/vid/5_chol_autopsf.psf',
        'pdb':'archive/vid/5_chol_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
                'par/par_all36_cgenff.prm',
                'par/par_chol.par',
               ],
        'info': 'Chol',
        'name': 'C',
        'ff': 'CH36',
        'natoms':  1184,
        'nres':16,
    },
    '607': {
       'psf':'archive/vid/6_lipid_autopsf.psf',
        'pdb':'archive/vid/6_lipid_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
               ],
        'info': 'Lipid',
        'name': 'L',
        'ff': 'CH36',
        'natoms':  22080,
        'nres':160,
    },
    '608': {
       'psf':'archive/vid/7_1dopc_autopsf.psf',
        'pdb':'archive/vid/7_1dopc_autopsf.pdb',
        'pars':['par/par_all36_prot.prm',
                'par/par_all36_lipid.prm',
               ],
        'info': '1 DOPC',
        'name': '1 DOPC',
        'ff': 'CH36',
        'natoms':  138,
        'nres':1,
    },
}



# ===================================================================
# NAMD configuration file
# It has three place-holders (%s) that are replaced by psf, pdb and
#   parameter options.
# ===================================================================
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


# ===================================================================
# Gromacs MDP file
# ===================================================================
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
