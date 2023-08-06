# CPrAA - A Checker for Probabilistic Abstract Argumentation

[![PyPI](https://img.shields.io/pypi/v/cpraa "View CPrAA on PyPI")](https://pypi.org/project/cpraa/)

CPrAA is a Python tool and package for various tasks in probabilistic abstract argumentation:
 * find distributions satisfying numerous probabilistic argumentation semantics
 * check for credulous or skeptical acceptance of arguments
 * maximize or minimize the marginal probability of certain arguments
 * generate labelings according to different labeling schemes


## Installation

CPrAA is available on [PyPI](https://pypi.org/project/cpraa/) and can be installed with `pip`:

    pip install cpraa

Note that Python 3.7 or higher is required.


## Basic usage

For usage as a command-line tool, locate your installation of `cpraa` with `pip show cpraa`:

    $ pip show cpraa
    Name: cpraa
    Version: 0.6.1
    [...]
    Location: /path/to/installation

Change to the directory `/path/to/installation/cpraa` and run `python main.py --help` to display the built-in help message of CPrAA.
For the remainder of this readme we assume a shortcut `cpraa` is created which resolves to `python main.py` in this directory.

Basic usage usually requires at least three flags:
   * `--file` (or `-f`) followed by a `.tgf` file specifying the argumentation framework
   * `--semantics` (or `-s`) followed by the names of one or more semantics
   * the task to perform, e.g. `--one_distribution` to compute one distribution which satisfies the constraints of all specified semantics

**Example:**

    $ cpraa --file AFs/example.tgf --semantics MinCmp --one_distribution
    Computing one distribution satisfying the following semantics: MinCmp
    Support:
    P( A,-B, C) = 1

The result shows a distribution in _support format_, that is, only the assignments with non-zero probabilities are shown.
In this case, `P( A,-B, C) = 1` means that the assignment where `A` and `C` hold while `B` does not hold has a probability of one under this distribution.
To get the full distribution, the flag `--distribution_output_format` (or just `-o` for short) can be used with parameter `F`.
Likewise, the parameter `M` can be passed with the same flag to display the marginal probabilities of all arguments, and it is possible to pass multiple format options at once:

    $ cpraa --file AFs/example.tgf --semantics MinCmp --one_distribution --distribution_output_format FM
    Computing one distribution satisfying the following semantics: MinCmp
    P(-A,-B,-C) = 0
    P(-A,-B, C) = 0
    P(-A, B,-C) = 0
    P(-A, B, C) = 0
    P( A,-B,-C) = 0
    P( A,-B, C) = 1
    P( A, B,-C) = 0
    P( A, B, C) = 0
    P(A) = 1
    P(B) = 0
    P(C) = 1


## Input format

Argumentation frameworks (AFs) are provided in trivial graph format (`.tgf`) with some optional extensions.
A simple AF with three nodes (`A`, `B`, `C`) and three edges (`A -> B`, `B -> A`, `B -> C`) is specified as follows:

    A
    B
    C
    #
    A B
    B A
    B C

That is, we first have a declaration of nodes with one node ID per line, then a separator `#`, and finally the declaration of attacks, again with one attack per line.
Empty lines are ignored, and `;` introduces a line comment.

Nodes can optionally be annotated with a name. This can be handy to keep IDs short even if the name is long. 
Further, nodes can be annotated with a numeric value (e.g. `0.75` or `1`) or a value interval (e.g. `0.1:0.3`).
These values or intervals can be used by semantics to impose further constraints. 
Most prominently, the `AF` semantics enforces a node's marginal probability to equal the given value or fall within the specified interval if either is given.

The general format for a node declaration is

> `<node_id>` [ `<node_name>` ] [ `<node_value>` | `<node_value_min>` `:` `<node_value_max>` ] [ `;` `<comment>`]

where `<node_id>` is an alphanumeric string, `<node_name>` is alphanumeric but does not start with a digit, and `<node_value>`, `<node_value_min>`, and `<node_value_max>` are either integers or floats.

Edge declarations consist of two node IDs and can likewise be annotated with a name and a value or an interval:

> `<from_node_id>` `<to_node_id>` [ `<edge_name>` ] [ `<edge_value>` | `<edge_value_min>` `:` `<edge_value_max>` ] [ `;` `<comment>`]

The folder `AFs` contains a number of example argumentation frameworks in `.tgf` format.


## Semantics

The semantics that should be enforced for a task are specified with the `--semantics` (or `-s`) flag.
There is also the option to specify that certain semantics should _not_ hold with `--complement_semantics` (or `-cs`).

A list of all available semantics can be viewed with `--list_semantics` (or `-ls`):

    $ cpraa --list_semantics
    Available semantics: Min, Neu, Max, Dirac, Ter, Fou, SFou, Inv, Rat, Coh, Opt, SOpt, Jus, CF, WAdm, PrAdm, MinAdm, JntAdm, WCmp, PrCmp, MinCmp, JntCmp, ElmCF, ElmAdm, ElmCmp, ElmGrn, ElmPrf, ElmSStl, ElmStl, WNorS, NorS, SNorS, WNor, Nor, SNor, AF, NNorAF, NNor, CFs, StrengthCF, StrengthSupportCF, DiracCF, DiracAdm, DiracCmp, DiracGrn, DiracPrf, DiracSStl, DiracStl

Tip: With `--documentation` (or `-d`) followed by the names of one or more semantics a short description of most semantics is available:

    $ cpraa --documentation Fou MinAdm
    Semantics 'Fou':
        Foundedness semantics: Initial nodes must hold with probability 1.
    
    Semantics 'MinAdm':
        Min-admissibility semantics: CF and for every argument C, P(C) <= min_{B in Pre(C)} P(OR Pre(B)) holds.
        Equivalently, for all B in Pre(C) with Pre(B) = {A1, ..., An}, it holds P(C) <= 1 - P(nA1, ..., nAn).


## Tasks

Before taking a closer look at the tasks offered by CPrAA, it is worth noting that not all tasks are available for all semantics.
This is because, e.g., the optimization tasks are only feasible when facing _linear_ constraints.
However, for some semantics the imposed constraints are polynomial (rendering a formulation in terms of linear constraints impossible), or linear constraints are not yet implemented.
Notably, and perhaps most inconveniently, complement semantics are not available for tasks requiring linear constraints. 


### Check satisfiability 
`-OD`, `--one_distribution`

Basic task to check if the constraints imposed by all selected semantics are satisfiable.
If so, a satisfying distribution is returned as witness. 
Note that such a distribution in many cases is not the unique solution but only one representative from an infinite solution space. 

**Example:** Look for a distribution on the example AF that is min-complete (`MinCmp`) but not justifiable (`Jus`):

    $ cpraa -f AFs/example.tgf --semantics MinCmp --complement_semantics Jus --one_distribution
    Computing one distribution satisfying the following semantics: MinCmp, co-Jus
    Support:
    P(-A,-B, C) = 0.5
    P( A,-B,-C) = 0.5


### Enumerate vertices of convex solution space 
`-CD`, `--corner_distributions`

This task requires linear constraints, as otherwise it is not guaranteed that the solution space is convex.
The distributions (viewed as vectors in n-dimensional space) located at the corners of a convex solution space have the nice property that all solutions can be stated as a convex combination of them.
In case this task yields only a single distribution, the solution is unique.

**Example:** Find the corner distributions for element-wise completeness (`ElmCmp`) in the example AF:

    $ cpraa -f AFs/example.tgf --semantics ElmCmp --corner_distributions
    Computing the corner distributions for the following semantics: ElmCmp
    
    Result 1 of 3:
    Support:
    P(-A,-B,-C) = 1
    
    Result 2 of 3:
    Support:
    P(-A, B,-C) = 1
    
    Result 3 of 3:
    Support:
    P( A,-B, C) = 1

As expected, the resulting distributions are the Dirac distributions of the assignments corresponding to all three complete assignments of the example AF. 


### Optimize marginal probabilities

`-MIN`, `--minimize_probability`, or `-MAX`, `--maximize_probability`

This task requires linear constraints and one or more arguments from the AF (passed with `--arguments` or `-a`).
If the constraints are satisfiable, the resulting distribution minimises (or respectively maximises) the marginal probability of the given argument, or, if multiple arguments are given, the probability of any argument holding.

**Example:** Find a probabilistically complete distribution under which argument `B`'s marginal probability is maximal: 

    $ cpraa -f AFs/example.tgf --semantics PrCmp -a B -MAX
    Computing optimal distribution maximizing the probability of argument B while satisfying the following semantics: PrCmp
    Support:
    P(-A, B,-C) = 1


### Acceptance checking for arguments

An argument `A` is _credulously accepted_ under some given constraints if at least one satisfying distribution exists with `P(A) = 1`, and _skeptically accepted_ if `P(A) = 1` holds for all distributions `P` that satisfy the constraints.

One or more arguments from the AF need to be specified following the `--arguments` (`-a`) flag to be checked with `--credulous_acceptance` (`-CA`) or `--skeptical_acceptance` (`-SA`).
As a shortcut, there is also `--credulous_acceptance_all` (`-CAA`) and `--skeptical_acceptance_all` (`-SAA`) to check credulous or skeptical acceptance for all arguments in the AF.

Acceptance checking is also possible with respect to a given threshold value, e.g., `t = 0.75`: 
Then `A` is credulously accepted w.r.t. `t` if `P(A) >= 0.75` holds for at least one distribution, and likewise skeptically accepted w.r.t `t` if `P(A) >= 0.75` holds for all distributions.
Such a threshold can be specified directly following the flag for the respective acceptance checking task, e.g., `--credulous_acceptance 0.75`.  

**Example:** Check if argument `C` is skeptically accepted with a threshold of `0.5` under joint-complete semantics: 

    $ cpraa -f AFs/example.tgf --semantics JntCmp --argument C --skeptical_acceptance 0.5
    Checking skeptical acceptance of argument C with threshold 0.5 under the following semantics: JntCmp
    C is not skeptically accepted.
    Counterexample:
    Support:
    P(-A,-B,-C) = 1

The output tells us that `C` is not skeptically accepted under the given constraints and additionally provides a distribution which is a counterexample, in this case a joint-complete distribution with `P(C) = 0`.


### Generate labelings

For tasks involving labelings, a labeling scheme needs to be specified.
A list of all available labeling schemes is printed with the `--list_labeling_schemes` (or `-ll`) flag.
Note that the `--documentation` (or `-d`) flag also works with labeling schemes and displays a short description:

    $ cpraa --list_labeling_schemes
    Available labeling schemes: Cautious, Threshold, Firm, ClassicalOld, ThresholdClassicalOld, Classical, ThresholdClassical, Optimistic, Pessimistic
    $ cpraa --documentation Cautious
    Labeling scheme 'Cautious':
        Arguments with probability 1 are labeled 'in', those with probability 0 are labeled 'out' and all others are
    labeled 'undec'.

Some labeling schemes require one or more thresholds which can be specified following the `--labeling_threshold` (or `-lt`) flag.
Given all that, either one labeling or all labelings can be computed with `--one_labeling` (`-OL`) and `--all_labelings` (`-AL`).

**Example:** Compute all min-complete labelings under the `Firm` labeling scheme: 

    $ cpraa -f AFs/example.tgf --semantics MinCmp --labeling_scheme firm --all_labelings
    Computing all firm labelings satisfying the following semantics: MinCmp
    Number of labelings: 6
    {}{}{A,B,C}
    {}{A,B,C}{}
    {}{A,C}{B}
    {}{B}{A,C}
    {A,C}{B}{}
    {B}{A,C}{}

Labelings are printed in set notation in the order `{in}{out}{undec}`.
That is, the labeling `{B}{A,C}{}` means argument `B` is labeled _in_, `A` and `C` are both _out_, and no argument is labeled as _undecided_.

## Further options

### Additional constraints as SMT file 

`-smt`, `--smt_file`

In the input format section, we saw that additional constraints on the marginal probabilities of arguments can be specified directly in the input file. 
More involved constraints can be added via an extra file in [SMT-LIB](https://smtlib.cs.uiowa.edu/) format.
Note that this functionality is currently only available for tasks that do not require linear constraints.

**Example:** The file `example.smt` contains the following additional constraints for the AF `example.tgf`:

    ; P(A) = 2 ∗ P(C)
    (declare-fun p_A () Real)
    (declare-fun p_C () Real)
    (assert (= p_A (* 2 p_C)))

    ; P(A ∨ C | -B) ≥ 0.8
    ; P((A ∨ C) ∧ -B) ≥ 0.8 ∗ P(-B)
    ; P(A ∧ -B) + P(C ∧ -B) - P(A ∧ C ∧ -B) ≥ 0.8 ∗ P(-B)
    (declare-fun p_A_nB () Real)
    (declare-fun p_nB_C () Real)
    (declare-fun p_A_nB_C () Real)
    (declare-fun p_nB () Real)
    (assert (>= (- (+ p_A_nB p_nB_C) p_A_nB_C) (* 0.8 p_nB)))

To express the constraint `P(A) = 2 ∗ P(C)`, i.e., that `A` is twice as likely as `C`, we need two variables `p_A` and `p_C` which refer to the marginal probabilities of `A` and `C`.
The constraint is then given in assert statement using prefix notation: `(assert (= p_A (* 2 p_C)))`.

For the constraint `P(A ∨ C | -B) ≥ 0.8`, i.e., the conditional probability of `A` or `C` holding given that `B` does not hold is at least `0.8`, we need to rewrite the constraint such that only statements about the probability of conjunctions remain: `P(A ∧ -B) + P(C ∧ -B) - P(A ∧ C ∧ -B) ≥ 0.8 ∗ P(-B)`.
Thus, variables need to be introduced for `P(A ∧ -B)`, `P(C ∧ -B)`, `P(A ∧ C ∧ -B)` and `P(-B)`: `p_A_nB`, `p_nB_C`, `p_A_nB_C` and `p_nB`.
Note how negation is represented by a leading `n` and that the argument names `A`, `B` and `C` always appear in lexicographic order. 
This is required for correct parsing of the constraints. 

Looking for one joint-complete distribution which satisfies the above constraints yields the following: 

    $ cpraa --file AFs/example.tgf --smt_file AFs/example.smt --semantics JntCmp --one_distribution
    SMT constraint:  ((p_A = (2.0 * p_C)) & ((4/5 * p_nB) <= ((p_A_nB + p_nB_C) - p_A_nB_C)))
    Computing one distribution satisfying the following semantics: JntCmp
    Support:
    P(-A, B,-C) = 1


### Specify which solver to use

`-b`, `--backend_solver`

By default, CPrAA automatically picks a fitting solver to use as backend for each task.
With this flag, usage of a specific solver can be enforced.
Options are all SMT solvers available via [pySMT](https://github.com/pysmt/pysmt) (`z3`, `msat`, `cvc4`, `yices`, `btor`, `picosat`, `bdd`), linear solvers via [CVXOPT](https://github.com/cvxopt/cvxopt) (`cvxopt`, `glpk`, `mosek`), and a direct integration of Z3 (`z3-legacy`).
While Z3 and CVXOPT are dependencies of CPrAA and thus always available, most of the other solvers need to be installed separately. 
More information on how to install the listed SMT solvers is given in the [documentation](https://pysmt.readthedocs.io/en/latest/getting_started.html) of pySMT.


### Time the execution

`-t`, `--time`

With this flag, some timings are printed, including the overall runtime and how long it took to generate all constraints.
Note that some given timings may include other timings (e.g., the timing for the task may include the timing for the constraint generation), so the sum of given partial timings can exceed the overall runtime.

    $ cpraa --file AFs/example.tgf  --semantics MinCmp --one_distribution --time
    Computing one distribution satisfying the following semantics: MinCmp
    solver instance setup took 0.002 seconds
    Generating constraints for all semantics took 0.002 seconds
    Support:
    P( A,-B, C) = 1
    Computing one distribution took 0.020 seconds
    Overall runtime: 0.025 seconds


<!--
### Output format options for distributions

`-o`, `--distribution_output_format`

`-p`, `--output_precision`
-->

### Display the constraints of the semantics  

`-dc`, `--display_constraints`

With this flag, the constraints generated for the give AF under the given semantics are displayed.
Very long constraints are truncated.
Note that for complemented semantics, the constraints are displayed without the subsequent conjunction and negation.

If a semantics generates one constraint for each attack or each argument in the AF, then the attack's or argument's name is given before the constraint. 

**Example:**

    $ cpraa --file AFs/example.tgf --semantics MinCmp --one_distribution --display_constraints
    Computing one distribution satisfying the following semantics: MinCmp
    CF: A->B: (p_A_B = 0.0)
    CF: B->C: (p_B_C = 0.0)
    CF: B->A: (p_A_B = 0.0)
    MinAdm: A: (p_A <= (1.0 - p_nA))
    MinAdm: B: (p_B <= (1.0 - p_nB))
    MinAdm: C: (p_C <= (1.0 - p_nA))
    MinCmp: A: ((p_A_nB_nC + p_A_B_nC + p_A_nB_C + p_A_B_C) <= p_A)
    MinCmp: B: ((p_nA_B_nC + p_nA_B_C + p_A_B_nC + p_A_B_C) <= p_B)
    MinCmp: C: ((p_A_nB_nC + p_A_B_nC + p_A_nB_C + p_A_B_C) <= p_C)
    Support:
    P( A,-B, C) = 1

Min-completeness requires min-admissibility, which in turn enforces conflict-freeness.
Thus, we first see the constraints generated by CF for each attack, followed by the MinAdm constraints and MinCmp constraints for each argument.