# DiracDec Implementation

## Installation

- Install Wolfram Engine from https://www.wolfram.com/engine/.
Activate the engine as instructed. Note that Python communicates with Wolfram engine through socket connections, which is influenced by network settings. Inappropriate settings (for example, global VPN) may lead to connection failure.

- Install the dependencies by executing
  ```
  pip install requirements.txt
  ```

The implementation is tested with Python 3.11.

## Manifest
- `.\diracdec`: the implementation source
- `.\tests`: the unit tests for the implementation, including the examples
- `.\demo.ipynb`: a notebook with some demonstrations
- `.\app.py`: a web application for diracdec written in Flask

## Usage
- Web UI: execute
```
python app.py
```
in the root folder and connect to the server.

- In Python: see `.\demo.ipynb` and examples in `.\tests`


## Language
The parser expects languages of $sub$ or $term$.

The keywords are the symbols in captial letters in the following definition. A variable is a string matching the regex `[a-zA-Z\_][a-zA-Z0-9\_]*` .

- sub ::= { subls }
- subls ::= $\epsilon$ | subls var : term ;
- term ::= base | scal | dirac
- base ::= var | '\<WOLFRAM\>' | PAIR(base, base) | FST(base) | SND(base)
- scal ::= var | "\<WOLFRAM\>" | DELTA(base, base) | scal ADDS scal | scal MLTS scal | CONJS(scal) | dirac DOT dirac
- dirac ::= var | 0X | ADJ(dirac) | scal SCR dirac | dirac ADD dirac 
  - | KET(base) | dirac MLTK dirac | dirac TSRK dirac 
  - | BRA(base) | dirac MLTB dirac | dirac TSRB dirac  
  - | 1O | dirac OUTER dirac | dirac MLTO dirac | dirac TSRO dirac


## Note
- The syntax of Dirac notation already incorperate the equivalence of AC symbols. Expressions with AC leading symbols will be flattened and stored as a list when constructed.
- The syntax for the parser is very close to that of a term rewriting system. The only modification is that we allow the chain of infix binary such as ```a ADDS b ADDS c```, which is supported by the preference setting of **ply**.
- In the trs, every term is considered as immutable.

- We write special functions for each rule involving AC symbols, and many obvious optimizations are considered.

- About extra rules for Delta: 
    - now we analysis every individual delta-operator only
    - the implementation with Wolfram Base backend relies on `FindInstance` method and requies the hint of variables, which is automatically calculated.

- We can output the corresponding CiME2 code for the trs and check the confluence of the trs indirectly.

- We already encountered efficiency problems in a simple example:
    ```
            a = sub(parse(''' (I2 TSRO H) MLTO CZ MLTO (I2 TSRO H)'''))
            b = sub(parse(''' CX '''))
            assert trs.normalize(a) == trs.normalize(b)
    ```
    It takes about 5 seconds.

- Now the variables of dirac notation and wolfram language are unified. Meaning, we can substitute the symbols in wolfram language now. And since we will always operate wolfram expression in the Global context, we delete the "Global`" prefix when calculating the variables. Also, it allowed to substitute the symbols in wolfram language by TRSVar  instances directly.

- Use `HoldForm` in the Wolfram Language to keep the input expression unchanged. The trs have rules to release the hold during reduction.

- We have implemented the abstract/application and beta reduction, but it is very slow currently.

- I already encountered problem in using Wolfram Engine: equivalent expresssions reduced by `FullSimply` can have different syntax. I may need a complex scalar table to deal with this problem. (That is, we provide the choice to use a more powerful method to compare the equivalence of terms.)
This is implemented in the backend "wolfram_unique". We transform terms in simple backend to wolfram_unique backend when comparing.


- I implemented `sum_i sum_j <i|A|j> |i><j| -> A`, but the matching is far from complete. Now I believe the rule for sum is not well designed - in the opposite direction actually. We should try to pull things out of the sum instead of pushing them in.

- Now we use `MultiBindTerm` to characterize successive big-op.

- I want to add index sets to the summation, but the problem is that it can be hard to decide whether the term belongs to the set when applying SUM-ELIM rules involving delta. So now we have universal set for this purpose.

- Quantum register & register sets implemented, reducton rules implemented. The problem is the checking of register in/disjoint properties is a little bit complicated.

## TODO
- consider the case of teleportation after we have indices
- reconsider how to deal with equivalence
- consider parsing latex input

- summation with index set
- C(0) -> \mathbf{0} (necessary for summation with index set)