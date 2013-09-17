#!/usr/bin/env python


# imports
from __future__ import print_function
import os,  subprocess, shutil
import _config as config




def run_command(command, logfile='runlog.log'):
    '''runs a process and reports its output and status

    Gets:
        command  -> a list of arguments, e.g. ['ls' , '-l']
        logfile  -> if not None, it is a file to store the output

    Returns:
        stdout   -> both stdout + stderr
        status   -> bool, the status of the command (False if the return code is != 0)

    '''
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    stdout, stderr = process.communicate()
    assert stderr is None, stderr

    if logfile:
        loglines = []
        loglines.append('running:  {}\n'.format(' '.join(command)))
        loglines.append(stdout)
        loglines.append('='*80 + '\n\n')
        with open(logfile, 'a') as f:
            f.writelines(loglines)

    status = False
    if process.returncode is None:
        print ('the process is still running ...')
    elif process.returncode !=0:
        print ('error: non-zero return code occured - check the log file')
    else:
        status = True

    return stdout, status




# ===================================================================
# NAMD
# ===================================================================

def run_namd(k, logfile):
    psf = config.systems[k]['psf']
    pdb = config.systems[k]['pdb']
    pars = '\n'.join(['parameters %s' % x for x in config.systems[k]['pars']])

    conf = config.namd_conf % (psf, pdb, pars)
    with open('conf', 'w') as f:
        f.writelines([conf])


    command = ['%s/namd2' % config.paths['namd'], '+p1', 'conf']
    stdout, status = run_command(command, logfile)

    if not status:
        print (stdout)
        return stdout, False
    else:
        return stdout, True


def parse_namd_output(output):
    lines = output.split('\n')
    result = {}
    for line in lines:
        if line.startswith('ENERGY:'):
            f = line.split()
            if f[1] == '0':
                E = list(map(float, f[2:]))
                result['bond']      = E[0]
                result['angle']     = E[1]
                result['dihedral']  = E[2]
                result['improper']  = E[3]
                result['coul']      = E[4]
                result['vdw']       = E[5]
                result['boundary']  = E[6]
                result['misc']      = E[7]
                result['kinetic']   = E[8]
                result['total']     = E[9]
                result['temp']      = E[10]
                result['potential'] = E[11]

    return result


# ===================================================================
# PSF2TOP
# ===================================================================
def run_psf2top(k, logfile):
    psf = config.systems[k]['psf']

    command = ['%s' % config.paths['psf2top']] + \
              ['-p', psf] + \
              ['-c'] + config.systems[k]['pars'] + \
              ['-v']

    stdout, status = run_command(command, logfile)
    if not status or 'ERROR' in stdout:
        print (stdout)
        return stdout, False
    else:
        return stdout, True



# ===================================================================
# GROMACS
# ===================================================================
def run_gromacs(k, logfile):
    top = 'top.top'
    pdb = config.systems[k]['pdb']
    mdp = config.gmx_mdp
    with open('mdp.mdp', 'w') as f:
        f.writelines([mdp])

    command = ['%s/grompp' % config.paths['gromacs'],
               '-p', top,
               '-f', 'mdp.mdp',
               '-c', pdb,
               '-o', 'topol.tpr']
    stdout, status = run_command(command, logfile)
    if not status:
        print(status)
        return stdout, False
    else:
        command = ['%s/mdrun' % config.paths['gromacs'],
                   '-nt', '1',
                   '-s', 'topol.tpr',
                   '-rerun', pdb,
                   '-g', 'gromacs.log']
        stdout, status = run_command(command, logfile)
        if not status:
            print(stdout)
            return stdout, False
        else:
            return stdout, True


def parse_gromacs_output():
    logname = 'gromacs.log'
    result = {}

    with open(logname) as f:
        lines = f.readlines()

    energy_lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('Step') and lines[i+1].strip().startswith('0'):

            if lines[i+3].strip().startswith('Energies'):
                energy_lines = lines[i+4: i+10]
                if lines[i+11].strip() != '':
                    print('warning: the gromacs energies are in more than 6 lines.')
                break

            elif lines[i+4].strip().startswith('Energies'):
                energy_lines = lines[i+5: i+11]
                if lines[i+12].strip() != '':
                    print('warning: the gromacs energies are in more than 6 lines.')
                break
            else:
                raise RuntimeError("could not parse gromacs log")

    if energy_lines != []:
        for i, line in enumerate(energy_lines):
            energy_lines[i] = energy_lines[i].replace('Proper Dih.',    'Proper_dih')
            energy_lines[i] = energy_lines[i].replace('Improper Dih.',  'Improper_dih')
            energy_lines[i] = energy_lines[i].replace('CMAP Dih.',      'CMAP_dih')
            energy_lines[i] = energy_lines[i].replace('LJ (SR)',        'LJ(SR)')
            energy_lines[i] = energy_lines[i].replace('Coulomb (SR)',   'Coulomb(SR)')
            energy_lines[i] = energy_lines[i].replace('Kinetic En.',    'Kinetic')
            energy_lines[i] = energy_lines[i].replace('Total Energy',   'TotalEnergy')
            energy_lines[i] = energy_lines[i].replace('Pressure (bar)', 'Pressure(bar)')

        vmap = dict(
            bond = 0,
            angle = 0,
            dihedral = 0,
            improper = 0,
            vdw = 0,
            coul = 0,
            kinetic = 0,
            total = 0,
            potential =0,

        )

        _conv = lambda x: float(x) / 4.184

        for i in range(0, len(energy_lines),2):
            titles = energy_lines[i].split()
            values = energy_lines[i+1].split()
            assert len(titles) == len(values), energy_lines[i]

            for j, ty in enumerate(titles):
                if ty == 'Bond':
                    vmap['bond'] = _conv(values[j])

                elif ty == 'U-B':
                    vmap['angle'] = _conv(values[j])

                elif ty in ('Proper_dih', 'CMAP_dih'):
                    vmap['dihedral'] += _conv(values[j])

                elif ty == 'Improper_dih':
                    vmap['improper'] = _conv(values[j])

                elif ty in ('LJ(SR)', 'LJ-14'):
                    vmap['vdw'] += _conv(values[j])

                elif ty in ('Coulomb(SR)', 'Coulomb-14'):
                    vmap['coul'] += _conv(values[j])

                elif ty == 'Kinetic':
                    vmap['kinetic'] = _conv(values[j])

                elif ty == 'Potential':
                    vmap['potential'] = _conv(values[j])

                elif ty == 'TotalEnergy':
                    vmap['total'] = _conv(values[j])

        result = vmap

    return result



# ===================================================================
# MAIN function
# ===================================================================

def main():

    logfile = os.path.abspath('runlog.log')
    if os.path.exists(logfile):
        os.remove(logfile)

    maindir = os.getcwd()

    systems = config.systems
    # from the _config file, get systems
    systems_keys = list(systems.keys())
    systems_keys.sort()

    print(' ')


    for k in systems_keys:
        # should we skip this test ?
        if k in config.skip_systems:
            continue

        # if the output directory for the test `k` still exists, remove it
        if os.path.exists(k):
            shutil.rmtree(k)

        # get the absolute paths
        systems[k]['psf'] = os.path.abspath(systems[k]['psf'])
        systems[k]['pdb'] = os.path.abspath(systems[k]['pdb'])
        for i, m in enumerate(systems[k]['pars']):
            systems[k]['pars'][i] = os.path.abspath(m)


        print(('running system: %s' % k))

        # make a subfolder
        os.mkdir(k)
        os.chdir(k)

        # make gromacs folder
        os.mkdir('gromacs')
        os.chdir('gromacs')

        # make the gromacs topology
        output, ok = run_psf2top(k, logfile)
        if not ok:
            print('An error occured when using psf2top... exiting.')
            return

        # run gromacs
        output, ok = run_gromacs(k, logfile)
        if not ok:
            print('An error occured when running gromacs... exiting.')
            return
        else:
            result = parse_gromacs_output()
            systems[k]['gromacs_result'] = result


        # go one level up
        os.chdir('..')

        # make namd folder
        os.mkdir('namd')
        os.chdir('namd')

        # run namd
        output, ok = run_namd(k, logfile)
        if not ok:
            print('An error occured when running namd... exiting.')
            return
        else:
            with open('namd.out', 'w') as f:
                f.writelines([output])
            result = parse_namd_output(output)
            systems[k]['namd_result'] = result


        # go one level up
        os.chdir('..')

        # go back to the main directory
        os.chdir(maindir)

    summarize_test_outputs(systems)




def summarize_test_outputs(systems):
    '''
    Gets:
        config.systems with the energies e.g.:
            {
                '101': {
                    'psf': '...',
                    'gromacs_result' : {},
                    'namd_result' : {},
                }
            }
    '''

    print(' ')
    system_keys = list(systems.keys())
    system_keys.sort()


    # detail summary ----------------------------
    desc = 'Table 1. Summary of the NAMD and GROMACS energies.\n'
    print(desc)

    for k in system_keys:
        if k in config.skip_systems:
            continue

        print('-' * 59)
        heading = '%s - %s \n' % (k, systems[k]['info'])
        heading+= '{:10s}   {:>10s}   {:>10s}   {:>9s}  {:>9s}'.format(
            '', 'NAMD', 'GROMACS', 'GMX-NAMD', '% |diff|')
        print(heading)

        for m in ('bond', 'angle', 'dihedral', 'improper', 'coul', 'vdw'):
            namd = systems[k]['namd_result'][m]
            gromacs = systems[k]['gromacs_result'][m]

            diff =  gromacs - namd

            if namd == 0:
                diffp = '0.000'
            else:
                diffp = abs(  ((gromacs-namd)/namd) * 100.0  )
                diffp =  '%5.3f' % (diffp)

            result = '%10s   %10.2f   %10.2f   %9.4f  %9s' % (m, namd, gromacs, diff, diffp)
            print(result)

        print(' ')

    print('-' * 59)

    # short summary -----------------------------
    print('\n\n')
    desc = 'Table 2. Summary of the difference between GROMACS and NAMD energies.'
    print(desc)
    print('-' * 110 + ' ' + '-' * 13)
    print('{:12s}  {:6s}  {:4s} {:^13s} {:^13s} {:^13s} {:^13s} {:^13s} {:^13s}  {:^12s}'.format(
           ' ','natoms', 'ff', 'bond', 'angle', 'dihedral', 'improper', 'coul', 'vdw', 'sum'))

    print('-' * 110 + ' ' + '-' * 13)

    for k in system_keys:
        if k in config.skip_systems:
            continue

        sys = systems[k]
        potnamd = 0
        potgmx  = 0
        s = '%12s  %6d  %4s  ' % (sys['name'], sys['natoms'], sys['ff'] )
        for m in ('bond', 'angle', 'dihedral', 'improper', 'coul', 'vdw'):
            namd = systems[k]['namd_result'][m]
            gromacs = systems[k]['gromacs_result'][m]

            potnamd += namd
            potgmx  += gromacs

            diff =  gromacs - namd

            if namd == 0:
                diffp = '0.0'
            else:
                diffp = abs(  ((gromacs-namd)/namd) * 100.0  )
                diffp =  '%4.1f' % (diffp)
            s += '%5.2f (%4s)  ' % (diff, diffp)

        diff = potgmx - potnamd
        if potnamd == 0:
            diffp = '0.0'
        else:
            diffp = abs(  ((potgmx-potnamd)/potnamd) * 100.0  )
            diffp =  '%4.1f' % (diffp)
        s += '%5.2f (%4s)  ' % (diff, diffp)

        print(s)
    print('-' * 110 + ' ' + '-' * 13)

if __name__ == '__main__':
    main()


