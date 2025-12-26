Task 4:
Write a RISC-V assembly program that converts a C code into an Assembly code by using an IF and IF-
ELSE statements. Perform the following tasks:
C Code IF Statement:
if (apples = = oranges) // C code check i==j
f = g + h;
apples = oranges − h;
Convert the above C code into Assembly code:
• Compare the values of apples (s0) and oranges (s1) using bne.
• If they are not equal, skip the next instruction and jump to L1.
• If they are equal, execute f = g + h by adding s3 (g) and s4 (h) and storing the result in s2 (f).
• At label L1, execute apples = oranges - h by subtracting s4 (h) from s1 (oranges) and storing the
result in s0 (apples).
C Code IF-ELSE Statement:
if (apples = = oranges)
f = g + h;
else
apples = oranges − h;
Convert the above C code into Assembly code:
• Compare s0 (apples) and s1 (oranges) using bne.
• if they are not equal, jump to L1 (ELSE block).
• If they are equal, execute f = g + h.
• Use the j instruction to skip the ELSE block and jump to L2.
• At label L1, execute apples = oranges - h (ELSE block).
• Label L2 marks the end of the IF-ELSE structure.


C Code
if (apples == oranges) {
    f = g + h;
}
apples = oranges - h;


    .text
    .globl main

main:
    # Initialize values
    li s0, 10       # apples
    li s1, 10       # oranges
    li s3, 5        # g
    li s4, 3        # h

    # IF statement: if (apples == oranges)
    bne s0, s1, L1      # If s0 != s1, skip f = g + h
    add s2, s3, s4      # f = g + h

L1:
    sub s0, s1, s4      # apples = oranges - h

    nop

IF-ELSE Statement
C Code

if (apples == oranges) {
    f = g + h;
} else {
    apples = oranges - h;
}

    # Initialize values
    li s0, 10       # apples
    li s1, 10       # oranges
    li s3, 5        # g
    li s4, 3        # h

    # IF-ELSE: if (apples == oranges)
    bne s0, s1, L1      # If s0 != s1, jump to ELSE block
    add s2, s3, s4      # f = g + h
    j L2                # Skip ELSE block

L1:                     # ELSE block
    sub s0, s1, s4      # apples = oranges - h

L2:                     # End of IF-ELSE
    nop
