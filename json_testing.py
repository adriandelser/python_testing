import json, os

filename = "myjson.json"
d = {}
#d[1]=2

with open(filename,"w+") as f:
    json.dump(d,f,indent=4)

with open(filename,"r") as f:
    #buffer = f.read()
    # print(buffer)
    data = json.load(f)
    print(data)


with open(filename, "a+") as f:
    print("hi")
    check_file = os.stat(filename).st_size
    print(check_file)


