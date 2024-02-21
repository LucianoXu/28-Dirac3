
## Unicode Characters
× · † ⊗

## Note
- the terms are compared first by hash values
- The syntax of Dirac notation already incorperate the equivalence of AC symbols. Expressions with AC leading symbols will be flattened and stored as a list when constructed.
- The syntax for the parser is very close to that of a term rewriting system. The only modification is that we allow the chain of infix binary such as ```a ADDS b ADDS c```, which is supported by the preference setting of **ply**.
- In the trs, every term is considered as immutable.

- We write special functions for each rule involving AC symbols, and many obvious optimizations are considered.