Task 5:
Write a RISC-V assembly program to implement a while loop that calculates the power of 2 such that
2^x = 128.
While loop : High-Level Code
// determines the power
// of x such that 2^x = 128
int pow = 1;
int x = 0;
do {
pow = pow * 2;
x = x + 1;
} while (pow!= 128);

Convert the above C code into Assembly code:
Follow these steps:
• Set pow = 1 in s0.
• Set x = 0 in s1.
• Store the constant 128 in t0 (used for comparison).

1. Loop Execution:
• Multiply pow by 2 using a left shift operation (slli).
• Increment x by 1 using addi.
• Use the bne instruction to check if pow != 128.
• If pow is not equal to 128, repeat the loop.
• If pow equals 128, exit the loop and proceed to the done label.

    .text
    .globl main

main:
    # ----------------------------
    # Initialize variables
    # ----------------------------
    li s0, 1          # pow = 1
    li s1, 0          # x = 0
    li t0, 128        # constant 128 for comparison

loop:
    # Multiply pow by 2 using left shift
    slli s0, s0, 1    # pow = pow << 1

    # Increment x by 1
    addi s1, s1, 1    # x = x + 1

    # Compare pow with 128
    bne s0, t0, loop  # If pow != 128, repeat loop

done:
    nop                # Loop exit point
