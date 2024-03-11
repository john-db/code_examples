from phylo2vec import newickToNaive

n = "((3 , ((5 , 4) , 2)) , (1 , 0))"
n = n.replace(" ", "")

print(newickToNaive(n))