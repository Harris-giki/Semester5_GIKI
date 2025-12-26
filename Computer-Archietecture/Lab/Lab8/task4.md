Task 4: Write a RISC-V assembly program in the Venus IDE that performs bitwise
logical operations (AND, OR, XOR, and NOT) to manipulate the bits of registers. You
will perform a series of operations on two registers (t0 and t1) and observe how each
operation affects the binary values in those registers.
• Load Values into Registers (t0, t1)
• Perform Bitwise AND Operation (and, andi).
• Perform Bitwise OR Operation (or, ori).
• Perform Bitwise XOR Operation (xor, xori)
• Perform Bitwise NOT Operation (~not)


```asm
    .text
    .globl main

main:
    # -----------------------------------------
    # Load values into registers
    # -----------------------------------------
    li t0, 0x0F        # t0 = 0000 1111
    li t1, 0x33        # t1 = 0011 0011

    # -----------------------------------------
    # Bitwise AND
    # -----------------------------------------
    and  t2, t0, t1    # t2 = t0 & t1
    andi t3, t0, 0x0A  # t3 = t0 & 0000 1010

    # -----------------------------------------
    # Bitwise OR
    # -----------------------------------------
    or   t4, t0, t1    # t4 = t0 | t1
    ori  t5, t0, 0x0A  # t5 = t0 | 0000 1010

    # -----------------------------------------
    # Bitwise XOR
    # -----------------------------------------
    xor  t6, t0, t1    # t6 = t0 ^ t1
    xori t7, t0, 0x0A  # t7 = t0 ^ 0000 1010

    # -----------------------------------------
    # Bitwise NOT
    # -----------------------------------------
    not  t0, t0        # t0 = ~t0

    nop
```

