import re
import json

txtReg = re.compile("(?P<num>[0-9]*?)(?:\n|\r\n?)")


# open the txt file which matches 
idtxtfile = open("ids.txt")
idtxt = idtxtfile.read()
idtxtfile.close()

a = txtReg.findall(idtxt)
a = map(int,a)
pretty = json.dumps(a, indent=4, sort_keys=True)

idjson = open("ids.json", "w")
idjson.write(pretty)
idjson.close()
