import sys
import json

data = sys.stdin.readline()
data_json = json.loads(data)
print('data en .py:',data_json['primer_nombre'])

sys.stdout.flush()