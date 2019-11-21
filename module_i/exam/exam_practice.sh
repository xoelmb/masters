#!/bin/bash

# 5.a
#cat alice.txt | head -n 500 | tail -n 1

# 5.b
#cat alice.txt | tr ' ' '\n' | grep -E "th[aeiou]" | uniq -c
#cat alice.txt | tr ' ' '\n' | grep -c tha

# 5.c
split -l 200 alice.txt