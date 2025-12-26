Task 2: Develop a RISC-V assembly program to demonstrate the use of
arithmetic instructions in the Venus IDE. The program should accomplish
the following objectives:

```asm
# Task 2: Demonstration of Arithmetic Instructions
# Works in Venus IDE (RV32IM)

    .text
    .globl main

main:
    # ------------------------------------------------
    # Load predetermined values into registers
    # ------------------------------------------------
    li t0, 20        # t0 = 20
    li t1, 10        # t1 = 10
    li t2, 5         # t2 = 5
    li t3, 2         # t3 = 2

    # ------------------------------------------------
    # Addition and Subtraction
    # ------------------------------------------------
    add t4, t0, t1   # t4 = t0 + t1 = 20 + 10 = 30
    sub t5, t0, t1   # t5 = t0 - t1 = 20 - 10 = 10

    # ------------------------------------------------
    # Multiplication and Division
    # ------------------------------------------------
    mul t6, t2, t3   # t6 = t2 * t3 = 5 * 2 = 10
    div t7, t0, t3   # t7 = t0 / t3 = 20 / 2 = 10

    # End program
    nop
```

