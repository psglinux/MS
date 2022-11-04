#!/usr/bin/env python
from collections import OrderedDict
from itertools import permutations

en = "PBFPVYFBQXZTYFPBFEQJHDXXQVAPTPQJKTOYQWIPBVWLXTOXBTFXQWAXBVCXQWAXFQJVWLEQNTOZQGGQLFXQWAKVWLXQWAEBIPBFXFQVXGTVJVWLBTPQWAEBFPBFHCVLXBQUFEVWLXGDPEQVPQGVPPBFTIXPFHXZHVFAGFOTHFEFBQUFTDHZBQPOTHXTYFTODXQHFTDPTOGHFQPBQWAQJJTODXQHFOQPWTBDHHIXQVAPBFZQHCFWPFHPBFIPBQWKFABVYYDZBOTHPBQPQJTQOTOGHFQAPBFEQJHDXXQVAVXEBQPEFZBVFOJIWFFACFCCFHQWAUVWFLQHGFXVAFXQHFUFHILTTAVWAFFAWTEVOITDHFHFQAITIXPFHXAFQHEFZQWGFLVWPTOFFA"
prob_key = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

prob_key_ar = list(prob_key)
en_ar = list(en)
print "encrypted array :", en_ar

#create the stat based dict for the given key
def create_encrypt_text_dict_stat(e):
    stat_en = {}
    for i in e:
        if i in stat_en:
            stat_en[i] += 1
        else:
            stat_en[i] = 1
    print "statistical encrypted dict: ",  stat_en

    for e in alphabet:
        if not stat_en.has_key(e):
            stat_en[e] = 0
    print "statistical encrypted complete dict: ",  stat_en
    return stat_en

stat_en_dict = create_encrypt_text_dict_stat(en_ar)
#sorted_en_dict = {k: v for k, v in sorted(stat_en.items(), key=lambda item: item[1])}
#print "sorted dict :", sorted_en_dict
sorted_stat_en_arr = sorted(stat_en_dict, key=stat_en_dict.get, reverse=True)
sorted_dict_en = OrderedDict(sorted(stat_en_dict.items(), key=lambda t: t[1], reverse=True))

print "sorted encrypted dict   :", sorted_dict_en
#print "sorted encrypted array   :", sorted_stat_en_arr
#print "commonly used eng letter :", prob_key_ar
print len(sorted_stat_en_arr)

# statistically sorted elements in cipher text
# k - common probability of usage of english char
# since the most frequent.y used first 12 letter makes 80% of the words try
# using only the forst 12 letters based on frequency
def create_encrypt_to_mapped_dict(k, m):
    d = {}
    j = 0;
    for i in m:
        d[i] = k[j]
        #if (j < 11 or j > 18):
        #if (j < 12):
        #    d[i] = k[j]
        #else:
        #    d[i] = 'x'
        j += 1
    return d

def stat_based_decrypt(d_key, e_lst):
    d = []
    for i in e_lst:
        d.append(d_key[i])
    return d


### base code for decryption
print "---- iteration 1-----"
mapped_key = create_encrypt_to_mapped_dict(prob_key_ar, sorted_stat_en_arr)
print "sorted encrypted array   :", sorted_stat_en_arr
print "commonly used eng letter :", prob_key_ar
print "mapped key :", mapped_key

decrypted_arr = stat_based_decrypt(mapped_key, en_ar)
print "encrypted : ", en
print "decrypted : ", ''.join(decrypted_arr)

## permutate the first 6 item and try to find the elements
def permutate_keys(p_key, enc_ar):
    p = permutations(p_key[0:8], 8)
    for i in p:
        n_p_key = "".join(i)+p_key[8:]
        n_p_key_ar = list(n_p_key)
        n_mapped_key = create_encrypt_to_mapped_dict(n_p_key_ar, sorted_stat_en_arr)
        print "sorted encrypted array   :", sorted_stat_en_arr
        print "commonly used eng letter :", n_p_key
        print "mapped key :", mapped_key
        decrypted_arr = stat_based_decrypt(n_mapped_key, enc_ar)
        print "decrypted : ", ''.join(decrypted_arr)

#permutate_keys(prob_key, en_ar)
