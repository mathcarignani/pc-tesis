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

# sorted[2000:2005]
array = [0.245548,  0.245552,  0.245555,  0.245557,  0.245558]
# 0.245548 decagon_inverse 1052.11240955 other_inverse 816.254469432
# 0.245552 decagon_inverse 1052.12085423 other_inverse 816.261193406
# 0.245555 decagon_inverse 1052.12718779 other_inverse 816.266236397
# 0.245557 decagon_inverse 1052.13141019 other_inverse 816.269598395
# 0.245558 decagon_inverse 1052.13352139 other_inverse 816.271279395

first, last = 0.239635, 0.540579

decagon_first, decagon_last = decagon_inverse(first), decagon_inverse(last)
print 'DECAGON', 'first:', first, '=>', decagon_first, '| last:', last, '=>', decagon_last, 'DIFF=', decagon_last - decagon_first
# DECAGON first: 0.239635 => 1039.71721172 | last: 0.540579 => 1529.69771548 DIFF= 489.98050376

other_first, other_last = other_inverse(first), other_inverse(last)
print 'OTHER', 'first:', first, '=>', other_first, '| last:', last, '=>', other_last, 'DIFF=', other_last - other_first
# OTHER first: 0.239635 => 806.335707577 | last: 0.540579 => 1147.95943961 DIFF= 341.623732029


########################################################################################################################

# 'vwc_222.smet.csv'

# len(sorted) = 428

# 0.128,  0.129,  0.13 ,  0.131,  0.132,  0.133,  0.134,  0.135,
# 0.136,  0.137,  0.138,  0.139,  0.14 ,  0.141,  0.142,  0.143,
# 0.144,  0.145,  0.146,  0.147,  0.148,  0.149,  0.15 ,  0.151,
# 0.152,  0.153,  0.154,  0.155,  0.156,  0.157,  0.158,  0.159,
# 0.16 ,  0.161,  0.162,  0.163,  0.164,  0.165,  0.166,  0.167,
# 0.168,  0.169,  0.17 ,  0.171,  0.172,  0.173,  0.174,  0.175,
# 0.176,  0.177,  0.178,  0.179,  0.18 ,  0.181,  0.182,  0.183,
# 0.184,  0.185,  0.186,  0.187,  0.188,  0.189,  0.19 ,  0.191,
# 0.192,  0.193,  0.194,  0.195,  0.196,  0.197,  0.198,  0.199,
# 0.2  ,  0.201,  0.202,  0.203,  0.204,  0.205,  0.206,  0.207,
# 0.208,  0.209,  0.21 ,  0.211,  0.212,  0.213,  0.214,  0.215,
# 0.216,  0.217,  0.218,  0.219,  0.22 ,  0.221,  0.222,  0.223,
# 0.224,  0.225,  0.226,  0.227,  0.228,  0.229,  0.23 ,  0.231,
# 0.232,  0.233,  0.234,  0.235,  0.236,  0.237,  0.238,  0.239,
# 0.24 ,  0.241,  0.242,  0.243,  0.244,  0.245,  0.246,  0.247,
# 0.248,  0.249,  0.25 ,  0.251,  0.252,  0.253,  0.254,  0.255,
# 0.256,  0.257,  0.258,  0.259,  0.26 ,  0.261,  0.262,  0.263,
# 0.264,  0.265,  0.266,  0.267,  0.268,  0.269,  0.27 ,  0.271,
# 0.272,  0.273,  0.274,  0.275,  0.276,  0.277,  0.278,  0.279,
# 0.28 ,  0.281,  0.282,  0.283,  0.284,  0.285,  0.286,  0.287,
# 0.288,  0.289,  0.29 ,  0.291,  0.292,  0.293,  0.294,  0.295,
# 0.296,  0.297,  0.298,  0.299,  0.3  ,  0.301,  0.302,  0.303,
# 0.304,  0.305,  0.306,  0.307,  0.308,  0.309,  0.31 ,  0.311,
# 0.312,  0.313,  0.314,  0.315,  0.316,  0.317,  0.318,  0.319,
# 0.32 ,  0.321,  0.322,  0.323,  0.324,  0.325,  0.326,  0.327,
# 0.328,  0.329,  0.33 ,  0.331,  0.332,  0.333,  0.334,  0.335,
# 0.336,  0.337,  0.338,  0.339,  0.34 ,  0.341,  0.342,  0.343,
# 0.344,  0.345,  0.346,  0.347,  0.348,  0.349,  0.35 ,  0.351,
# 0.352,  0.353,  0.354,  0.355,  0.356,  0.357,  0.358,  0.359,
# 0.36 ,  0.361,  0.362,  0.363,  0.364,  0.365,  0.366,  0.367,
# 0.368,  0.37 ,  0.371,  0.372,  0.373,  0.374,  0.376,  0.377,
# 0.378,  0.379,  0.382,  0.383,  0.384,  0.385,  0.386,  0.387,
# 0.388,  0.389,  0.39 ,  0.391,  0.392,  0.393,  0.394,  0.395,
# 0.396,  0.397,  0.398,  0.399,  0.4  ,  0.401,  0.402,  0.403,
# 0.404,  0.405,  0.406,  0.407,  0.408,  0.409,  0.41 ,  0.411,
# 0.412,  0.413,  0.414,  0.415,  0.416,  0.417,  0.418,  0.419,
# 0.42 ,  0.421,  0.422,  0.423,  0.424,  0.425,  0.426,  0.427,
# 0.428,  0.429,  0.43 ,  0.431,  0.432,  0.433,  0.434,  0.435,
# 0.436,  0.437,  0.438,  0.439,  0.44 ,  0.441,  0.442,  0.443,
# 0.444,  0.445,  0.446,  0.447,  0.448,  0.449,  0.45 ,  0.451,
# 0.452,  0.453,  0.454,  0.455,  0.456,  0.457,  0.458,  0.459,
# 0.46 ,  0.461,  0.462,  0.463,  0.464,  0.465,  0.466,  0.467,
# 0.468,  0.469,  0.47 ,  0.471,  0.472,  0.473,  0.474,  0.475,
# 0.476,  0.477,  0.478,  0.479,  0.48 ,  0.481,  0.482,  0.483,
# 0.484,  0.485,  0.486,  0.487,  0.488,  0.489,  0.49 ,  0.491,
# 0.492,  0.493,  0.494,  0.495,  0.496,  0.497,  0.498,  0.499,
# 0.5  ,  0.501,  0.502,  0.503,  0.504,  0.505,  0.506,  0.507,
# 0.508,  0.509,  0.51 ,  0.511,  0.512,  0.513,  0.514,  0.515,
# 0.516,  0.517,  0.518,  0.519,  0.52 ,  0.521,  0.522,  0.523,
# 0.524,  0.525,  0.526,  0.527,  0.528,  0.529,  0.53 ,  0.531,
# 0.532,  0.533,  0.535,  0.536,  0.537,  0.538,  0.539,  0.54 ,
# 0.541,  0.542,  0.543,  0.544,  0.545,  0.546,  0.548,  0.549,
# 0.55 ,  0.551,  0.552,  0.553,  0.554,  0.555,  0.556,  0.558,
# 0.559,  0.56 ,  0.561,  0.562

# 0.128 decagon_inverse 847.716706828 other_inverse 647.366554503
# 0.129 decagon_inverse 849.097801662 other_inverse 648.502874145
# 0.13 decagon_inverse 850.484033853 other_inverse 649.643893994
# 0.131 decagon_inverse 851.875434946 other_inverse 650.789642277
# 0.132 decagon_inverse 853.272036587 other_inverse 651.940147175
# 0.133 decagon_inverse 854.673870519 other_inverse 653.095436813
# 0.134 decagon_inverse 856.080968577 other_inverse 654.255539242
# 0.135 decagon_inverse 857.493362681 other_inverse 655.420482432
# 0.136 decagon_inverse 858.911084829 other_inverse 656.590294257
# 0.137 decagon_inverse 860.334167094 other_inverse 657.765002479
# 0.138 decagon_inverse 861.762641617 other_inverse 658.944634738
# 0.139 decagon_inverse 863.196540595 other_inverse 660.129218533
# 0.14 decagon_inverse 864.63589628 other_inverse 661.31878121
# 0.141 decagon_inverse 866.080740969 other_inverse 662.513349943
# 0.142 decagon_inverse 867.531106995 other_inverse 663.712951722
# 0.143 decagon_inverse 868.987026721 other_inverse 664.917613329
# 0.144 decagon_inverse 870.448532531 other_inverse 666.127361327
# 0.145 decagon_inverse 871.915656818 other_inverse 667.342222039
# 0.146 decagon_inverse 873.38843198 other_inverse 668.562221525
# 0.147 decagon_inverse 874.866890406 other_inverse 669.787385571
# 0.148 decagon_inverse 876.351064469 other_inverse 671.01773966
# 0.149 decagon_inverse 877.840986514 other_inverse 672.253308955
# 0.15 decagon_inverse 879.336688845 other_inverse 673.494118278
# 0.151 decagon_inverse 880.838203718 other_inverse 674.740192085
# 0.152 decagon_inverse 882.345563328 other_inverse 675.991554443
# 0.153 decagon_inverse 883.858799795 other_inverse 677.248229008
# 0.154 decagon_inverse 885.377945151 other_inverse 678.510239
# 0.155 decagon_inverse 886.903031332 other_inverse 679.777607174
# 0.156 decagon_inverse 888.434090157 other_inverse 681.050355798
# 0.157 decagon_inverse 889.97115332 other_inverse 682.328506624
# 0.158 decagon_inverse 891.514252372 other_inverse 683.612080859
# 0.159 decagon_inverse 893.063418708 other_inverse 684.901099138
# 0.16 decagon_inverse 894.618683547 other_inverse 686.195581496
# 0.161 decagon_inverse 896.180077923 other_inverse 687.495547333
# 0.162 decagon_inverse 897.747632661 other_inverse 688.801015385
# 0.163 decagon_inverse 899.321378365 other_inverse 690.112003697
# 0.164 decagon_inverse 900.901345396 other_inverse 691.42852958
# 0.165 decagon_inverse 902.487563857 other_inverse 692.750609588
# 0.166 decagon_inverse 904.080063569 other_inverse 694.078259475
# 0.167 decagon_inverse 905.678874058 other_inverse 695.411494166
# 0.168 decagon_inverse 907.284024529 other_inverse 696.750327718
# 0.169 decagon_inverse 908.895543845 other_inverse 698.094773281
# 0.17 decagon_inverse 910.51346051 other_inverse 699.444843065
# 0.171 decagon_inverse 912.137802641 other_inverse 700.8005483
# 0.172 decagon_inverse 913.768597949 other_inverse 702.161899193
# 0.173 decagon_inverse 915.405873712 other_inverse 703.528904894
# 0.174 decagon_inverse 917.049656753 other_inverse 704.901573451
# 0.175 decagon_inverse 918.699973414 other_inverse 706.279911768
# 0.176 decagon_inverse 920.356849529 other_inverse 707.663925567
# 0.177 decagon_inverse 922.020310399 other_inverse 709.053619341
# 0.178 decagon_inverse 923.690380762 other_inverse 710.448996314
# 0.179 decagon_inverse 925.367084767 other_inverse 711.850058392
# 0.18 decagon_inverse 927.050445947 other_inverse 713.256806126
# 0.181 decagon_inverse 928.740487184 other_inverse 714.669238657
# 0.182 decagon_inverse 930.437230681 other_inverse 716.08735368
# 0.183 decagon_inverse 932.140697934 other_inverse 717.511147391
# 0.184 decagon_inverse 933.850909693 other_inverse 718.940614443
# 0.185 decagon_inverse 935.567885938 other_inverse 720.375747902
# 0.186 decagon_inverse 937.291645836 other_inverse 721.816539193
# 0.187 decagon_inverse 939.022207714 other_inverse 723.262978061
# 0.188 decagon_inverse 940.75958902 other_inverse 724.715052518
# 0.189 decagon_inverse 942.50380629 other_inverse 726.172748797
# 0.19 decagon_inverse 944.254875108 other_inverse 727.636051305
# 0.191 decagon_inverse 946.01281007 other_inverse 729.104942577
# 0.192 decagon_inverse 947.777624747 other_inverse 730.579403228
# 0.193 decagon_inverse 949.549331645 other_inverse 732.059411903
# 0.194 decagon_inverse 951.327942164 other_inverse 733.544945238
# 0.195 decagon_inverse 953.113466562 other_inverse 735.035977807
# 0.196 decagon_inverse 954.905913909 other_inverse 736.532482081
# 0.197 decagon_inverse 956.705292048 other_inverse 738.034428383
# 0.198 decagon_inverse 958.511607551 other_inverse 739.541784842
# 0.199 decagon_inverse 960.324865679 other_inverse 741.054517354
# 0.2 decagon_inverse 962.145070336 other_inverse 742.572589537
# 0.201 decagon_inverse 963.972224023 other_inverse 744.095962694
# 0.202 decagon_inverse 965.806327799 other_inverse 745.62459577
# 0.203 decagon_inverse 967.647381231 other_inverse 747.15844532
# 0.204 decagon_inverse 969.495382349 other_inverse 748.697465466
# 0.205 decagon_inverse 971.350327603 other_inverse 750.241607869
# 0.206 decagon_inverse 973.212211811 other_inverse 751.790821695
# 0.207 decagon_inverse 975.081028118 other_inverse 753.345053583
# 0.208 decagon_inverse 976.956767947 other_inverse 754.904247619
# 0.209 decagon_inverse 978.839420949 other_inverse 756.46834531
# 0.21 decagon_inverse 980.728974959 other_inverse 758.037285559
# 0.211 decagon_inverse 982.625415948 other_inverse 759.611004648
# 0.212 decagon_inverse 984.528727974 other_inverse 761.189436219
# 0.213 decagon_inverse 986.438893134 other_inverse 762.772511256
# 0.214 decagon_inverse 988.355891521 other_inverse 764.360158077
# 0.215 decagon_inverse 990.279701171 other_inverse 765.952302327
# 0.216 decagon_inverse 992.210298021 other_inverse 767.548866967
# 0.217 decagon_inverse 994.147655858 other_inverse 769.149772276
# 0.218 decagon_inverse 996.091746278 other_inverse 770.754935855
# 0.219 decagon_inverse 998.042538634 other_inverse 772.364272628
# 0.22 decagon_inverse 1000.0 other_inverse 773.977694855
# 0.221 decagon_inverse 1001.96409512 other_inverse 775.595112144
# 0.222 decagon_inverse 1003.93478636 other_inverse 777.216431469
# 0.223 decagon_inverse 1005.91203368 other_inverse 778.841557192
# 0.224 decagon_inverse 1007.89579458 other_inverse 780.470391086
# 0.225 decagon_inverse 1009.88602408 other_inverse 782.102832371
# 0.226 decagon_inverse 1011.88267464 other_inverse 783.738777743
# 0.227 decagon_inverse 1013.88569616 other_inverse 785.378121416
# 0.228 decagon_inverse 1015.89503595 other_inverse 787.020755163
# 0.229 decagon_inverse 1017.91063865 other_inverse 788.666568367
# 0.23 decagon_inverse 1019.93244625 other_inverse 790.315448069
# 0.231 decagon_inverse 1021.96039802 other_inverse 791.967279031
# 0.232 decagon_inverse 1023.99443052 other_inverse 793.621943788
# 0.233 decagon_inverse 1026.03447752 other_inverse 795.279322722
# 0.234 decagon_inverse 1028.08047003 other_inverse 796.939294127
# 0.235 decagon_inverse 1030.13233625 other_inverse 798.601734285
# 0.236 decagon_inverse 1032.19000156 other_inverse 800.266517544
# 0.237 decagon_inverse 1034.2533885 other_inverse 801.933516398
# 0.238 decagon_inverse 1036.32241676 other_inverse 803.602601575
# 0.239 decagon_inverse 1038.39700316 other_inverse 805.273642129
# 0.24 decagon_inverse 1040.47706167 other_inverse 806.94650553
# 0.241 decagon_inverse 1042.56250336 other_inverse 808.621057763
# 0.242 decagon_inverse 1044.65323644 other_inverse 810.297163428
# 0.243 decagon_inverse 1046.74916626 other_inverse 811.974685845
# 0.244 decagon_inverse 1048.85019527 other_inverse 813.653487156
# 0.245 decagon_inverse 1050.95622311 other_inverse 815.33342844
# 0.246 decagon_inverse 1053.06714653 other_inverse 817.014369823
# 0.247 decagon_inverse 1055.1828595 other_inverse 818.696170587
# 0.248 decagon_inverse 1057.30325314 other_inverse 820.378689293
# 0.249 decagon_inverse 1059.42821584 other_inverse 822.061783895
# 0.25 decagon_inverse 1061.5576332 other_inverse 823.745311856
# 0.251 decagon_inverse 1063.69138813 other_inverse 825.429130275
# 0.252 decagon_inverse 1065.82936084 other_inverse 827.113096003
# 0.253 decagon_inverse 1067.97142891 other_inverse 828.797065763
# 0.254 decagon_inverse 1070.11746735 other_inverse 830.480896278
# 0.255 decagon_inverse 1072.26734858 other_inverse 832.164444389
# 0.256 decagon_inverse 1074.42094258 other_inverse 833.847567175
# 0.257 decagon_inverse 1076.57811688 other_inverse 835.530122078
# 0.258 decagon_inverse 1078.73873663 other_inverse 837.21196702
# 0.259 decagon_inverse 1080.90266469 other_inverse 838.892960524
# 0.26 decagon_inverse 1083.06976169 other_inverse 840.57296183
# 0.261 decagon_inverse 1085.23988611 other_inverse 842.251831012
# 0.262 decagon_inverse 1087.41289433 other_inverse 843.929429092
# 0.263 decagon_inverse 1089.58864075 other_inverse 845.605618151
# 0.264 decagon_inverse 1091.76697786 other_inverse 847.28026144
# 0.265 decagon_inverse 1093.94775633 other_inverse 848.953223482
# 0.266 decagon_inverse 1096.13082508 other_inverse 850.624370183
# 0.267 decagon_inverse 1098.31603143 other_inverse 852.293568926
# 0.268 decagon_inverse 1100.50322115 other_inverse 853.960688673
# 0.269 decagon_inverse 1102.69223858 other_inverse 855.625600056
# 0.27 decagon_inverse 1104.88292673 other_inverse 857.288175468
# 0.271 decagon_inverse 1107.07512741 other_inverse 858.94828915
# 0.272 decagon_inverse 1109.26868132 other_inverse 860.605817272
# 0.273 decagon_inverse 1111.46342815 other_inverse 862.260638013
# 0.274 decagon_inverse 1113.65920672 other_inverse 863.912631635
# 0.275 decagon_inverse 1115.8558551 other_inverse 865.561680553
# 0.276 decagon_inverse 1118.05321069 other_inverse 867.207669399
# 0.277 decagon_inverse 1120.25111039 other_inverse 868.850485085
# 0.278 decagon_inverse 1122.44939069 other_inverse 870.490016861
# 0.279 decagon_inverse 1124.64788778 other_inverse 872.126156364
# 0.28 decagon_inverse 1126.8464377 other_inverse 873.758797669
# 0.281 decagon_inverse 1129.04487645 other_inverse 875.387837332
# 0.282 decagon_inverse 1131.24304012 other_inverse 877.013174428
# 0.283 decagon_inverse 1133.44076499 other_inverse 878.634710589
# 0.284 decagon_inverse 1135.63788767 other_inverse 880.252350028
# 0.285 decagon_inverse 1137.83424524 other_inverse 881.865999571
# 0.286 decagon_inverse 1140.02967531 other_inverse 883.475568679
# 0.287 decagon_inverse 1142.22401622 other_inverse 885.080969461
# 0.288 decagon_inverse 1144.41710707 other_inverse 886.682116692
# 0.289 decagon_inverse 1146.6087879 other_inverse 888.27892782
# 0.29 decagon_inverse 1148.79889981 other_inverse 889.871322975
# 0.291 decagon_inverse 1150.98728499 other_inverse 891.459224967
# 0.292 decagon_inverse 1153.17378694 other_inverse 893.042559289
# 0.293 decagon_inverse 1155.35825049 other_inverse 894.621254108
# 0.294 decagon_inverse 1157.54052195 other_inverse 896.195240261
# 0.295 decagon_inverse 1159.72044919 other_inverse 897.764451239
# 0.296 decagon_inverse 1161.89788175 other_inverse 899.328823175
# 0.297 decagon_inverse 1164.07267093 other_inverse 900.888294827
# 0.298 decagon_inverse 1166.2446699 other_inverse 902.442807554
# 0.299 decagon_inverse 1168.41373374 other_inverse 903.992305299
# 0.3 decagon_inverse 1170.57971958 other_inverse 905.536734558
# 0.301 decagon_inverse 1172.74248664 other_inverse 907.076044355
# 0.302 decagon_inverse 1174.90189636 other_inverse 908.61018621
# 0.303 decagon_inverse 1177.05781238 other_inverse 910.13911411
# 0.304 decagon_inverse 1179.21010071 other_inverse 911.662784472
# 0.305 decagon_inverse 1181.35862974 other_inverse 913.181156109
# 0.306 decagon_inverse 1183.50327031 other_inverse 914.69419019
# 0.307 decagon_inverse 1185.64389575 other_inverse 916.201850206
# 0.308 decagon_inverse 1187.78038198 other_inverse 917.704101925
# 0.309 decagon_inverse 1189.91260752 other_inverse 919.200913352
# 0.31 decagon_inverse 1192.04045352 other_inverse 920.692254686
# 0.311 decagon_inverse 1194.16380386 other_inverse 922.17809828
# 0.312 decagon_inverse 1196.28254512 other_inverse 923.658418591
# 0.313 decagon_inverse 1198.39656666 other_inverse 925.133192138
# 0.314 decagon_inverse 1200.5057606 other_inverse 926.602397456
# 0.315 decagon_inverse 1202.61002192 other_inverse 928.06601505
# 0.316 decagon_inverse 1204.70924838 other_inverse 929.524027347
# 0.317 decagon_inverse 1206.80334061 other_inverse 930.976418651
# 0.318 decagon_inverse 1208.89220211 other_inverse 932.423175094
# 0.319 decagon_inverse 1210.97573924 other_inverse 933.864284589
# 0.32 decagon_inverse 1213.05386122 other_inverse 935.299736782
# 0.321 decagon_inverse 1215.12648017 other_inverse 936.729523009
# 0.322 decagon_inverse 1217.19351105 other_inverse 938.153636241
# 0.323 decagon_inverse 1219.25487172 other_inverse 939.572071045
# 0.324 decagon_inverse 1221.31048288 other_inverse 940.984823532
# 0.325 decagon_inverse 1223.36026808 other_inverse 942.391891312
# 0.326 decagon_inverse 1225.40415371 other_inverse 943.793273447
# 0.327 decagon_inverse 1227.44206896 other_inverse 945.188970409
# 0.328 decagon_inverse 1229.47394583 other_inverse 946.578984029
# 0.329 decagon_inverse 1231.4997191 other_inverse 947.963317459
# 0.33 decagon_inverse 1233.51932628 other_inverse 949.341975121
# 0.331 decagon_inverse 1235.53270762 other_inverse 950.714962668
# 0.332 decagon_inverse 1237.53980605 other_inverse 952.082286941
# 0.333 decagon_inverse 1239.54056716 other_inverse 953.443955923
# 0.334 decagon_inverse 1241.5349392 other_inverse 954.799978703
# 0.335 decagon_inverse 1243.52287297 other_inverse 956.150365431
# 0.336 decagon_inverse 1245.50432185 other_inverse 957.495127278
# 0.337 decagon_inverse 1247.47924175 other_inverse 958.834276402
# 0.338 decagon_inverse 1249.44759105 other_inverse 960.1678259
# 0.339 decagon_inverse 1251.40933057 other_inverse 961.49578978
# 0.34 decagon_inverse 1253.36442352 other_inverse 962.818182918
# 0.341 decagon_inverse 1255.31283548 other_inverse 964.135021023
# 0.342 decagon_inverse 1257.25453435 other_inverse 965.446320604
# 0.343 decagon_inverse 1259.18949027 other_inverse 966.752098932
# 0.344 decagon_inverse 1261.11767564 other_inverse 968.052374009
# 0.345 decagon_inverse 1263.039065 other_inverse 969.347164534
# 0.346 decagon_inverse 1264.95363505 other_inverse 970.636489873
# 0.347 decagon_inverse 1266.86136456 other_inverse 971.920370023
# 0.348 decagon_inverse 1268.76223433 other_inverse 973.198825586
# 0.349 decagon_inverse 1270.65622718 other_inverse 974.471877739
# 0.35 decagon_inverse 1272.54332784 other_inverse 975.739548204
# 0.351 decagon_inverse 1274.42352295 other_inverse 977.00185922
# 0.352 decagon_inverse 1276.296801 other_inverse 978.258833516
# 0.353 decagon_inverse 1278.16315228 other_inverse 979.510494286
# 0.354 decagon_inverse 1280.02256883 other_inverse 980.756865161
# 0.355 decagon_inverse 1281.87504439 other_inverse 981.997970188
# 0.356 decagon_inverse 1283.72057436 other_inverse 983.2338338
# 0.357 decagon_inverse 1285.55915578 other_inverse 984.464480799
# 0.358 decagon_inverse 1287.3907872 other_inverse 985.68993633
# 0.359 decagon_inverse 1289.21546875 other_inverse 986.910225859
# 0.36 decagon_inverse 1291.03320199 other_inverse 988.125375153
# 0.361 decagon_inverse 1292.84398994 other_inverse 989.335410261
# 0.362 decagon_inverse 1294.64783698 other_inverse 990.540357489
# 0.363 decagon_inverse 1296.44474884 other_inverse 991.740243387
# 0.364 decagon_inverse 1298.23473256 other_inverse 992.935094727
# 0.365 decagon_inverse 1300.01779642 other_inverse 994.124938486
# 0.366 decagon_inverse 1301.79394991 other_inverse 995.309801828
# 0.367 decagon_inverse 1303.56320371 other_inverse 996.489712091
# 0.368 decagon_inverse 1305.32556961 other_inverse 997.664696765
# 0.37 decagon_inverse 1308.82969033 other_inverse 1000.0
# 0.371 decagon_inverse 1310.57147404 other_inverse 1001.16037418
# 0.372 decagon_inverse 1312.30642757 other_inverse 1002.315934
# 0.373 decagon_inverse 1314.03456776 other_inverse 1003.4667075
# 0.374 decagon_inverse 1315.7559124 other_inverse 1004.61272279
# 0.376 decagon_inverse 1319.17829035 other_inverse 1006.89059154
# 0.377 decagon_inverse 1320.87936338 other_inverse 1008.02250148
# 0.378 decagon_inverse 1322.57372022 other_inverse 1009.14976618
# 0.379 decagon_inverse 1324.26138261 other_inverse 1010.27241393 >>>>> salto
# 0.382 decagon_inverse 1329.28443094 other_inverse 1013.61293852
# 0.383 decagon_inverse 1330.94554658 other_inverse 1014.71740145
# 0.384 decagon_inverse 1332.60008641 other_inverse 1015.81738883
# 0.385 decagon_inverse 1334.24807591 other_inverse 1016.91292886
# 0.386 decagon_inverse 1335.88954111 other_inverse 1018.00404968
# 0.387 decagon_inverse 1337.52450851 other_inverse 1019.09077939
# 0.388 decagon_inverse 1339.15300511 other_inverse 1020.17314603
# 0.389 decagon_inverse 1340.77505835 other_inverse 1021.25117756
# 0.39 decagon_inverse 1342.39069608 other_inverse 1022.32490187
# 0.391 decagon_inverse 1343.99994655 other_inverse 1023.39434679
# 0.392 decagon_inverse 1345.60283841 other_inverse 1024.45954003
# 0.393 decagon_inverse 1347.19940063 other_inverse 1025.52050925
# 0.394 decagon_inverse 1348.78966255 other_inverse 1026.57728197
# 0.395 decagon_inverse 1350.37365379 other_inverse 1027.62988564
# 0.396 decagon_inverse 1351.95140427 other_inverse 1028.6783476
# 0.397 decagon_inverse 1353.5229442 other_inverse 1029.72269508
# 0.398 decagon_inverse 1355.08830403 other_inverse 1030.76295518
# 0.399 decagon_inverse 1356.64751443 other_inverse 1031.7991549
# 0.4 decagon_inverse 1358.20060631 other_inverse 1032.83132111
# 0.401 decagon_inverse 1359.74761078 other_inverse 1033.85948056
# 0.402 decagon_inverse 1361.28855911 other_inverse 1034.88365986
# 0.403 decagon_inverse 1362.82348276 other_inverse 1035.90388551
# 0.404 decagon_inverse 1364.35241332 other_inverse 1036.92018385
# 0.405 decagon_inverse 1365.87538255 other_inverse 1037.9325811
# 0.406 decagon_inverse 1367.39242231 other_inverse 1038.94110333
# 0.407 decagon_inverse 1368.90356455 other_inverse 1039.94577648
# 0.408 decagon_inverse 1370.40884136 other_inverse 1040.94662633
# 0.409 decagon_inverse 1371.90828487 other_inverse 1041.94367853
# 0.41 decagon_inverse 1373.40192731 other_inverse 1042.93695856
# 0.411 decagon_inverse 1374.88980095 other_inverse 1043.92649176
# 0.412 decagon_inverse 1376.37193811 other_inverse 1044.91230334
# 0.413 decagon_inverse 1377.84837115 other_inverse 1045.89441832
# 0.414 decagon_inverse 1379.31913244 other_inverse 1046.87286158
# 0.415 decagon_inverse 1380.78425439 other_inverse 1047.84765784
# 0.416 decagon_inverse 1382.24376937 other_inverse 1048.81883169
# 0.417 decagon_inverse 1383.6977098 other_inverse 1049.78640751
# 0.418 decagon_inverse 1385.14610804 other_inverse 1050.75040957
# 0.419 decagon_inverse 1386.58899645 other_inverse 1051.71086195
# 0.42 decagon_inverse 1388.02640735 other_inverse 1052.66778858
# 0.421 decagon_inverse 1389.45837302 other_inverse 1053.62121323
# 0.422 decagon_inverse 1390.8849257 other_inverse 1054.57115949
# 0.423 decagon_inverse 1392.30609756 other_inverse 1055.51765081
# 0.424 decagon_inverse 1393.72192071 other_inverse 1056.46071047
# 0.425 decagon_inverse 1395.13242722 other_inverse 1057.40036159
# 0.426 decagon_inverse 1396.53764904 other_inverse 1058.3366271
# 0.427 decagon_inverse 1397.93761808 other_inverse 1059.26952981
# 0.428 decagon_inverse 1399.33236612 other_inverse 1060.19909232
# 0.429 decagon_inverse 1400.72192488 other_inverse 1061.12533711
# 0.43 decagon_inverse 1402.10632598 other_inverse 1062.04828647
# 0.431 decagon_inverse 1403.48560091 other_inverse 1062.96796252
# 0.432 decagon_inverse 1404.85978109 other_inverse 1063.88438725
# 0.433 decagon_inverse 1406.22889778 other_inverse 1064.79758244
# 0.434 decagon_inverse 1407.59298216 other_inverse 1065.70756975
# 0.435 decagon_inverse 1408.95206528 other_inverse 1066.61437065
# 0.436 decagon_inverse 1410.30617805 other_inverse 1067.51800646
# 0.437 decagon_inverse 1411.65535127 other_inverse 1068.41849832
# 0.438 decagon_inverse 1412.99961558 other_inverse 1069.31586725
# 0.439 decagon_inverse 1414.33900152 other_inverse 1070.21013405
# 0.44 decagon_inverse 1415.67353946 other_inverse 1071.10131942
# 0.441 decagon_inverse 1417.00325964 other_inverse 1071.98944385
# 0.442 decagon_inverse 1418.32819215 other_inverse 1072.8745277
# 0.443 decagon_inverse 1419.64836693 other_inverse 1073.75659116
# 0.444 decagon_inverse 1420.96381377 other_inverse 1074.63565427
# 0.445 decagon_inverse 1422.27456233 other_inverse 1075.5117369
# 0.446 decagon_inverse 1423.58064207 other_inverse 1076.38485877
# 0.447 decagon_inverse 1424.88208233 other_inverse 1077.25503945
# 0.448 decagon_inverse 1426.17891226 other_inverse 1078.12229834
# 0.449 decagon_inverse 1427.47116089 other_inverse 1078.9866547
# 0.45 decagon_inverse 1428.75885704 other_inverse 1079.84812764
# 0.451 decagon_inverse 1430.0420294 other_inverse 1080.70673609
# 0.452 decagon_inverse 1431.32070649 other_inverse 1081.56249886
# 0.453 decagon_inverse 1432.59491663 other_inverse 1082.4154346
# 0.454 decagon_inverse 1433.86468801 other_inverse 1083.26556178
# 0.455 decagon_inverse 1435.13004865 other_inverse 1084.11289878
# 0.456 decagon_inverse 1436.39102636 other_inverse 1084.95746377
# 0.457 decagon_inverse 1437.64764883 other_inverse 1085.79927481
# 0.458 decagon_inverse 1438.89994354 other_inverse 1086.6383498
# 0.459 decagon_inverse 1440.1479378 other_inverse 1087.47470651
# 0.46 decagon_inverse 1441.39165878 other_inverse 1088.30836254
# 0.461 decagon_inverse 1442.63113344 other_inverse 1089.13933536
# 0.462 decagon_inverse 1443.86638857 other_inverse 1089.96764231
# 0.463 decagon_inverse 1445.09745081 other_inverse 1090.79330057
# 0.464 decagon_inverse 1446.3243466 other_inverse 1091.61632718
# 0.465 decagon_inverse 1447.54710221 other_inverse 1092.43673904
# 0.466 decagon_inverse 1448.76574375 other_inverse 1093.25455294
# 0.467 decagon_inverse 1449.98029712 other_inverse 1094.06978549
# 0.468 decagon_inverse 1451.19078808 other_inverse 1094.88245319
# 0.469 decagon_inverse 1452.3972422 other_inverse 1095.69257239
# 0.47 decagon_inverse 1453.59968487 other_inverse 1096.50015932
# 0.471 decagon_inverse 1454.79814132 other_inverse 1097.30523007
# 0.472 decagon_inverse 1455.99263658 other_inverse 1098.10780059
# 0.473 decagon_inverse 1457.18319553 other_inverse 1098.90788671
# 0.474 decagon_inverse 1458.36984285 other_inverse 1099.70550413
# 0.475 decagon_inverse 1459.55260308 other_inverse 1100.5006684
# 0.476 decagon_inverse 1460.73150055 other_inverse 1101.29339498
# 0.477 decagon_inverse 1461.90655944 other_inverse 1102.08369916
# 0.478 decagon_inverse 1463.07780375 other_inverse 1102.87159613
# 0.479 decagon_inverse 1464.24525731 other_inverse 1103.65710094
# 0.48 decagon_inverse 1465.40894377 other_inverse 1104.44022855
# 0.481 decagon_inverse 1466.56888661 other_inverse 1105.22099374
# 0.482 decagon_inverse 1467.72510914 other_inverse 1105.99941122
# 0.483 decagon_inverse 1468.87763452 other_inverse 1106.77549555
# 0.484 decagon_inverse 1470.0264857 other_inverse 1107.54926117
# 0.485 decagon_inverse 1471.17168551 other_inverse 1108.32072243
# 0.486 decagon_inverse 1472.31325656 other_inverse 1109.08989352
# 0.487 decagon_inverse 1473.45122133 other_inverse 1109.85678853
# 0.488 decagon_inverse 1474.58560212 other_inverse 1110.62142146
# 0.489 decagon_inverse 1475.71642106 other_inverse 1111.38380615
# 0.49 decagon_inverse 1476.84370014 other_inverse 1112.14395636
# 0.491 decagon_inverse 1477.96746114 other_inverse 1112.90188573
# 0.492 decagon_inverse 1479.08772572 other_inverse 1113.65760776
# 0.493 decagon_inverse 1480.20451535 other_inverse 1114.41113589
# 0.494 decagon_inverse 1481.31785135 other_inverse 1115.16248339
# 0.495 decagon_inverse 1482.42775489 other_inverse 1115.91166348
# 0.496 decagon_inverse 1483.53424695 other_inverse 1116.65868924
# 0.497 decagon_inverse 1484.63734837 other_inverse 1117.40357363
# 0.498 decagon_inverse 1485.73707985 other_inverse 1118.14632953
# 0.499 decagon_inverse 1486.83346189 other_inverse 1118.88696971
# 0.5 decagon_inverse 1487.92651487 other_inverse 1119.62550683
# 0.501 decagon_inverse 1489.016259 other_inverse 1120.36195344
# 0.502 decagon_inverse 1490.10271433 other_inverse 1121.096322
# 0.503 decagon_inverse 1491.18590078 other_inverse 1121.82862486
# 0.504 decagon_inverse 1492.26583809 other_inverse 1122.55887428
# 0.505 decagon_inverse 1493.34254586 other_inverse 1123.2870824
# 0.506 decagon_inverse 1494.41604355 other_inverse 1124.01326129
# 0.507 decagon_inverse 1495.48635045 other_inverse 1124.73742289
# 0.508 decagon_inverse 1496.55348572 other_inverse 1125.45957906
# 0.509 decagon_inverse 1497.61746837 other_inverse 1126.17974158
# 0.51 decagon_inverse 1498.67831726 other_inverse 1126.8979221
# 0.511 decagon_inverse 1499.73605109 other_inverse 1127.61413219
# 0.512 decagon_inverse 1500.79068844 other_inverse 1128.32838335
# 0.513 decagon_inverse 1501.84224774 other_inverse 1129.04068695
# 0.514 decagon_inverse 1502.89074728 other_inverse 1129.75105428
# 0.515 decagon_inverse 1503.93620519 other_inverse 1130.45949656
# 0.516 decagon_inverse 1504.97863948 other_inverse 1131.1660249
# 0.517 decagon_inverse 1506.01806802 other_inverse 1131.87065031
# 0.518 decagon_inverse 1507.05450853 other_inverse 1132.57338375
# 0.519 decagon_inverse 1508.08797861 other_inverse 1133.27423604
# 0.52 decagon_inverse 1509.1184957 other_inverse 1133.97321796
# 0.521 decagon_inverse 1510.14607714 other_inverse 1134.67034018
# 0.522 decagon_inverse 1511.17074009 other_inverse 1135.36561329
# 0.523 decagon_inverse 1512.19250163 other_inverse 1136.0590478
# 0.524 decagon_inverse 1513.21137866 other_inverse 1136.75065412
# 0.525 decagon_inverse 1514.22738798 other_inverse 1137.4404426
# 0.526 decagon_inverse 1515.24054626 other_inverse 1138.12842349
# 0.527 decagon_inverse 1516.25087001 other_inverse 1138.81460696
# 0.528 decagon_inverse 1517.25837565 other_inverse 1139.49900312
# 0.529 decagon_inverse 1518.26307946 other_inverse 1140.18162198
# 0.53 decagon_inverse 1519.26499758 other_inverse 1140.86247347
# 0.531 decagon_inverse 1520.26414605 other_inverse 1141.54156745
# 0.532 decagon_inverse 1521.26054077 other_inverse 1142.21891369
# 0.533 decagon_inverse 1522.25419752 other_inverse 1142.89452191 >>>>> salto
# 0.535 decagon_inverse 1524.23335963 other_inverse 1144.24056269
# 0.536 decagon_inverse 1525.21889595 other_inverse 1144.91101429
# 0.537 decagon_inverse 1526.20175622 other_inverse 1145.5797659
# 0.538 decagon_inverse 1527.18195562 other_inverse 1146.24682688
# 0.539 decagon_inverse 1528.15950923 other_inverse 1146.91220647
# 0.54 decagon_inverse 1529.13443198 other_inverse 1147.57591385
# 0.541 decagon_inverse 1530.10673873 other_inverse 1148.23795814
# 0.542 decagon_inverse 1531.07644418 other_inverse 1148.89834838
# 0.543 decagon_inverse 1532.04356295 other_inverse 1149.55709354
# 0.544 decagon_inverse 1533.00810954 other_inverse 1150.21420252
# 0.545 decagon_inverse 1533.97009833 other_inverse 1150.86968417
# 0.546 decagon_inverse 1534.92954361 other_inverse 1151.52354723 >>>>> salto
# 0.548 decagon_inverse 1536.84086016 other_inverse 1152.82645236
# 0.549 decagon_inverse 1537.79275944 other_inverse 1153.47551162
# 0.55 decagon_inverse 1538.74217123 other_inverse 1154.12298669
# 0.551 decagon_inverse 1539.68910927 other_inverse 1154.76888602
# 0.552 decagon_inverse 1540.63358719 other_inverse 1155.41321796
# 0.553 decagon_inverse 1541.57561852 other_inverse 1156.05599083
# 0.554 decagon_inverse 1542.51521669 other_inverse 1156.69721287
# 0.555 decagon_inverse 1543.45239503 other_inverse 1157.33689227
# 0.556 decagon_inverse 1544.38716677 other_inverse 1157.97503713 >>>>> salto
# 0.558 decagon_inverse 1546.24954283 other_inverse 1159.24675542
# 0.559 decagon_inverse 1547.17717312 other_inverse 1159.88034478
# 0.56 decagon_inverse 1548.10244871 other_inverse 1160.51243148
# 0.561 decagon_inverse 1549.02538235 other_inverse 1161.14302332
# 0.562 decagon_inverse 1549.94598667 other_inverse 1161.77212808


first, last = 0.128, 0.562

decagon_first, decagon_last = decagon_inverse(first), decagon_inverse(last)
print 'DECAGON', 'first:', first, '=>', decagon_first, '| last:', last, '=>', decagon_last, 'DIFF=', decagon_last - decagon_first
# DECAGON first: 0.128 => 847.716706828 | last: 0.562 => 1549.94598667 DIFF= 702.229279844

other_first, other_last = other_inverse(first), other_inverse(last)
print 'OTHER', 'first:', first, '=>', other_first, '| last:', last, '=>', other_last, 'DIFF=', other_last - other_first
# OTHER first: 0.128 => 647.366554503 | last: 0.562 => 1161.77212808 DIFF= 514.405573574

