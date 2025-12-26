Task 1: Write a RISC-V assembly program that performs the following operations: • Load the immediate value 4 into register t0. • Perform a logical left shift on t0 by 1 bit and store the result in t2. • Perform a logical right shift on t0 by 1 bit and store the result in t3. • Perform an arithmetic right shift on t0 by 1 bit and store the result in t4.

    .text
    .globl main

main:
    # Load immediate value 4
    li t0, 4            # t0 = 4 (0000 0100)

    # Logical left shift by 1
    slli t2, t0, 1      # t2 = t0 << 1 = 8

    # Logical right shift by 1
    srli t3, t0, 1      # t3 = t0 >> 1 (logical) = 2

    # Arithmetic right shift by 1
    srai t4, t0, 1      # t4 = t0 >> 1 (arithmetic) = 2

    nop
