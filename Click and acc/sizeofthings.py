import sys
import time
ls = [
    time.struct_time((2025, 1, 18, 15, 50, 25, 0, -1, -1)),
    dict({'Running': 2, 'Unknown': 91, 'Tilting': 0, 'On-Foot': 3, 'In-Vehicle': 2, 'Still': 4, 'Walking': 1, 'most_likely': 'Unknown', 'On-Bicycle': 0, 'OnStairs': 0}),
    "In motion",
    False,
    0,
    -0.15332,
    0.20532,
    -1.97070,
    3.47144,
    -1.03906,
    -1.40625,
    9.85156,
    False,
    False,
    3.40393,
    0.14180
]
print(sys.getsizeof(ls))