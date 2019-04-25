from __future__ import division
import os, sys, re, numpy
from subprocess import call

pyPath = os.path.dirname(os.path.abspath(__file__))
gnuplot_script = '''
reset

set termoption dash

set style line 80 lt -1 lc rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"
set grid back linestyle 81
set border 3 back linestyle 80

set style line 1 lt rgb "#A00000" lw 1 pt 1 ps 1
set style line 2 lt rgb "#00A000" lw 1 pt 6 ps 1
set style line 3 lt rgb "#5060D0" lw 1 pt 2 ps 1
set style line 4 lt rgb "#F25900" lw 1 pt 9 ps 1

set style line 11 lt -1 lc rgb "#A00000" lw 2 
set style line 12 lt -1 lc rgb "#00A000" lw 2
set style line 13 lt -1 lc rgb "#5060D0" lw 2
set style line 14 lt 1 lc rgb "#F25900" lw 2

set key top right font ",5"

set xtics nomirror
set ytics nomirror'''

def sample(n, d):
    '''
    Sample the data. Take 1 point for each n points in data array d.
    '''
    return d[::n]


def parse_log (logfile):

    d = []

    f = open(logfile, "r")
    for l in f.readlines():
        if l[0] == '#':
            continue
        temp = l.split('\t')
        if len(temp) != 2:
            temp = l.split(' ')
        assert len(temp) == 2, "Unrecognized line: {}".format(l)
        d.append(float(temp[1]))
    f.close()

    return d

def parse_ram_log(logfile):
    tbSize = []
    ramSize = []
    f = open(logfile)
    for l in f.readlines():
        if l[0] == '#':
            continue
        tmp = l.split(' ')
        if len(tmp) > 1:
            tmp = tmp[9]
            if tmp[-1] == 'g':
                ramSize.append(float(tmp[:-1])*1024)
            elif tmp[-1] == 'm':
                ramSize.append(float(tmp[:-1]))
            else:
                ramSize.append(float(tmp)/1024)
        else:
            tbSize.append(float(tmp[0])/1000000)
    return tbSize, ramSize

def plot_CDF (title, logs, nametext):
    xlabel = 'delay'

    pltfile = os.path.join(pyPath, 'plt', nametext+'.plt')
    pdffile = os.path.join(pyPath, 'pdf', nametext+'.pdf')
    #datafiles = []
    datafiles_sampled = []
    #datalength = []
    for log in logs:
        datfile = log.replace('log', 'dat')
        datfile_sampled = datfile.replace('.dat', 'sampled.dat')

        #x = parse_log(log)
        #x.sort()
        #y = [float(e)/len(x) for e in range(1, len(x)+1)]
        #f = open(datfile, 'w')
        #for i in range(len(x)):
        #    f.write(str(y[i]) + ' ' + str(x[i]) + '\n')
        #f.close()

        x = sample(100, parse_log(log))
        x.sort()
        y = [float(e)/len(x) for e in range(1, len(x)+1)]
        f = open(datfile_sampled, 'w')
        for i in range(len(x)):
            f.write(str(y[i]) + ' ' + str(x[i]) + '\n')
        f.close()

        #datafiles.append(datfile)
        #datafiles_sampled.append(datafiles_sampled)
    
    call(["Gnuplot", os.path.join(pyPath, 'plt', 'BGP feeds processing delay with 10000 feeds.plt')])
    return

def run_plot():
    allLogs = os.listdir(os.path.join(pyPath, 'log'))
    delayLogs = [e for e in allLogs if re.match('[0-9]{1,}.+_[0-9]{1,}.log', e)]
    ramLogs = [e for e in allLogs if e not in delayLogs]
    AS_links = []
    for log in delayLogs:
        temp = log.split('_',2)
        link = (int(temp[0]), int(temp[1]))
        if link not in AS_links:
            AS_links.append(link)

    for l in AS_links:
        # plot initialization logs
        delayLogs = [os.path.join(pyPath, 'log', e) for e in delayLogs if re.match('{}_{}_.+_[0-9]{{1,}}.log'.format(l[0], l[1]), e)]
        #print "Plotting initialization delay for downstream AS {} and upstream AS {}...".format(l[0], l[1])
        plot_CDF('BGP feeds processing delay', delayLogs, 'BGP feeds processing delay with 10000 feeds')

'''
    ramLogs = [os.path.join(pyPath, 'log', e) for e in ramLogs]
    for log in ramLogs:
        f = open(log.replace('log', 'dat'), 'w')
        fs = open(log.replace('log', 'dat').replace('.dat','_sampled.dat'), 'w')
        tbSize, ramSize = parse_ram_log(log)
        for i in range(len(tbSize)):
            f.write(str(tbSize[i])+' '+str(ramSize[i])+'\n')
        f.close()
        for i in range(19, len(tbSize), 20):
            fs.write(str(tbSize[i])+' '+str(ramSize[i])+'\n')
        fs.close()
'''

if __name__ == '__main__':
    run_plot()
