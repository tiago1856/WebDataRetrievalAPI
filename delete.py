

r1 = {"qwe": 100, "asd": 200}
r2 = {"qwe": None, "asd": 666}

result = dict((k,v if k in r2 and r2[k] in [None, ''] else r2[k]) for k,v in r1.items())

print (result)