import numpy as np
import json

codes = {}

with open('./iso_3116.txt', 'r') as f:
    
    # loop over each line in the README file
    for idx, line in enumerate(f):
        
        c = int(np.floor(idx/5))
        d = {}
        
        if idx % 5 == 0: nm = line[0:-1]
        elif idx % 5 == 2: a2 = line[0:-1]
        elif idx % 5 == 3: a3 = line[0:-1]
        elif idx % 5 == 4: nu = line[0:-1]
        
        if idx % 5 == 4:
            codes[a2] = {
                        'name': nm,
                        'alpha-3': a3,
                        'numeric': nu
            }
                                            
f.close()

with open('iso_3116.json', 'w') as f:
    json.dump(codes, f)
f.close()