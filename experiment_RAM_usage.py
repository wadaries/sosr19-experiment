#!/usr/bin/env python
import subprocess
from multiprocessing import Process
from timeit import default_timer as timer
from experiment_setup import Experiment

def run(upstreamAS, downstreamAS, case, data, stepNum = 100):
    n = data[3]
    step = n/stepNum
    X = range(0, n, step)
    X = [x + step for x in X]
    exp = Experiment()
    exp.setup(downstreamAS, upstreamAS)

    if data[0] == 'residue':
       if data[1] == 'miro':
           exp.load_miro_residue()
       elif data[1] == 'wiser':
           exp.load_wiser_residue()
       elif data[1] == 'combine':
           exp.load_miro_wiser_residue()
    elif data[0] == 'strawman':
       if data[1] == 'miro':
           exp.load_miro()
       elif data[1] == 'wiser':
           exp.load_wiser()

    if data[2] != 0:
       exp.load_miro_policies("rib10000.txt", data[2])
       print('Loaded {} policies'.format(data[2]))
    else:
       print('Loaded 0 policies')
    ribfile = open('rib1000000.txt', 'r')

    logf = open('Gnuplot/log/{}_ram.log'.format(case), 'w')
    logf.write('# PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND\n')
    logf.flush()
    start = timer()
    errCnt = 0
    for i in range(1,n+1):
        l = ribfile.readline()
        try:
            bgp_announce(l, exp)
        except Exception, e:
            errCnt += 1
            print 'Failed at the line "{}". {} BGP announcement(s) failed so far. Error: '.format(l, errCnt), e 
        if i in X:
            print '{}% finished for current scenario.'.format(float(i)/n*100)
            logf.write(str(i)+'\n')
            logf.flush()
            subprocess.call('top -cb n1 -U postgres -w 150 | grep "local" | grep -v "grep"', shell=True, stdout=logf)
    end = timer()
    logf.close()
    delay = (end-start)
    print 'Load {} BGP feeds for scenario:{} in {} s.'.format(n, case, delay)
    ribfile.close()

def top():
    print('top started')
    with open("top.log", "w") as ofp:
        ofp.write('  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND\n')
    with open("top.log", "a") as ofp:
        #subprocess.call('top -cb n400 -d 0.3 -U postgres -w 150 | grep "local" | grep -v "grep"', shell=True, stdout=ofp)
        subprocess.call('top -cb n5 -U postgres -w 150 | grep "local" | grep -v "grep"', shell=True, stdout=ofp)

def bgp_announce(feedline, exp):

    feed = feedline.split('|')
    if (feedline.startswith('#') or feedline.isspace() or
            feed[0] is not 'R' or not (feed[1] is 'A'
            or feed[1] is 'W')):
        return

    # STRAWMANS
    if exp.miro:
        if feed[1] is 'A':
            delay = exp.bgp_announce_miro(feed)
        elif feed[1] is 'W':
            delay = exp.bgp_withdraw(feed)
    elif exp.wiser:
        if feed[1] is 'A':
            delay = exp.bgp_announce_wiser(feed)
        elif feed[1] is 'W':
            delay = exp.bgp_withdraw(feed)

    # RESIDUES
    elif exp.miro_res:
        if feed[1] is 'A':
            ins_delay, pol_delay = exp.bgp_announce_miro_residue(feed)
        elif feed[1] is 'W':
            delay = exp.bgp_withdraw(feed)

    elif exp.wiser_res:
        if feed[1] is 'A':
            ins_delay, pol_delay = exp.bgp_announce_wiser_residue(feed)
        elif feed[1] is 'W':
            delay = exp.bgp_withdraw(feed)

    elif exp.miro_wiser_res:
        if feed[1] is 'A':
            ins_delay, pol_delay = exp.bgp_announce_miro_wiser_residue(feed)
        elif feed[1] is 'W':
            delay = exp.bgp_withdraw(feed)
    return

if __name__ == '__main__':
    downstreamAS = 2914
    upstreamAS = 1239
    experiments = {
        'miro_residue':('residue','miro',20,1000000),
        'wiser_residue':('residue','wiser',0,1000000),
        'miro_wiser_residue':('residue','combine',20,1000000)
        }
    for exp, data in experiments.iteritems():
        run(upstreamAS, downstreamAS, exp, data, 100)
