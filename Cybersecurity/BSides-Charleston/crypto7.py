#!/usr/bin/env python

# ***********************
# Charleson BSides 2017
# Cryptography Challenge
# ***********************

import sys

# TODO: optional argument for reverse (ASCII to ciphertext)

# if len sys.argv == 1:

ctext = input("Enter the ciphertext (space-separated bytes): ")
if len(ctext) == 0:
    # use default ciphertext
    print("Using default ciphertext.")
    ctext = "45 86 96 37 02 e6 56 87 47 02 d6 56 37 37 16 76 56 02 96 37 02 26 27 f6 57 76 86 47 02 47 f6 02 97 f6 57 02 26 97 02 16 e6 e6 f6 97 96 e6 76 02 26 96 47 02 d6 16 e6 96 07 57 c6 16 47 96 f6 e6 e2 02 45 86 56 02 e6 56 87 47 02 66 c6 16 76 02 96 37 02 34 27 f6 37 37 77 f6 27 46 e2"

arr = ctext.split()

print("The ciphertext:\n" + ctext + "\n")

flipped = []

for num in arr:
    try:
        flipped.append(num[1]+num[0])
    except:
        print("There is a formatting error. Be sure that your string consists only of space-separated bytes. Exiting...")
        exit(0)

flippedText = ""
for num in flipped:
    flippedText += num + " "
print("After flipping the nibbles:\n" + flippedText + "\n")

decoded = ""

for num in flipped:
    try:
        decoded += bytearray.fromhex(num).decode()
    except:
        print("There is a problem converting to ASCII. Be sure that your string contains only valid hexadecimal characters. Exiting...")
        exit(0)

print("Corresponding ASCII text:\n" + decoded + "\n")
