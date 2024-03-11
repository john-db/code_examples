import argparse, dendropy, re, median
from phylo2vec import newickToNaive, naivetovec, vecToNewick

def score_tree_rf(tree, trees):
    val = 0
    for newick in trees:
        val += median.rf_newicks(tree, newick)
    return val

def main(args):
    trees = []
    with open(args.input) as file:
        for line in file:
            trees.append(line)
    
    for s in trees:
        tree = dendropy.Tree.get(data=s, schema="newick")
        print(len(tree.leaf_nodes()))
    
    for s in trees:
        tree.resolve_polytomies()
        tree = dendropy.Tree.get(data=s, schema="newick")
        print(len(tree.nodes()))
    
    #removes branch lengths
    for i in range(0, len(trees)):
        # trees[i] = re.sub(r'(?:\:|\))(?:e-)*[0-9:.]+', '', trees[i])
        trees[i] = re.sub(r'[0-9]*\.[0-9]*', '', trees[i])
        print(len(trees[i]))
        trees[i] = trees[i].replace(':', '')
        trees[i] = trees[i].replace('0', '%zero%')
        trees[i] = trees[i].replace('1', '%one%')
        trees[i] = trees[i].replace('2', '%two%')
        trees[i] = trees[i].replace('3', '%three%')
        trees[i] = trees[i].replace('4', '%four%')
        trees[i] = trees[i].replace('5', '%five%')
        trees[i] = trees[i].replace('6', '%six%')
        trees[i] = trees[i].replace('7', '%seven%')
        trees[i] = trees[i].replace('8', '%eight%')
        trees[i] = trees[i].replace('9', '%nine%')
        trees[i] = trees[i].replace('%%', '&')

        

    tree = trees[0]
    pattern = r'[^(),;\n]+'
    species = re.findall(pattern, tree)
    species_map = {}
    new_root = None
    for i in range(0, len(species)):
        species_map[species[i]] = str(i)
        if i == len(species) - 1:
            new_root = str(i)

    for key in species_map:
        for i in range(0, len(trees)):
            #there will probably be problems if the species names contain numbers
            trees[i] = trees[i].replace(key, species_map[key])

    if args.reroot == "true":
        for i in range(len(trees)):
            tree_str = "[&R] " + trees[i] + ";"
            tree = dendropy.Tree.get(data=tree_str, schema="newick")
            mrca = tree.mrca(taxon_labels=[new_root])
            tree.reroot_at_edge(mrca.edge, update_bipartitions=False)
            trees[i] = tree.as_string(schema='newick')[5:-2]
        
    # naives = map(newickToNaive, trees)
    # naives = list(naives)
    # vectors = map(naivetovec, naives)
    # vectors = list(vectors)
    vectors = []
    for i in range(len(trees)):
        naiv = newickToNaive(trees[i])
        vec = naivetovec(naiv)
        vectors.append(vec)
    my_medians = median.medians(vectors)
    my_medians = list(map(vecToNewick, my_medians))

    # scores = []
    # for i in range(len(my_medians)):
    #     scores.append(score_tree_rf(my_medians[i], trees))

    int_to_species = {species_map[k]:k for k in species_map}
    n = len(int_to_species.keys())
    while n > 0:
        n -= 1
        for i in range(0, len(my_medians)):
            #there will probably be problems if the species names contain numbers
            my_medians[i] = my_medians[i].replace(str(n), int_to_species[str(n)])

    for i in range(len(my_medians)):
            my_medians[i] = my_medians[i].replace('&', '%%')
            my_medians[i] = my_medians[i].replace('%zero%', '0')
            my_medians[i] = my_medians[i].replace('%one%', '1')
            my_medians[i] = my_medians[i].replace('%two%', '2')
            my_medians[i] = my_medians[i].replace('%three%', '3')
            my_medians[i] = my_medians[i].replace('%four%', '4')
            my_medians[i] = my_medians[i].replace('%five%', '5')
            my_medians[i] = my_medians[i].replace('%six%', '6')
            my_medians[i] = my_medians[i].replace('%seven%', '7')
            my_medians[i] = my_medians[i].replace('%eight%', '8')
            my_medians[i] = my_medians[i].replace('%nine%', '9')


    if None != args.output: 
        f = open(args.output, "w")
        for i in range(len(my_medians)):
            f.write(my_medians[i] + '\n')
        f.close()
    else:
        for i in range(len(my_medians)):
            print(my_medians[i] + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str,
                        help="Input file containing newick strings of trees",
                        required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="Path for output file",
                        required=False, default=None)
    parser.add_argument("-r", "--reroot", type=str,
                        help="if true then the input trees will all be rerooted to be rooted at the same taxon",
                        required=False, default="true", choices=['true', 'false'])
    main(parser.parse_args())