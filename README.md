# Database-defined Interdomain Routing Policies Experiments

To run the experiment, make sure the following files are under the same directory:
* experiment\_setup.py
* experiment\_setup.sql
* allIGP
* AS\_links
* ingress\_egress
* peering_links
* rib100.txt, rib10000.txt, rib1000000.txt

## Data
Rib data obtained from Routeviews:

http://archive.routeviews.org/bgpdata/2003.01/UPDATES/updates.20030101.0005.bz2

It was preprocessed using the following bgpreader command:
```bgpreader -i -d singlefile -o rib-file,http://archive.routeviews.org/bgpdata/2003.01/UPDATES/updates.20030101.0005.bz2 | head -n <number of lines>```

## Running the experiment
```./experiment_setup.py```

### the Strawman method

* MIRO experiment

    Running the experiment using the MIRO method:
    ```Python
    exp = Experiment()                                # Initialize experiment and database
    exp.setup(1239, 2917)                             # Create tables for given downstream, upstream AS
    exp.load_strawman()

    exp.add_policy('216.79.72.0/24', 6389)            # Add policy to avoid prefix and AS path
    exp.load_bgp('rib100.txt', 'insertiondelay.log')  # Load RIB file, time insertions, and output to file
    ```

* Wiser experiment

    Running the experiment using the Wiser strawman method:
    ```Python
    exp = Experiment()                                # Initialize experiment and database
    exp.setup(1239, 2917)                             # Create tables for given downstream, upstream AS
    exp.load_wiser()                                  # Load Wiser policy checking triggers
    exp.load_bgp('rib100.txt', 'insertiondelay.log')  # Load RIB file, time insertions, and output to file
    exp.unload_wiser()                                # Unload the policy checking triggers when experiment finished
    ```

### the Residue method
Running the experiment using the residue method:
```Python
exp = Experiment()
exp.setup(1239, 2917)
exp.load_residue()

exp.add_policy('216.79.72.0/24', 6389)
exp.load_bgp('rib100.txt', 'insertiondelay.log')
```

## Memory usage measurement
The `experiment_RAM_usage.py` measure the memory usage using the `top` command. the `run` function in the `experiment_RAM_usage.py` is the function that runs the experiment and collects the memory usage data. Given an experiment setup (the downstream AS, the upstreamAS, scenario and the BGP feeds number) and the number of points to collect, say N, the `run` function will issue the `top` command after every (BGP_feeds_number\N) BGP feeds consumptions, and write the result to the `<scenario>_ram.log` file in the `Gnuplot\log` folder.

For example, the following codes run the MIRO experiment with the residue method using 1000,000 BGP feeds, and then collects the memory usage for every 10,000 BGP feeds consumptions.

```Python
downstreamAS = 2914
upstreamAS = 1239
experiments = {
    'miro_residue':('residue','miro',20,1000000),
    }
for exp, data in experiments.iteritems():
    run(upstreamAS, downstreamAS, exp, data, 100)
```

## Log file:

* BGP feeds processing delays

    Filename format: \<downstream AS\>\_\<upstream AS\>\_\<operation measured\>\_\<BGP feeds read\>.log

    Data format: \<BGP feed row number\>    \<Processing delay in milliseconds\>

* Memory usage

    Filename format: \<scenario\>\_ram.log

    Data format: Every two lines form a data point. The first line gives the number of BGP feeds processed, and the second line gives the information returned by the `top` command, which has the following fields:

    PID, USER, PR, NI, VIRT, RES, SHR, S, %CPU, %MEM, TIME+ COMMAND

    We are interested in the RES filed which stands for the physical memory taken by current connection to the database. For the meaning of other fields, please refer to the top command [manual](http://man7.org/linux/man-pages/man1/top.1.html).
