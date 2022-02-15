from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)
from IPython.core import magic_arguments
from IPython.utils.process import arg_split
from io import StringIO
import os
import sys
import subprocess
import pandas as pd
import tskit

def slim_magic_args(f):
    """single decorator for adding script args"""
    args = [
        magic_arguments.argument(
            '--out', type=str,
            help="""The variable in which to store output from the script.            
            """
        ),
    ]
    for arg in args:
        f = arg(f)
    return f

def slim_magic_args_reps(f):
    """single decorator for adding script args"""
    args = [
        magic_arguments.argument(
            'num_reps', type=int,
            help="""The number of replicate simulations to run.            
            """
        ),
        magic_arguments.argument(
            '--out', type=str,
            help="""The variable in which to store output from the script.            
            """
        ),
    ]
    for arg in args:
        f = arg(f)
    return f
@magics_class
class SlimMagic(Magics):

    @magic_arguments.magic_arguments()
    @slim_magic_args
    @cell_magic
    def slim(self, line=None, cell=None):
        """
        slim runs a SLiM simulation and prints the resulting stdout.
        %%slim
        """
        argv = arg_split(line, posix=not sys.platform.startswith("win"))
        args, cmd = self.slim_stats.parser.parse_known_args(argv)
        script = cell
        logfile = "tmp.log"
        os.system("echo '" + script + "' | slim > " + logfile)
        with open(logfile, "r") as f:
            log = f.read()
        if args.out:
            self.shell.user_ns[args.out] = log
        else:
            print(log)
        return

    
    @magic_arguments.magic_arguments()
    @slim_magic_args
    @cell_magic
    def slim_stats(self, line=None, cell=None):
        """
        slim_stats returns a pandas df in which
        a SLiM simulation has been run, its output captured.
        Contents of the cell specify the complete SLiM
        simulation.
        
        Output from simulation is expected to be a comma-delimited
        list of summaries printed from slim to stdout. by convention
        the header row begins with 'generation' e.g.,
        
        generation, stat1, stat2, ... , statn

        usage:
        %%slim_stats 
        """
        argv = arg_split(line, posix=not sys.platform.startswith("win"))
        args, cmd = self.slim_stats.parser.parse_known_args(argv)
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
        if args.out:
            self.shell.user_ns[args.out] = df
            return
        else:
            return df

    @magic_arguments.magic_arguments()
    @slim_magic_args_reps
    @cell_magic
    def slim_stats_reps_cstack(self, line, cell):
        """
        slim_stats_reps_cstack returns a pandas df in which
        num_reps number of replicate SLiM simulations have been
        run, and their output captured, and then column stacked,
        merging along rows.
        
        output from simulation is expected to be a comma-delimited
        list of summaries printed from SLiM to stdout. by convention
        the header row begins with 'generation' e.g.,
        
        generation,stat1_rep1,stat2_rep1,...,statn_rep1,...,stat1_repn,...
       
        """
        argv = arg_split(line, posix=not sys.platform.startswith("win"))
        args, cmd = self.slim_stats_reps_cstack.parser.parse_known_args(argv)
        script = cell
        n = int(args.num_reps)
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
        if args.out:
            self.shell.user_ns[args.out] = dff
            return
        else:
            return dff
    
    @magic_arguments.magic_arguments()
    @slim_magic_args_reps
    @cell_magic
    def slim_stats_reps_rstack(self, line, cell):
        """
        slim_stats_reps_rstack returns a pandas df in which
        num_reps number of replicate slim simulations have been
        run, and their output captured, and then row stacked, merging
        along columns. 
        
        output from simulation is expected to be a comma-delimited
        list of summaries printed from slim to stdout. by convention
        the header row begins with 'generation' e.g.,
        
        generation,stat1,stat2,...,statn

        """
        argv = arg_split(line, posix=not sys.platform.startswith("win"))
        args, cmd = self.slim_stats_reps_rstack.parser.parse_known_args(argv)
        script = cell
        n = int(args.num_reps)
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
        if args.out:
            self.shell.user_ns[args.out] = dff
            return
        else:
            return dff
        
    @magic_arguments.magic_arguments()
    @slim_magic_args
    @cell_magic
    def slim_ts(self, line=None, cell=None):
        """
        slim_ts returns a tree sequence object resulting
        from the SLiM simulation.
        Contents of the cell specify the complete SLiM
        simulation.

        usage:
        %%slim_ts cell_script
        """
        argv = arg_split(line, posix=not sys.platform.startswith("win"))
        args, cmd = self.slim_ts.parser.parse_known_args(argv)
        script = cell
        logfile = "tmp.log"
        os.system("echo '" + script + "' | slim > " + logfile)
        ts = tskit.load("tmp.trees")
        # TODO: delete tmp.trees and tmp.log
        if args.out:
            self.shell.user_ns[args.out] = ts
            return
        else:
            return ts
