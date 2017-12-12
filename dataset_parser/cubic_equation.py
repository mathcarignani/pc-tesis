import numpy as np


# returns real root for equation: a*x**3 + b*x**2 + c*x + d = 0
def cubic_equation(a, b, c, d):
    coefs = [a, b, c, d]
    roots = np.roots(coefs)
    real_root = roots[np.isreal(roots)][0]
    return real_root.real

coeff_d = {'a': 1.17*10**(-9), 'b': -3.95*10**(-6), 'c': 4.90*10**(-3), 'd': -1.9}

def decagon(m):
    return coeff_d['a']*m**3 + coeff_d['b']*m**2 + coeff_d['c']*m + coeff_d['d']

def decagon_inverse(result):
    return cubic_equation(coeff_d['a'], coeff_d['b'], coeff_d['c'], coeff_d['d'] - result)


coeff_other = {'a': 2.97*10**(-9), 'b': -7.37*10**(-6), 'c': 6.69*10**(-3), 'd': -1.92}

def other(m):
    return coeff_other['a']*m**3 + coeff_other['b']*m**2 + coeff_other['c']*m + coeff_other['d']

def other_inverse(result):
    return cubic_equation(coeff_other['a'], coeff_other['b'], coeff_other['c'], coeff_other['d'] - result)



array = []
for result in array:
    print result, 'decagon_inverse', decagon_inverse(result), 'other_inverse', other_inverse(result)

# sorted[0:5]
array = [0.239635,  0.239898,  0.239948,  0.240032,  0.240248]
# 0.239635 decagon_inverse 1039.71721172 other_inverse 806.335707577
# 0.239898 decagon_inverse 1040.26464764 other_inverse 806.775793852
# 0.239948 decagon_inverse 1040.36876516 other_inverse 806.859473843
# 0.240032 decagon_inverse 1040.54371291 other_inverse 807.000065763
# 0.240248 decagon_inverse 1040.99375275 other_inverse 807.361642233

# sorted[2000:2005]
array = [0.245548,  0.245552,  0.245555,  0.245557,  0.245558]
# 0.245548 decagon_inverse 1052.11240955 other_inverse 816.254469432
# 0.245552 decagon_inverse 1052.12085423 other_inverse 816.261193406
# 0.245555 decagon_inverse 1052.12718779 other_inverse 816.266236397
# 0.245557 decagon_inverse 1052.13141019 other_inverse 816.269598395
# 0.245558 decagon_inverse 1052.13352139 other_inverse 816.271279395

# sorted[-5:]
array = [0.537073,  0.537902,  0.538773,  0.539939,  0.540579]
# 0.537073 decagon_inverse 1526.27340063 other_inverse 1145.62851845
# 0.537902 decagon_inverse 1527.08601326 other_inverse 1146.18152937
# 0.538773 decagon_inverse 1527.93783591 other_inverse 1146.76131234
# 0.539939 decagon_inverse 1529.07503677 other_inverse 1147.53547542
# 0.540579 decagon_inverse 1529.69771548 other_inverse 1147.95943961

first, last = 0.239635, 0.540579

decagon_first, decagon_last = decagon_inverse(first), decagon_inverse(last)
print 'DECAGON', 'first:', first, '=>', decagon_first, '| last:', last, '=>', decagon_last, 'DIFF=', decagon_last - decagon_first
# DECAGON first: 0.239635 => 1039.71721172 | last: 0.540579 => 1529.69771548 DIFF= 489.98050376

other_first, other_last = other_inverse(first), other_inverse(last)
print 'OTHER', 'first:', first, '=>', other_first, '| last:', last, '=>', other_last, 'DIFF=', other_last - other_first
# OTHER first: 0.239635 => 806.335707577 | last: 0.540579 => 1147.95943961 DIFF= 341.623732029
