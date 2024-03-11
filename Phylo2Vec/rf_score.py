import argparse
import median

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
    
    if None != args.output:
        f = open(args.output, "w")
        for tree in trees:
            f.write(str(score_tree_rf(tree, trees)) + ", " + tree + '\n')
        f.close()
    else:
        for tree in trees:
            print(str(score_tree_rf(tree, trees)) + ", " + tree + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tree", type=str,
                        help="file containing Newick string(s) of the tree to be scored",
                        required=True)
    parser.add_argument("-ts", "--trees", type=str,
                        help="file containing Newick string(s) for the tree to be scored against",
                        required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="Path for output file. if no path given it will be printed to standard output",
                        required=False, default=None)
    main(parser.parse_args())