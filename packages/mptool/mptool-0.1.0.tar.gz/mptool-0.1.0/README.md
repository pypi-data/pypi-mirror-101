![mptool](mptool.png)

# Enumeration and sampling of minimal pathways in metabolic (sub)networks

This repository contains a Python module with implementations of methods for metabolic pathway enumeration and sampling as well as notebooks that reproduce the results presented in [our paper](https://www.biorxiv.org/content/10.1101/2020.07.31.230177v2) [1].

Minimal pathways (MPs) are minimal sets of reactions that need to be active (have non-zero flux) in a metabolic (sub)network to satisfy all constraints on the network as a whole [1]. They can also be defined as the set of *support-minimal* elementary flux vectors (EFVs) [2].

An MP can be found by direct minimization of a mixed-integer linear program (MILP) or by iterative minimization of multiple linear programs (LPs). Enumeration of MPs is implemented using both of these approaches, in the iterative case by computing minimal cut sets (MCSs) in a separate binary integer program (BIP) [3]. For iterative minimzation, enumeration can be accelerated by using a graph defined by the known MPs to predict unknown MPs, or it can be randomized to allow random sampling of MPs in cases where complete enumeration is inconvenient or infeasible.

## Requirements

To run the code in this repostitory, you will need Python (tested with version 3.7.0) and `gurobipy`, the Python interface of the Gurobi Optimizer (tested with versions 7.5.2, 8.1.0, and 9.0.0). The specific packages that were used in the testing environment are listed in `requirements.txt`.

## Installation
You can install `mptool` using [pip](https://pypi.org/project/mptool/):
```
pip install mptool
```
This will also install all minimal requirements except `gurobipy`, which must be installed separately.

## Instructions

To enumerate or sample MPs, use the functions provided in `mptool.py` or run it directly as a script:
```
python mptool.py <model file> <bounds file>
```
A model in `.xml`, `.json`, or `.mat` format is required and a `.csv` file containing bounds for the model (reaction ID, lower bound, and upper bound on each line) is optional. The bounds can also be specified in the model itself and should include a functional requirement such as a minimal growth rate. If no bounds file is provided, flux variability analysis (FVA) will be run by default to determine tight bounds for all fluxes. The parameters of the procedure and the subnetwork in which to enumerate or sample MPs can easily be modified in the script.

When run as a script, `mptool.py` will enumerate MPs (and MCSs) in a random subnetwork (consisting of 1 / 6 of the reactions in the model) using iterative minimization with graph. Example bounds are provided for a core and a genome-scale *E. coli* model:
```
python mptool.py models/e_coli_core.json data/e_coli_core_example_bounds.csv
python mptool.py models/iML1515.json data/iML1515_example_bounds.csv
```

The notebooks `benchmarking.ipynb`, `e_coli_sampling.ipynb`, and `host_microbe_enumeration.ipynb` reproduce our results from benchmarking methods, sampling *E. coli* central carbon metabolism, and enumerating host-microbe metabolite exchanges, respectively. Models were obtained from [BiGG](http://bigg.ucsd.edu) [4] and [Virtual Metabolic Human](https://www.vmh.life/) [5].

## References

[1] O. Øyås and J. Stelling. "Scalable metabolic pathway analysis". *biorXiv* (2020).

[2] S. Klamt et al. "From elementary flux modes to elementary flux vectors: Metabolic pathway analysis with arbitrary linear flux constraints". *PLoS Computational Biology* 13.4 (2017).

[3] H.S. Song et al. "Sequential computation of elementary modes and minimal cut sets in genome-scale metabolic networks using alternate integer linear programming". *Bioinformatics* 33.15 (2017).

[4] Z.A. King et al. "BiGG Models: A platform for integrating, standardizing, and sharing genome-scale models" *Nucleic Acids Research* 44.D1 (2016).

[5] A. Noronha et al. "The Virtual Metabolic Human database: integrating human and gut microbiome metabolism with nutrition and disease" *Nucleic Acids Research* 47.D1 (2018).
