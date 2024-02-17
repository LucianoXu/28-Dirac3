
## Unicode Characters
× · † ⊗

## Note
- Because of the **randomized hashing**, the same expression will have different hash values across different sessions.
- The syntax of Dirac notation already incorperate the equivalence of AC symbols. Expressions with AC leading symbols will be flattened and stored as a list when constructed.
- The syntax for the parser is very close to that of a term rewriting system. The only modification is that we allow the chain of infix binary such as ```a ADDS b ADDS c```, which is supported by the preference setting of **ply**.