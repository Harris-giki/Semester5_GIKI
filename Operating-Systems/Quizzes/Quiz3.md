| Instruction                 | Privileged / Unprivileged              |
| --------------------------- | -------------------------------------- |
| Load from process own stack | Unprivileged                           |
| Write on process own heap   | Unprivileged                           |
| Execute trap instruction    | Unprivileged (causes privilege switch) |
| Write on trap table         | Privileged                             |
| Read from trap table        | Privileged                             |
