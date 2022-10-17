import json
import os

for file in os.listdir('json'):
    if file[-3:] == 'txt':
        with open(f'json/{file}', 'r') as f:
            line = f.readline()
            data = json.loads(line)['data']
        with open(f'csv/{file}', 'w') as f:
            for datapoint in data:
                for i, n in enumerate(datapoint):
                    if i != 5:
                        f.write(str(n))
                        f.write(',')
                    else:
                        f.write(str(n))
                        f.write('\n')
