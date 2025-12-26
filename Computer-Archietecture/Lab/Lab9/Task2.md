Task 2:
Write a RISC-V assembly program to demonstrate conditional branching using beq, bne, instructions.
Perform the following tasks:
Conditional Branching using beq (Branch if Equal):
• Load two immediate values into registers s0 and s1.
• Perform a logical left shift on s1 by 2 bits.
• Compare s0 and s1 using beq. If they are equal, branch to the label target.
• If the branch is taken, skip the next two instructions.
• At the target label, add s0 to s1 and store the result in s1.
Conditional Branching using bne (Branch if Not Equal):
• Repeat the same steps as in beq but use bne instead.
• If s0 and s1 are not equal, jump to the target label.
• Verify that, in this case, the branch is not taken because s0 == s1.


    .text
    .globl main

main:
    # ----------------------------
    # Conditional Branching using beq
    # ----------------------------
    li s0, 16           # Load immediate 16 into s0
    li s1, 4            # Load immediate 4 into s1

    slli s1, s1, 2      # Logical left shift s1 by 2 → s1 = 16

    beq s0, s1, target_beq  # If s0 == s1, branch to target_beq

    # Instructions skipped if branch taken
    li t0, 0             # Dummy instruction 1
    li t1, 0             # Dummy instruction 2

target_beq:
    add s1, s0, s1      # s1 = s0 + s1 = 16 + 16 = 32

    # ----------------------------
    # Conditional Branching using bne
    # ----------------------------
    li s0, 16           # Reset s0 = 16
    li s1, 16           # Reset s1 = 16

    slli s1, s1, 0      # Shift by 0 bits, s1 still 16

    bne s0, s1, target_bne  # If s0 != s1, branch to target_bne

    # Instructions executed because branch NOT taken
    li t2, 1            # Dummy instruction 1
    li t3, 2            # Dummy instruction 2

target_bne:
    add s1, s0, s1      # s1 = s0 + s1 = 16 + 16 = 32

    nop
