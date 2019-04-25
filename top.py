#!/usr/bin/env python

import subprocess
from multiprocessing import Process
from experiment_setup import run

def setup():
    print('setup started')
    downstreamAS = 2914
    upstreamAS = 1239
    experiments = {
       'residue_miro_xpol_init_10000':('residue','miro',20,10000),
       'strawman_miro_xpol_init_10000':('strawman','miro',20,10000),
       'strawman_wiser_0pol_init_10000':('strawman','wiser',0,10000)
       }
    for exp, data in experiments.iteritems():
        run(upstreamAS, downstreamAS, exp, data)
    return

def top():
    print('top started')
    with open("top.log", "w") as ofp:
        ofp.write('  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND\n')
    with open("top.log", "a") as ofp:
        subprocess.call('top -cb n400 -d 0.3 -U postgres -w 150 | grep "local" | grep -v "grep"', shell=True, stdout=ofp)

p1 = Process(target=setup)
p2 = Process(target=top)
p1.start()
p2.start()
