# slim_magic
This package provides a few ipython magic functions
for (population genetic) simulation using SLiM 
([Haller and Messer, 2019](https://doi.org/10.1093/molbev/msy228)). 
These magic functions are not 
meant for heavy, computation.
Instead they are aimed at 
teaching, or gaining a quick
intuition for what a simulation
might produce, without
using the excellent SLiM GUI. 

The basic idea is that the magic functions will 
execute a cell with a SLiM code block behind the 
scenes and return to the user either a dataframe
full of summaries output by the code or 
a tree sequence. 

## Installation
To install `slim_magic` take the following steps, starting with
cloning this repo

```
$ git clone git@github.com:andrewkern/slim_magic.git
$ cd slim_magic
```
(optional) create a new conda environment or similar
```
$ conda create -n slim_magic python=3.8 --yes
$ conda activate slim_magic
```
that will take a minute. now install the
`slim_magic` ipython extension
```
$ python setup.py install
```
## usage
Currently there are four separate magic functions implemented, please
see `example_magic.ipynb` for a jupyter notebook example.
you can fire that up at the command line with

```
$ jupyter notebook
```

The four functions are `%%slim_stats`, `%%slim_stats_reps_cstack`, 
`%%slim_stats_reps_rstack`, and `%%slim_ts`

