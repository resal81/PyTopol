#!/usr/bin/env python


import os, sys, subprocess, shutil
import _config as config

def run_command(command, logfile='runlog.log'):

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
                E = map(float, f[2:])
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


def run_psf2top(k, logfile):
    psf = config.systems[k]['psf']
    pdb = config.systems[k]['pdb']
    #pars = ' '.join(['%s' % x for x in config.systems[k]['pars']])

    command = ['%s' % config.paths['psf2top'], psf] + config.systems[k]['pars'] + ['-v']
    stdout, status = run_command(command, logfile)
    if not status or 'ERROR' in stdout:
        print (stdout)
        return stdout, False
    else:
        return stdout, True


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
            energy_lines = lines[i+4: i+10]
            if lines[i+11].strip() != '':
                print('warning: the gromacs energies are in more than 6 lines.')
            break

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


def main():

    logfile = os.path.abspath('runlog.log')
    if os.path.exists(logfile):
        os.remove(logfile)

    maindir = os.getcwd()
    systems = list(config.systems.keys())
    systems.sort()

    print(' ')

    for k in systems:
        if os.path.exists(k):
            shutil.rmtree(k)

        # get the absolute paths
        config.systems[k]['psf'] = os.path.abspath(config.systems[k]['psf'])
        config.systems[k]['pdb'] = os.path.abspath(config.systems[k]['pdb'])
        for i, m in enumerate(config.systems[k]['pars']):
            config.systems[k]['pars'][i] = os.path.abspath(m)


        print ('running system: %s' % k)

        # make a subfolder
        os.mkdir(k)
        os.chdir(k)

        # make gromacs folder
        os.mkdir('gromacs')
        os.chdir('gromacs')

        # make the gromacs topology
        output, ok = run_psf2top(k, logfile)
        if not ok:
            print('an error occured when using psf2top... exiting.')
            return

        # run gromacs
        output, ok = run_gromacs(k, logfile)
        if not ok:
            print('an error occured when running gromacs... exiting.')
            return
        else:
            result = parse_gromacs_output()
            config.systems[k]['gromacs_result'] = result


        # go one level up
        os.chdir('..')

        # make namd folder
        os.mkdir('namd')
        os.chdir('namd')

        # run namd
        output, ok = run_namd(k, logfile)
        if not ok:
            print('an error occured when running namd... exiting.')
            return
        else:
            result = parse_namd_output(output)
            config.systems[k]['namd_result'] = result


        # go one level up
        os.chdir('..')

        # go back to the main directory
        os.chdir(maindir)


    print(' ')
    for k in systems:
        print '%s - %s' % (k, config.systems[k]['info'])
        print '%-10s   %-10s   %-10s  %-9s' % (k, 'NAMD', 'GROMACS', 'Diff (%)')
        for m in ('bond', 'angle', 'dihedral', 'improper', 'coul', 'vdw'):
            namd = config.systems[k]['namd_result'][m]
            gromacs = config.systems[k]['gromacs_result'][m]
            if namd == 0:
                diff = 'NA'
            else:
                diff = '%6.3f' % (((gromacs-namd)/namd) * 100.0)
            s = '%10s   %10.1f   %10.1f   %9s' % (m, namd, gromacs, diff)
            print s

        print


if __name__ == '__main__':
    main()


