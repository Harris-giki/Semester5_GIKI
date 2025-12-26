Task 3: Develop a RISC-V assembly program in the Venus IDE that
combines arithmetic and data transfer instructions to perform a simple
computational task. The program should achieve the following objectives:

```asm
    .data
num1:   .word 15        # First integer in memory
num2:   .word 5         # Second integer in memory
result: .word 0         # Memory location to store result

    .text
    .globl main

main:
    # -----------------------------------------
    # Load two integers from memory
    # -----------------------------------------
    lw t0, num1         # t0 = 15
    lw t1, num2         # t1 = 5

    # -----------------------------------------
    # Perform arithmetic operation
    # (change add to sub, mul, or div if needed)
    # -----------------------------------------
    add t2, t0, t1      # t2 = t0 + t1 = 20

    # -----------------------------------------
    # Store result back into memory
    # -----------------------------------------
    sw t2, result       # result = 20

    nop
```
