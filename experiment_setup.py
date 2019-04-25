#!/usr/bin/env python
import os, sys, psycopg2, random, re
from itertools import groupby
from timeit import default_timer as timer
from Gnuplot.log_parser import run_plot
pyPath = os.path.dirname(os.path.abspath(__file__))
databaseHost = '192.168.56.101'
databasePort = 5432
databaseName = 'bolero'
databaseUser = 'bolero'
databasePassword = 'bolero'
class Experiment:
#=====| SETUP |===============================================================#
    def __init__(self, dbname=databaseName, user=databaseUser, password=databasePassword,
            host=databaseHost, port=databasePort):
        # Connect to DB
        self.conn = psycopg2.connect(dbname=databaseName, user=databaseUser, password=databasePassword,
            host=databaseHost, port=databasePort)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

        # AS topology and ingress/egres files, and their respective delimiters
        self.dataFiles = ['allIGP',
                'AS_links',
                'ingress_egress', 
                'peering_links']
        self.delimiters = {'allIGP':',',
                'AS_links':',',
                'ingress_egress':'|', 
                'peering_links':','}
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()
        return

    def setup(self, downstreamAS, upstreamAS):
        self.downstreamAS = downstreamAS
        self.upstreamAS = upstreamAS
        # Load SQL table definitions
        s = open(os.path.join(pyPath, 'experiment_setup.sql')).read()
        self.cur.execute(s)

        # Copy each datafile into DB
        for e in self.dataFiles:
            f = open(os.path.join(pyPath, e))
            self.cur.copy_from(f, e, sep=self.delimiters[e])
            f.close()

        # Clear bgp table
        self.cur.execute('truncate table bgp;')

        self.IGP = {} # Maps links to cost
        self.ingress = [] # Ingress routers for downstream AS
        self.egress = [] # Egress routers for downstream AS

        # Check that valid link exists
        self.cur.execute('''select ingress, egress from ingress_egress 
                where (downstreamAS, upstreamAS) = ({}, {})
                '''.format(downstreamAS, upstreamAS))
        e = self.cur.fetchone()
        assert (e is not None),'''No valid AS link between the downstream AS 
        {} and upstream AS {}!'''.format(downstreamAS, upstreamAS)
        self.ingress = e[0]
        self.egress = e[1]

        # Policy table for MIRO
        droppolicy_tbl = "DROP TABLE IF EXISTS policy CASCADE;"
        createpolicy_tbl = """CREATE UNLOGGED TABLE policy (
            prefix varchar,
            aspath int);"""
        self.cur.execute(droppolicy_tbl)
        self.cur.execute(createpolicy_tbl)

        # MIRO/Wiser switch on/off
        self.miro = False
        self.wiser = False
        self.miro_res = False
        self.wiser_res = False

        # Load igp
        self.load_igp(downstreamAS)
        return
        
    def load_igp(self, downstreamAS):
        igp_qry = 'select ingress, egress, cost from allIGP where ASNum = {}'
        self.cur.execute(igp_qry.format(downstreamAS))
        self.IGP = {} # {(ingress, egress): cost}
        for e in self.cur.fetchall():
            ingress = e[0]
            egress = e[1]
            cost = e[2]
            self.IGP[(ingress, egress)] = cost
        return

#=====| SHARED |==============================================================#
    def load_bgp(self, infile, logfile, logfile2=""):
        # Log delays
        readme = '''# Logs the delay for processing a BGP feed in seconds.
# Data format: <BGP feed row number>    <Delay>\n'''
        readme_res = '''# Logs the delay for querying a BGP feed in seconds.
# Data format: <BGP feed row number>    <Delay>\n'''
        ofp = open(logfile, 'w')
        ofp.write(readme)
        ofp_res = open(logfile2, 'w') if logfile2 != "" else None
        if ofp_res != None:
            ofp_res.write(readme_res)

        # Parse file
        line_n = 1
        with open(infile, 'r') as ifp:
            for l in ifp:
                feed = l.split('|')
                if (l.startswith('#') or l.isspace() or
                        feed[0] is not 'R' or not (feed[1] is 'A'
                        or feed[1] is 'W')):
                    continue

                # STRAWMANS
                if self.miro:
                    if feed[1] is 'A':
                        delay = self.bgp_announce_miro(feed)
                        ofp.write('{0}\t{1}\n'.format(line_n, str(delay * 1000)))
                    elif feed[1] is 'W':
                        delay = self.bgp_withdraw(feed)
                elif self.wiser:
                    if feed[1] is 'A':
                        delay = self.bgp_announce_wiser(feed)
                        ofp.write('{0}\t{1}\n'.format(line_n, str(delay * 1000)))
                    elif feed[1] is 'W':
                        delay = self.bgp_withdraw(feed)

                # RESIDUES
                elif self.miro_res:
                    if feed[1] is 'A':
                        ins_delay, pol_delay = self.bgp_announce_miro_residue(feed)
                        ofp.write('{0}\t{1}\n'.format(line_n, str(ins_delay * 1000)))
                        ofp_res.write('{0}\t{1}\n'.format(line_n, str(pol_delay * 1000)))
                    elif feed[1] is 'W':
                        delay = self.bgp_withdraw(feed)

                elif self.wiser_res:
                    if feed[1] is 'A':
                        ins_delay, pol_delay = self.bgp_announce_wiser_residue(feed)
                        ofp.write('{0}\t{1}\n'.format(line_n, str(ins_delay * 1000)))
                        ofp_res.write('{0}\t{1}\n'.format(line_n, str(pol_delay * 1000)))
                    elif feed[1] is 'W':
                        delay = self.bgp_withdraw(feed)

                elif self.miro_wiser_res:
                    if feed[1] is 'A':
                        ins_delay, pol_delay = self.bgp_announce_miro_wiser_residue(feed)
                        ofp.write('{0}\t{1}\n'.format(line_n, str(ins_delay * 1000)))
                        ofp_res.write('{0}\t{1}\n'.format(line_n, str(pol_delay * 1000)))
                    elif feed[1] is 'W':
                        delay = self.bgp_withdraw(feed)

                line_n += 1
        ofp.close()
        if logfile2 != "":
            ofp_res.close()
        return

    def add_policy(self, asn, prefix=None):
        if prefix == None:
            #TODO case where only want to avoid prefix
            return
        # Add policy filter
        policy_ins = "INSERT INTO policy VALUES('{}',{});"
        self.cur.execute(policy_ins.format(prefix, asn))
        return

    def bgp_withdraw(self, feed):
        # PREFIX, ASN
        prefix = feed[7]
        asn = feed[5]

        # Deletion from BGP table
        bgp_del = "DELETE FROM bgp WHERE prefix='{0}' AND aspath[1]={1};"
        bgp_del = bgp_del.format(prefix, asn)
        start = timer()
        self.cur.execute(bgp_del)
        end = timer()

        return end-start

    def load_miro_policies(self, infile, n):
        policies = []
        with open(infile,'r') as ifp:
            for l in ifp:
                feed = l.split('|')
                if (l.startswith('#') or l.isspace() or
                        feed[0] is not 'R' or feed[1] is not 'A'):
                    continue
                prefix = feed[7]
                aspath = feed[9].split()
                asn = (int(random.choice(aspath)) if len(aspath) <=3 
                        else int(random.choice(aspath[1:-1])))
                policies.append((prefix, asn))

        # Insert n random policies into policy table
        selected_policies = random.sample(policies, n)
        for pol in selected_policies:
            self.cur.execute("INSERT INTO policy VALUES ('{}', {})".format(pol[0], pol[1]))
        return

    def map_mincosts_wiser(self):
        self.ingress2cost = {}

        # Query neighbors' costs only once
        upcosts_sel = "SELECT next_hop, cost FROM upstream_costs;"
        start = timer()
        self.cur.execute(upcosts_sel)
        end = timer()
        delay = end-start

        # Map ingress routers to minimum costs to get to src
        upcosts_qry = self.cur.fetchall()
        for row in upcosts_qry:
            ingress = row[0]
            cost = row[1]
            if (ingress not in self.ingress2cost 
                    or cost < self.ingress2cost[ingress]):
                self.ingress2cost[ingress] = cost
        return delay

#=====| MIRO RESIDUE |========================================================#
    def load_miro_residue(self):
        self.miro_res = True
        print('Loaded Miro residue')
        return

    def bgp_announce_miro_residue(self, feed):
        # PREFIX, ASPATH
        prefix = feed[7]
        aspath_str = '{' + str(feed[9]).replace(' ',',') + '}'

        # INGRESS, EGRESS, COST
        assert(len(self.ingress) != 0), 'No ingress nodes'
        delay_ins = 0
        for ingress in self.ingress:
            egress = self.egress[random.randint(0, len(self.egress)-1)]
            cost = self.IGP[(ingress, egress)]

            # Insert into bgp, feed tables
            bgp_ins = "INSERT INTO bgp VALUES ('{}',{},{},'{}',{})"
            bgp_ins = bgp_ins.format(prefix, ingress, egress, aspath_str, cost)
            start = timer()
            self.cur.execute(bgp_ins)
            end = timer()
            delay_ins += end-start

        # Time decision delay, python version
        policy_qry, delay_pol = self.get_policies(prefix)
        # Convert policy asns and as paths to lists
        pol_asns = [b for a,b in policy_qry]
        entry_asns = [int(asn) for asn in feed[9].split()]

        # Policy already considers prefix, only need to consider feed's aspath
        start = timer()
        for asn in entry_asns:
            if asn in pol_asns:
                end = timer()
                delay_pol += end-start
                break
        end = timer()
        delay_pol += end-start
        return delay_ins, delay_pol

    def get_policies(self, prefix):
        policy_sel = "SELECT prefix, aspath FROM policy WHERE prefix='{}';"
        start = timer()
        self.cur.execute(policy_sel.format(prefix))
        end = timer()
        policy_qry = self.cur.fetchall()
        return policy_qry, end-start

    def generate_miro_residue(self, prefix, policy_qry):
        residue = ""
        residue_template = "{0} AND NOT (prefix='{1}' AND {2}=ANY(aspath))"
        for pol in policy_qry:
            residue = residue_template.format(residue, pol[0], pol[1])
        
        return residue, 0

#=====| WISER RESIDUE |=======================================================#
    def load_wiser_residue(self):
        self.cur.execute('''select egress from ingress_egress 
                where downstreamas = {} and upstreamas = {};'''.format(
                    self.upstreamAS, self.downstreamAS))
        tmp = self.cur.fetchone()
        self.wiserSource = tmp[0][random.randint(0, len(tmp[0])-1)]
        self.cur.execute('truncate table upstream_costs;')
        self.cur.execute('''with upstreamigp as (
                select ingress, egress, cost from alligp where asnum = {0}),
                links as (select source, target from peering_links 
                    where src_as = {0} and dst_as = {1}) 
                    insert into upstream_costs 
                    select ingress, egress, target, cost from 
                    upstreamigp join links on upstreamigp.egress = links.source 
                    where ingress = {2}'''.format(self.upstreamAS, 
                        self.downstreamAS, 
                        self.wiserSource))
        self.map_mincosts_wiser()
        self.wiser_res = True
        print('Loaded Wiser residue')
        return

    def bgp_announce_wiser_residue(self, feed):
        # PREFIX, ASPATH
        prefix = feed[7]
        aspath_str = '{' + str(feed[9]).replace(' ',',') + '}'

        # INGRESS, EGRESS, COST
        assert(len(self.ingress) != 0), 'No ingress nodes'
        delay_ins = 0
        for ingress in self.ingress:
            egress = self.egress[random.randint(0, len(self.egress)-1)]

            # Wiser cost
            cost = self.IGP[(ingress, egress)]
            upcost = self.ingress2cost[ingress]
            wisercost = cost + upcost

            # Insert into bgp table
            bgp_ins = "INSERT INTO bgp VALUES ('{}',{},{},'{}',{})"
            bgp_ins = bgp_ins.format(prefix, ingress, egress, aspath_str, wisercost)
            start = timer()
            self.cur.execute(bgp_ins)
            end = timer()
            delay_ins += end-start

        # Time query under constraint
        residue, delay_pol = self.generate_wiser_residue(prefix)
        wiser_sel = """SELECT * FROM bgp 
            WHERE prefix='{}' {}""".format(prefix,residue)
        start = timer()
        self.cur.execute(wiser_sel)
        end = timer()
        delay_pol += end-start
        return delay_ins, delay_pol

    def generate_wiser_residue(self, prefix):
        residue = "AND cost=(SELECT MIN(cost) FROM bgp WHERE prefix='{}')"
        residue = residue.format(prefix)
        return residue, 0


#=====| MIRO-WISER RESIDUE |==================================================#
    def load_miro_wiser_residue(self):
        self.cur.execute('''select egress from ingress_egress 
                where downstreamas = {} and upstreamas = {};'''.format(
                    self.upstreamAS, self.downstreamAS))
        tmp = self.cur.fetchone()
        self.wiserSource = tmp[0][random.randint(0, len(tmp[0])-1)]
        self.cur.execute('truncate table upstream_costs;')
        self.cur.execute('''with upstreamigp as (
                select ingress, egress, cost from alligp where asnum = {0}),
                links as (select source, target from peering_links 
                    where src_as = {0} and dst_as = {1}) 
                    insert into upstream_costs 
                    select ingress, egress, target, cost from 
                    upstreamigp join links on upstreamigp.egress = links.source 
                    where ingress = {2}'''.format(self.upstreamAS, 
                        self.downstreamAS, 
                        self.wiserSource))
        self.map_mincosts_wiser()
        self.miro_wiser_res = True
        print('Loaded MIRO-Wiser residue')
        return

    def bgp_announce_miro_wiser_residue(self, feed):
        # PREFIX, ASPATH
        prefix = feed[7]
        aspath_str = '{' + str(feed[9]).replace(' ',',') + '}'

        # INGRESS, EGRESS, COST
        assert(len(self.ingress) != 0), 'No ingress nodes'
        delay_ins = 0
        for ingress in self.ingress:
            egress = self.egress[random.randint(0, len(self.egress)-1)]

            # Wiser cost
            cost = self.IGP[(ingress, egress)]
            upcost = self.ingress2cost[ingress]
            wisercost = cost + upcost

            # Insert into bgp table
            bgp_ins = "INSERT INTO bgp VALUES ('{}',{},{},'{}',{})"
            bgp_ins = bgp_ins.format(prefix, ingress, egress, aspath_str, wisercost)
            start = timer()
            self.cur.execute(bgp_ins)
            end = timer()
            delay_ins += end-start

        # Get policies and miro residue
        policy_qry, delay_pol = self.get_policies(prefix)
        pol_asns = [b for a,b in policy_qry]
        miro_wiser_res,_ = self.generate_miro_wiser_residue(prefix, policy_qry)

        # Get preliminary query w/ mincost under MIRO constraint
        miro_wiser_sel = """SELECT * FROM bgp WHERE prefix='{}' {}"""
        miro_wiser_sel = miro_wiser_sel.format(prefix, miro_wiser_res)
        start = timer()
        self.cur.execute(miro_wiser_sel)
        end = timer()
        delay_pol += end-start
        miro_wiser_qry = self.cur.fetchall()

        # Policy already considers prefix, only need to consider feed's aspath
        start = timer()
        for qry in miro_wiser_qry:
            for asn in qry[3]:
                if asn in pol_asns:
                    end = timer()
                    delay_pol += end-start
                    break
        end = timer()
        delay_pol += end-start
        return delay_ins, delay_pol

    def generate_miro_wiser_residue(self, prefix, policy_qry):
        # Generate MIRO residue
        miro_residue, delay = self.generate_miro_residue(prefix, policy_qry)
        miro_wiser_residue = """AND 
            cost=(SELECT min(cost) FROM bgp WHERE prefix='{0}'{1})"""
        miro_wiser_residue = miro_wiser_residue.format(prefix, miro_residue)
        return miro_wiser_residue, delay # delay is 0

#=====| PRINTING |============================================================#
    def print_bgp(self):
        self.cur.execute('SELECT * FROM bgp;')
        bgp_qry = self.cur.fetchall()
        for bgp_row in bgp_qry:
            print(bgp_row)
        return

    def print_igp(self):
        for link, c in self.IGP.iteritems():
            print(str(link) + ' ' + str(c))
        return

    def print_policies(self):
        self.cur.execute('SELECT * FROM policy;')
        pol_qry = self.cur.fetchall()
        for pol in pol_qry:
            print(':- (prefix={}, ASN={})'.format(pol[0], pol[1]))
        return

    def DB_execute(self, query):
        self.cur.execute(query)

    def DB_fetchone(self):
        return self.cur.fetchone()

    def DB_fetchall(self):
        return self.cur.fetchall()

#=====| MIRO STRAWMAN |=======================================================#
    def load_miro(self):
        self.miro = True
        print('Loaded MIRO strawman')
        return

    def bgp_announce_miro(self, feed):
        # PREFIX, ASPATH
        prefix = feed[7]
        aspath_str = '{' + str(feed[9]).replace(' ',',') + '}'

        # Check against policy, if not compliant, do not insert
        policy_qry, delay = self.get_policies(prefix)
        for pol in policy_qry:
            if str(pol[1]) in feed[9].split():
                return delay
            
        # INGRESS, EGRESS, COST 
        for ingress in self.ingress:
            egress = self.egress[random.randint(0, len(self.egress)-1)]
            cost = self.IGP[(ingress, egress)]

            # Insertion delay
            bgp_ins = "INSERT INTO bgp VALUES ('{}',{},{},'{}',{})"
            bgp_ins = bgp_ins.format(prefix, ingress, egress, aspath_str, cost)
            start = timer()
            self.cur.execute(bgp_ins)
            end = timer()
            delay += end-start

        return delay


#=====| WISER STRAWMAN |======================================================#
    def load_wiser(self):
        # pick a source from the upstream AS for the Wiser experiment
        self.cur.execute('select egress from ingress_egress where downstreamas = {} and upstreamas = {};'.format(self.upstreamAS, self.downstreamAS)) 
        # choose the source among the border nodes of the upstream AS that do 
        # not peer with the downstream. If we exchange the role of downstream 
        # and upstream and query for the egress nodes, the egress nodes would 
        # be those border nodes we want.
        tmp = self.cur.fetchone()
        self.wiserSource = tmp[0][random.randint(0, len(tmp[0])-1)]
        self.cur.execute('truncate table upstream_costs;')
        self.cur.execute('''with upstreamigp as (
                select ingress, egress, cost from alligp where asnum = {0}),
                links as (select source, target from peering_links 
                    where src_as = {0} and dst_as = {1}) 
                    insert into upstream_costs 
                    select ingress, egress, target, cost from 
                    upstreamigp join links on upstreamigp.egress = links.source 
                    where ingress = {2}'''.format(self.upstreamAS, 
                        self.downstreamAS, 
                        self.wiserSource))

        # Setup upstream map
        self.map_mincosts_wiser()
        self.wiser = True
        print('Loaded Wiser strawman')
        return

    def bgp_announce_wiser(self, feed):
        # PREFIX, ASPATH
        prefix = feed[7]
        aspath_str = '{' + str(feed[9]).replace(' ',',') + '}'

        # INGRESS, EGRESS, COST
        assert(len(self.ingress) != 0), 'No ingress nodes'
        min_wisercost = None
        min_entry = None
        for ingress in self.ingress:
            egress = self.egress[random.randint(0, len(self.egress)-1)]

            # Wiser cost: sum of normalized received cost and internal cost.
            igpcost = self.IGP[(ingress, egress)]
            upcost = self.ingress2cost[ingress]
            wisercost = igpcost + upcost
 
            # If wiser cost is lower than current cost, do not insert
            if min_wisercost == None or wisercost < min_wisercost:
                min_wisercost = wisercost
                entry = (prefix, ingress, egress, aspath_str, wisercost)

        # If table is miro compliant, should only be one min cost in table
        min_currcost_sel = "SELECT cost FROM bgp WHERE prefix='{0}';"
        min_currcost_sel = min_currcost_sel.format(prefix)
        start = timer()
        self.cur.execute(min_currcost_sel)
        end = timer()
        delay = end-start
        min_currcost_qry = self.cur.fetchall()
        if min_currcost_qry != [] and min_currcost_qry[0] < min_wisercost:
            return delay

        # If minimum is no longer minimum, delete
        if min_currcost_qry != []:
            min_currcost_del = "DELETE FROM bgp WHERE prefix='{0}'"
            min_currcost_del = min_currcost_del.format(prefix)
            start = timer()
            self.cur.execute(min_currcost_del)
            end = timer()
            delay += end-start

        # Insertion delay
        bgp_ins = "INSERT INTO bgp VALUES ('{}',{},{},'{}',{})"
        bgp_ins = bgp_ins.format(entry[0], entry[1], entry[2], entry[3], entry[4])
        start = timer()
        self.cur.execute(bgp_ins)
        end = timer()
        return delay + end-start

    def load_wiser_check_in_db(self):
        '''
        Check Wiser policy using triggers in database side. Do not use this function with load_wiser().
        '''
        s = open(os.path.join(pyPath, 'experiment_wiser.sql')).read()
        self.cur.execute(s)
        # pick a source from the upstream AS for the Wiser experiment
        self.cur.execute('select egress from ingress_egress where downstreamas = {} and upstreamas = {};'.format(self.upstreamAS, self.downstreamAS)) # choose the source among the border nodes of the upstream AS that do not peer with the downstream. If we exchange the role of downstream and upstream and query for the egress nodes, the egress nodes would be those border nodes we want.
        tmp = self.cur.fetchone()
        self.wiserSource = tmp[0][random.randint(0, len(tmp[0])-1)]
        self.cur.execute('truncate table upstream_costs;')
        self.cur.execute('with upstreamigp as (select ingress, egress, cost from alligp where asnum = {0}), links as (select source, target from peering_links where src_as = {0} and dst_as = {1}) insert into upstream_costs select ingress, egress, target, cost from upstreamigp join links on upstreamigp.egress = links.source where ingress = {2}'.format(self.upstreamAS, self.downstreamAS, self.wiserSource))
        self.cur.execute('select load_wiser()')

    def unload_wiser(self):
        '''
        Unload Wiser policy checking triggers.
        '''
        self.wiser = False
        self.cur.execute('select unload_wiser()')

def run(upstreamAS, downstreamAS, exp, data):
    ribfile = 'rib{0}.txt'.format(data[3])
    inslogfile = 'Gnuplot/log/{0}_{1}_{2}.log'.format(downstreamAS, upstreamAS,exp)
    print('-'*80)
    print(inslogfile)
    if data[0] == 'residue':
       print(inslogfile.replace('init','residue'))

    exp = Experiment(dbname=databaseName, user=databaseUser, password=databasePassword,host=databaseHost, port=databasePort)
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
       exp.load_miro_policies(ribfile, data[2])
       print('Loaded {} policies'.format(data[2]))
    else:
       print('Loaded 0 policies')

    start = timer()
    if data[0] == 'residue':
       exp.load_bgp(ribfile, inslogfile, inslogfile.replace('init','residue'))
    else:
       exp.load_bgp(ribfile, inslogfile)
    end = timer()
    delay = (end-start)
    print('Loaded ' + ribfile + ' in ' + str(delay) + 's')


if __name__ == '__main__':
    downstreamAS = 2914
    upstreamAS = 1239
    experiments = {
           #'residue_wiser_0pol_init_100':('residue','wiser',0,100),
           #'residue_wiser_0pol_init_10000':('residue','wiser',0,10000),
           #'residue_miro_xpol_init_100':('residue','miro',20,100),
           #'residue_miro_xpol_init_10000':('residue','miro',20,10000),
           #'residue_combine_xpol_init_100':('residue','combine',20,100),
           'residue_combine_xpol_init_10000':('residue','combine',20,100),
           #'strawman_miro_0pol_init_100':('strawman','miro',0,100),
           #'strawman_miro_0pol_init_10000':('strawman','miro',0,10000),
           #'strawman_miro_xpol_init_100':('strawman','miro',20,100),
           #'strawman_miro_xpol_init_10000':('strawman','miro',20,10000),
           #'strawman_wiser_0pol_init_100':('strawman','wiser',0,100),
           #'strawman_wiser_0pol_init_10000':('strawman','wiser',0,10000)
           }

    for exp, data in experiments.iteritems():
        run(upstreamAS, downstreamAS, exp, data)

    run_plot()
