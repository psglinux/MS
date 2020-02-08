#!/usr/bin/env python

def find_prime_fatcor(n):
    for i in xrange(1,n+1,1):
        d = n/i
        r = n%i
        if r == 0:
            print "i = ", i, "187/i = ", 187/i," 187%i = ", 187%i

def find_one_e_or_d(tot, e):
    i = 1
    while 1:
       p = (i*e)%tot 
       if p == 1:
           print "e*d =", i*e, "e = ", e, " d = ", i
           break
       i += 1

def find_C(M, e, N):
    C = pow(M, e)%N
    print "Cipher :", C

def problem_1():
    find_prime_fatcor(187)
    find_one_e_or_d(160, 107)
    find_C(8, 107, 187)

problem_1()

