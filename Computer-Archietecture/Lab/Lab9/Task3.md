Task 3:
Write a RISC-V assembly program to demonstrate unconditional branching using the j (jump)
instruction. Perform the following tasks:
• Use the j instruction to unconditionally jump to the label target.
• Ensure that all instructions between the j instruction and the target label are skipped (not
executed).
• At the target label, perform an addition operation:
• Add the value in register s0 to s1 and store the result in s1.

    .text
    .globl main

main:
    # Load initial values
    li s0, 10           # s0 = 10
    li s1, 5            # s1 = 5

    # Unconditional jump to target
    j target            # Jump to target, skip next instructions

    # Instructions skipped
    li t0, 0            # Skipped
    li t1, 0            # Skipped

target:
    # Perform addition at the target label
    add s1, s0, s1      # s1 = s0 + s1 = 10 + 5 = 15

    nop
