![CI](https://github.com/the-grayson-group/SmoothTransitions/actions/workflows/test.yml/badge.svg)
![Publish](https://github.com/the-grayson-group/SmoothTransitions/actions/workflows/publish.yml/badge.svg)
# Smoothtransitions
## Overview

Smoothtransitions is a commandline tool for running workflows that aims to identify ground state and/or transition state structures in chemical reactions given a set of starting geometries.

For each of the candidate structures, a typical workflow might include:

- A constrained optimisation
- A series of unconstrained optimisations that last until the structure has converged or reached a maximum number of optimisation stages
- A single point energy calculation on the final optimised structure but only if it previously converged previously during optimisation

Running this workflow manually can be very laborious and error prone, especially when done for many structures at the same time, but smoothtransitions can make this process a lot easier.
Each stage in the workflow, and all necessary options for it, can be defined in a single configuration file.
This includes:

- SLURM settings for each stage
- Gaussian settings for each stage
- Number of iterations for each stage
- etc.

After defining these settings, smoothtransitions will handle the rest of the work. Starting from a folder containing a configuration file and the initial structures as mol2 files, smoothtransitions will:

- create subfolders for each stage and iteration and save properly named input and output files into these subfolders
- generate and submit the necessary SLURM scripts
- track the progress of the workflow in a log file
- upon completion of one SLURM job, determine the next action and submit further jobs as necessary

If no mol2 files are available, smoothtransitions can also handle conversion from most molecular formats into gaussian input files.

Smoothtransitions offers the following advantages:

- no more mistakes when manually modifying gaussian output files to new input files in order to continue a simulation
- no more wasted time because jobs finish at night or on the weekend when manual submission of the next batch may not be possible
- consistent structure for each experiment that can be shared across teams

This has allowed us to run transition state calculations over hundreds of candidate molecules.

Additional features in the pipeline include:

- automated generation of graphs such as atom distances
- automated analysis of SPE runs using tools such as goodvibes
- automated custom analysis after any stage

## Risks

Smoothtransitions will submit jobs in the users name on a HPC system. This bears the same risks as any other automated way of submitting jobs to a HPC system, and hence care should be taken, especially when using smoothtransitions to submit jobs to paid queues. Depending on its configuration, the application can potentially submit many simulations, generating costs equivalent to the run simulations. The authors of this tool take no responsibility for incurred cost by using this tool.

## Installation

The only requirement is openbabel (either version 2.4.1 or 3.1.1) and the respecitve Python bindings that come with it.
The best way to install them is using conda but on a HPC system `openbabel` and its Python bindings might already be
installed as a module. To check this run `module avail` or open a Python prompt via `python` and see if `import pybel` or `from openbabel import pybel` work.

If the requirements are fullfilled, installing smoothtransitions is as easy as: `pip install smoothtransitions`

Using a virtual environment for your smoothtransitions setup is recommended.

### Installing openbabel and smoothtransitions together
This assumes that anaconda, miniconda oder miniforge are installed on the system.
1) `conda create --name smoothtransitions python=3.7` # 3.6 and 3.8 are supported as well
2) `conda activate smoothtransitions` # depending on your conda version this might also be `source activate smoothtransitions`
3) `conda install -c conda-forge openbabel=3.1.1`
4) `pip install smoothtranstions`

### Additional instructions only for users of the Bath HPC Cluster:

- Add `module load anaconda3/2.5.0` into your `.bashrc` file and make sure to DELETE `module load openbabel/2.4.1`
- Follow the instructions above for installing `openbabel` and `smoothtransitions` together

# Running SmoothTransitions:

## General commands

```
smoothtransitions
Usage: smoothtransitions [OPTIONS] COMMAND [ARGS]...
  --help                          Show this message and exit.

Commands:
  io            Function that handles creating gjf files from various input...
  report        Run the reporting logic for all structures provided.
  runner        This command will do two things: 1) Determine what needs to...
  workflow      This function will start or continue a workflow defined by...
  workflow-log  Small command to print the workflow log nicely in the...
```

- `smoothtransitions workflow` this is the workhorse of the application as it will start or continue a defined workflow and call other commands internally
- `smoothtransitions io` allows the generation of Gaussian input files (`*.gjf`) from different input formats
- `smoothtransitions report` allows manual recording of simulation runs in a project logfile
- `smoothtransitions runner` allows manual running of individual simulation stages
- `smoothtransitions workflow-log` prints the log of the current experiment nicely to the command line.

For a detailed example, see the example folder.

## Structure of a configuration file

The following describes the structure of a configuration file. The format is always a yaml file.

A config file will always have the following general structure:

```
project_name: <some name>
first-stage: <first stage to run>

# one or more stages
<stage-name>:
  <configuration of the stage>

smoothtransitions:
  <configuration of the smoothtransitions steps>
```

A stage always needs the following structure, here we call the stage `optimisation`:
```
optimisation:
  next-stage: SPE # a further stage name or "abort"
  # what to do when the maximum number of iterations is reached
  after-max-iter: optimisation # a stage name or "abort"
  max-iter: 1 # number of iterations (slurm runs) to run
  gaussian:
    <configuration of the gaussian setup>
  slurm:
    <configuration of the slurm job>
```

### Special sections

There are currently three special stages, the first two are based on our current workflow and can be used or omitted. The third is a special section for the smoothtransitions commands that need to be run to keep the workflow running.

#### constraint
This section defines a stage that has additional requirements in terms of gjf files. In particular it allows us to define bond constraints to be added to the gjf file for running constrained optimisations.

#### SPE
This section defines a single point energy calculation which in our typical workflow defines the last step and therefore in some cases is treated differently.

#### smoothtransitions
This section defines all the commands that need to be run to keep the workflow running. Smoothtransitions achieves the submission of subsequent jobs in a workflow by running dependent commands. After each gaussian run, a report and runner job are run that depend on the previous in order to log the results of the previous run to the project log (report job) and then figure out and run the next jon (runner).

An example with just one stage is shown below:

```
project_name: "peroxide" # basic information
first-stage: constraint # the workflow needs to know which stage is the first in the workflow

constraint: # first level keys identify stages or general settings
  # basic workflow information
  # which stage to run after the current one
  next-stage: optimisation # a stage name or "abort"
  # what to do when the maximum number of iterations is reached
  after-max-iter: optimisation # a stage name or "abort"
  max-iter: 1 # number of iterations (slurm runs) to run
  # section that define all the gaussian settings
  gaussian:
    # this section will create the following gaussian header:
    # ---------------------------------------
    # %nprocshared=16
    # %mem=48GB

    # B3LYP/6-31G(d), opt=(calcfc, modredundant, maxcycles=80, maxstep=10), freq=noraman, geom=connectivity
    # ---------------------------------------
    # define all link 0 details, see gaussian documentation for valid keywords
    link_0:
      nprocshared: "16"
      mem: "48GB"
    # define all route details, see gaussian documentation for valid keywords
    route:
      # text that appear without a keyword before them need to be declared as such
      # (e.g. maxcycles below is a keyword before the value "80")
      non_keywords: "B3LYP/6-31G(d)"
      opt:
        non_keywords: "calcfc, modredundant"
        maxcycles: "80"
        maxstep: "10"
      freq: noraman
      geom: connectivity
  # additional bond constraints to be added (only for constraint sections)
  # This will add "B 1 2 F" at the end of the gjf file
  constraint:
    - "B 1 2 F"
  # all settings for the slurm job this will create a slurm submission script
  slurm:
    settings:
      job-name: "constraint" # this should be some overall name
      time: "00:10:00" # walltime for the job
      mem: "48000"
      nodes: "1"
      ntasks: "1"
      cpus-per-task: "16"
      partition: "batch-all"
      account: "free"
    # actual command to be run on submission, this will differ for your setup
    command: |
      export GAUSS_SCRDIR=$SCRATCH

      module purge
      module load slurm
      module load gaussian/16

      source $g16profile

      g16 < $gjf_file > $outputfile

# special section for smoothtransitions jobs that need to run after a gaussian job
smoothtransitions:
  slurm:
    settings:
      time: "00:05:00"
      mem: "48000"
      nodes: "1"
      ntasks: "1"
      cpus-per-task: "16"
      partition: "batch-all"
      account: "free"

    # this command will record the previous job in the project log
    report-command: |
      module purge
      module load slurm
      module load anaconda3/2.5.0

      source activate smoothtransitions

      smoothtransitions report $gaussianoutfile --config-file $configfile --project-file $projectfile

    # this command will record the previous job in the project log
    runner-command: |
      module purge
      module load slurm
      module load anaconda3/2.5.0

      source activate smoothtransitions

      smoothtransitions runner $gaussianoutfile --config-file $configfile --project-file $projectfile
```
