import json 



with open("data/trumptweets.json", encoding="utf-8") as f:
    data = json.load(f)

import pprint
pprint.pprint(data[0])