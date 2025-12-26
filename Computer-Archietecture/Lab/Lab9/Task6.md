Task 6:
Write a RISC-V assembly program to implement a for loop that adds numbers from 0 to 9 and stores
the sum in a register. Follow these steps:
For loop : High-Level Code:
// add the numbers from 0 to 9
int sum = 0;
int i;
for (i = 0; i < 10; i = i + 1) {
sum = sum + i; }
Convert the above C code into Assembly code:
Follow these steps:
Initialize Variables:
• Set sum = 0 in s1.
• Set i = 0 in s0.
• Store the constant 10 in t0 (loop condition).
Loop Execution:
• Check if i >= 10 using bge. If true, exit the loop and jump to done.
• If false, execute sum = sum + i.
• Increment i by 1.
• Jump back to the beginning of the loop to check the condition again.
Loop Termination:
• When I reach 10, the loop exits and proceed to done.


    .text
    .globl main

main:
    # ----------------------------
    # Initialize variables
    # ----------------------------
    li s1, 0          # sum = 0
    li s0, 0          # i = 0
    li t0, 10         # loop limit = 10

loop:
    # Check if i >= 10
    bge s0, t0, done  # exit loop if i >= 10

    # sum = sum + i
    add s1, s1, s0

    # i = i + 1
    addi s0, s0, 1

    # Jump back to beginning of loop
    j loop

done:
    nop

