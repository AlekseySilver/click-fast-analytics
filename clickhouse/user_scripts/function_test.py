import sys
import json

for line in sys.stdin:
    data = json.loads(line)
    result = data['num'] * 3  # Example operation
    print(json.dumps({"result": result}))