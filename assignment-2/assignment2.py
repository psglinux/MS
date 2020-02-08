#!/usr/bin/env python

def find_prime_factor(n):
    for i in xrange(1,n+1,1):
        d = n/i
        r = n%i
        if r == 0:
            print "i = ", i, n,"/i = ", n/i," ", n,"%i = ", n%i

def find_one_e_or_d(tot, e):
    i = 1
    while 1:
       p = (i*e)%tot
       if p == 1:
           print "e*d =", i*e, "e = ", e, " d = ", i
           break
       i += 1

def find_C(M, e, N, m):
    C = pow(M, e)%N
    print m, ":", C
    return C

def find_d_for_e(e, r, tot):
    print "e = ", e
    print "------------------------------------"
    for i in xrange(e,1000,1):
	 if (e*i%40 == 1 and i%e != 0):
	     print "e =", e, " d =", i

def problem_1():
    print "problem 1 : ------- starts"
    find_prime_factor(187)
    find_one_e_or_d(160, 107)
    find_C(8, 107, 187, "Cipher")
    print "problem 1 : ------- ends"

def problem_2():
    print "problem 2 : ------- starts"
    find_d_for_e(3, 1000, 40)
    find_d_for_e(5, 1000, 40)
    find_d_for_e(7, 1000, 40)
    c = find_C(8, 3, 55, "Cipher")
    find_C(c, 67, 55, "Plain")
    print "problem 2 : ------- ends"

problem_1()
problem_2()

