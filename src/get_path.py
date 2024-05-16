import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","doc","net_definition","circuit1.txt"))
print(path)
open(path,"r")