import json
import os

def testjson():
    data = []
    with open('.sync','r') as f:
        for line in f:
            data.append(json.loads(line))
        
        print(data)

'''
def testjson():
    with open(".sync", "a+") as outfile:
        print(outfile)
        d = json.load(outfile)
        print(d)
'''
'''
def testjson():
    my_data = json.loads(open(".sync").read())
    print(my_data)
'''
testjson()

