# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
from collections import OrderedDict

dictio = OrderedDict()

dictio["a"] = 1
dictio["b"] = 0
dictio["c"] = 2

sorted_items = sorted(dictio.items(), key=lambda x: x[1])

for i in range(len(sorted_items)):
    print(sorted_items[i])
    
