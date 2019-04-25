from experiment_setup import Experiment

downstreamAS = 2914
upstreamAS = 1239
numlines = 10000
exp = Experiment()
inslogfile = 'Gnuplot/log/{0}_{1}_{2}.log'.format(downstreamAS, upstreamAS,'wiser_init_{}'.format(numlines))
exp.setup(downstreamAS, upstreamAS)
exp.load_wiser_check_in_db()
ribfile = 'rib{0}.txt'.format(10000)
exp.load_bgp(ribfile, inslogfile)
exp.unload_wiser()