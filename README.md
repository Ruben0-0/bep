# IDENTIFYING IDEAL SEQUENCES
-------------------------------------------------
This code contains two main blocks:
1. Synthetic sequence model
2. Quantitative optimization method developed
   by Peter M. Burgess (2016)
-------------------------------------------------
It is possible to create synthetic sequences 
and then subsequently run them through Burgess'
optimization method; it is also possible to
load in custom datasets and run them through
Burgess' optimization method. An example of this
has been provided under the directory "Data from
Saputra" where three stratigraphic logs are
read from Excel files and run through the
algorithm. More examples of the usage of both
block 1 and block 2 are available in the 
directory "Workstation".

-------------------------------------------------
The dataset belonging to the original thesis
can be obtained at:
- https://drive.google.com/file/d/1bA8eNNvAoClY1M_1zhYnwSPLEnPZ6s29/view?usp=sharing

-------------------------------------------------

## Usage:

### Creating synthetic sequences

There are two functions of relevance for the
user: _sequencer_, found in the Python file
_synthseq_; and _gausian_noise_, found in the
Python file _noisify_. 

The sequencer function builds the synthetic 
sequence according to its input parameters 
without adding any gamma noise. If the input 
parameter _asymmetric_ is set to true, sequencer
will return the synthetic profile without adding
any gamma noise. The output can be directly used
as input for Burgess' algorithm (block 2).

If asymmetric is set to false, sequencer's output
can be directly used as input by the function 
_gaussian_noise_. This function adds a measure of
gamma noise to the synthetic profile according
to the user's input. The output of gaussian_noise
can be directly used as input for Burgess'
algorithm (block 2).

The input variables of relevance are:
- depths
- lithologies
- layout
- res
- n
- alpha<sup>*
- beta<sup>*
- gamma<sup>*
- psi<sup>*
- omega<sup>*

Variables _depths_, _lithologies_, and _layout_
define a single parasequence and its figure 
properties  (layer colors and patterns) on which
the creation of the synthetic profile is based.
Variable 'res' sets the grid spacing within the
synthetic profile. It is inversely proportional
to the sampling rate. 
Variable _n_ sets the total number of para-
sequences to be generated.

<sup>*For an explanation of these variables, please
 refer back to the original thesis.
 
### Burgess' quantitative optimization method

The only function of relevance for the user here
is _main_ found in the Python file _main.py_ in
the directory _Burgess_Model_. 

The following input variables are of relevance:
- depths
- lithologies
- layout
- res
- n

Variables _depths_, _lithologies_ and _layout_
now define the ENTIRE stratigraphic profile, and
the figure properties (layer colors and
patterns). 
Variables _res_ and _n_ must be carried over if
the input profile is synthetic. If not, they
are only relevant in figure layout settings.
Setting these to res=5 and n=6 will usually
suffice in creating proportional figures.


## Troubleshooting:

Sometimes the synthetic sequence model will
encounter errors in spite of correct input
parameters. This can have the following causes:

* Either the parasequence or layer thickness 
distributions extend to negative values. When
a negative thickness is drawn, an error will
be raised within _syn.consistent_range()_. Make
sure none of the distributions extend toward
negative values by adjusting their means or
skewness.

## Acknowledgements:

All credit for the algorithm in block 2 belongs
to its original creator, Peter M. Burgess.
For more information, please see:
- https://doi.org/10.1130/G37827.1
- https://doi.org/10.2110/jsr.2016.10

Furthermore, I want to express my gratitude to
my thesis supervisors, Prof. H.A. Abels and 
Prof. S.C. Toby, for their feedback, guidance,
and expertise throughout the project.

## Contact:

For any questions regarding the code or its 
usage, please contact:

- github.com/Ruben0-0

-------------------------------------------------
Ruben J. van Tartwijk
