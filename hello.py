import json
print('hello, world')
print('hello, world')
with open('./app.json', 'r',encoding='utf-8') as fcc_file:
    fcc_data = json.load(fcc_file)
    #print(fcc_data)
    #print(fcc_data["articalList"])
    officalList = fcc_data["articalList"]
    print(officalList)
    for o in officalList:
        print(o["officalAccout"])
    