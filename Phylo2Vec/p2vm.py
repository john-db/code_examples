import argparse, dendropy, re, median, treeswift
from phylo2vec import newickToNaive, naivetovec, vecToNewick

def check_leafsets(newicks, msg):
    leaves = []
    for s in newicks:
        tree = treeswift.read_tree_newick(s)
        temp = []
        for node in tree.traverse_postorder():
            if node.is_leaf():
                temp.append(node.get_label())
        temp = sorted(temp)
        leaves.append(temp)
    
    for l in leaves:
        if leaves[0] != l:
            raise Exception(msg + ", " + str(len(leaves[0])) + ", " + str(len(l)))

def main(args):
    newicks = []
    with open(args.input) as file:
        for line in file:
            newicks.append(line)
    
    # check_leafsets(newicks, "Trees are not all on the same leafset 1")

    relabelling = {}
    tree = treeswift.read_tree_newick(newicks[0])
    spec_int = 0
    for node in tree.traverse_postorder():
        if node.is_leaf():
            relabelling[node.get_label()] = str(spec_int)
            spec_int += 1
    spec_int -= 1
            
    for i in range(len(newicks)):
        tree = treeswift.read_tree_newick(newicks[i])
        tree.resolve_polytomies()
        tree.rename_nodes(relabelling)
        for node in tree.traverse_postorder():
            node.set_edge_length(-999.999)
            if not node.is_leaf():
                node.set_label(None)
        tree_str = tree.newick().replace(':-999.999', "")
        tree_str = "[&R] " + tree_str
        tree = dendropy.Tree.get(data=tree_str, schema="newick")
        if args.reroot == "true":
            mrca = tree.mrca(taxon_labels=[spec_int])
            tree.reroot_at_edge(mrca.edge, update_bipartitions=False)
        newicks[i] = tree.as_string(schema='newick')[5:-2]

    # check_leafsets(newicks, "Trees are not all on the same leafset 2")

    vectors = []
    for i in range(len(newicks)):
        naiv = newickToNaive(newicks[i])
        vec = naivetovec(naiv)
        vectors.append(vec)
    my_medians = median.medians(vectors)
    my_medians = list(map(vecToNewick, my_medians))

    int_to_species = {relabelling[k]:k for k in relabelling}
    for i in range(0, len(my_medians)):
        tree = treeswift.read_tree_newick(my_medians[i])
        tree.rename_nodes(int_to_species)
        my_medians[i] = tree.newick()

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