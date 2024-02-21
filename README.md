
## Unicode Characters
× · † ⊗

## Note
- the terms are compared first by hash values
- The syntax of Dirac notation already incorperate the equivalence of AC symbols. Expressions with AC leading symbols will be flattened and stored as a list when constructed.
- The syntax for the parser is very close to that of a term rewriting system. The only modification is that we allow the chain of infix binary such as ```a ADDS b ADDS c```, which is supported by the preference setting of **ply**.
- In the trs, every term is considered as immutable.

- We write special functions for each rule involving AC symbols, and many obvious optimizations are considered.

- About extra rules for Delta: 
    - now we analysis every individual delta-operator only
    - the implementation with Wolfram Base backend relies on `FindInstance` method and requies the hint of variables, which is provided through `side_info` arguments in the trs.

- We can output the corresponding CiME2 code for the trs and check the confluence of the trs indirectly.

- We already encountered efficiency problems in a simple example:
    ```
            a = sub(parse(''' (I2 TSRO H) MLTO CZ MLTO (I2 TSRO H)'''))
            b = sub(parse(''' CX '''))
            assert trs.normalize(a) == trs.normalize(b)
    ```
    It takes about 5 seconds.

- About parameters: there are something not that natural about Rz(beta) Ry(gamma) Rz(delta). We need to incorporate abstractions to represent functions

## TODO
- consider the case of teleportation after we have indices