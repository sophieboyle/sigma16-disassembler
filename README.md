# Sigma16 Disassembler

- A Sigma16 disassembler which converts object code to sigma16 assembly language
- Currently supported instructions
  - RRR
  - RX
  - EXP
- Note that arrays will be formatted with each element given an arbritrary variable name
  - This is because there is no information about variable name declarations in the object file to recover
  - This will not affect the actual operation of the code itself

## Note on Sigma16

- [Sigma16](https://github.com/jtod/Sigma16) is an architecture created by [John T O'Donnell](https://github.com/jtod), former lecturer at the University of Glasgow.

## TODO

- Support labels
