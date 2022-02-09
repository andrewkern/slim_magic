from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)
from io import StringIO
import os
import subprocess
import pandas as pd


@magics_class
class SlimMagic(Magics):

    @cell_magic
    def slim_stats(self, name, cell):
        """
        slim_stats returns a pandas df in which
        a SLiM simulation has been run, its output captured.
        Contents of the cell specify the complete SLiM
        simulation.
        
        Output from simulation is expected to be a comma-delimited
        list of summaries printed from slim to stdout. by convention
        the header row begins with 'generation' e.g.,
        
        generation, stat1, stat2, ... , statn
        """
        script = cell
        logfile = "tmp.log"
        os.system("echo '" + script + "' | slim > " + logfile)
        # deal with slim output header lines
        pattern = "generation,"
        count = 0
        with open(logfile, "r") as f:
            for line in f:
                if pattern in line:
                    break
                else:
                    count += 1
        df = pd.read_csv(logfile, skiprows=count)
        df = df.set_index('generation')
        return df

    @cell_magic
    def slim_stats_reps_cstack(self, reps, cell):
        """
        slim_stats_reps_cstack returns a pandas df in which
        reps number of replicate SLiM simulations have been
        run, and their output captured, and then column stacked,
        merging along rows.
        
        output from simulation is expected to be a comma-delimited
        list of summaries printed from SLiM to stdout. by convention
        the header row begins with 'generation' e.g.,
        
        generation,stat1_rep1,stat2_rep1,...,statn_rep1,...,stat1_repn,...
        """
        script = cell
        n = int(reps)
        aList = []
        for i in range(n):
            logfile = "tmp.log"
            os.system("echo '" + script + "' | slim > " + logfile)
            # deal with slim output header lines
            pattern = "generation,"
            count = 0
            with open(logfile, "r") as f:
                for line in f:
                    if pattern in line:
                        break
                    else:
                        count += 1
            df = pd.read_csv(logfile, skiprows=count)
            df = df.set_index('generation')
            # sucking everything up from log file
            aList.append(df)
        # below concat means that all columns will
        # have same names among reps
        dff = pd.concat(aList, axis=1, join="inner")
        return dff
        
    @cell_magic
    def slim_stats_reps_rstack(self, reps, cell):
        """
        slim_stats_reps_rstack returns a pandas df in which
        reps number of replicate slim simulations have been
        run, and their output captured, and then row stacked, merging
        along columns. 
        
        output from simulation is expected to be a comma-delimited
        list of summaries printed from slim to stdout. by convention
        the header row begins with 'generation' e.g.,
        
        generation,stat1,stat2,...,statn
        """
        script = cell
        n = int(reps)
        aList = []
        for i in range(n):
            logfile = "tmp.log"
            os.system("echo '" + script + "' | slim > " + logfile)
            # deal with slim output header lines
            pattern = "generation,"
            count = 0
            with open(logfile, "r") as f:
                for line in f:
                    if pattern in line:
                        break
                    else:
                        count += 1
            df = pd.read_csv(logfile, skiprows=count)
            df = df.set_index('generation')
            aList.append(df)
        dff = pd.concat(aList)
        return dff
        

