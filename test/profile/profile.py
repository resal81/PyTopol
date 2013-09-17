


import pstats
import os

if not os.path.exists('ref.prof'):
    cmd = 'python -m cProfile -o ref.prof ../../scripts/psf2top.py'
    cmd += ' -p ../systems/membrane/popc_autopsf.psf'
    cmd += ' -c ../systems/par/par_all36_lipid.prm'

    os.system(cmd)

p = pstats.Stats('ref.prof')
p.sort_stats('cumulative').print_stats(10)

