import os, median, dendropy, time
from compare_two_trees import compare_trees

def nrf_newicks(n1, n2):
    taxa = dendropy.TaxonNamespace()

    if ";" != n1[-1]:
        n1 += ';'
    if ";" != n2[-1]:
        n2 += ';'
    tree1 = dendropy.Tree.get(data=n1,
                              schema='newick',
                              rooting='force-unrooted',
                              taxon_namespace=taxa)

    tree2 = dendropy.Tree.get(data=n2,
                              schema='newick',
                              rooting='force-unrooted',
                              taxon_namespace=taxa)
    
    temp = compare_trees(tree1, tree2)
    return temp[5]

def main(args):
    repls = ["{:02d}".format(x) for x in range(1, 51)]
    # models = [
    #             "model.10.2000000.0.000001",
    #             "model.50.2000000.0.000001",
    #             "model.100.2000000.0.000001",
    #             "model.200.500000.0.000001",
    #             "model.200.500000.0.0000001",
    #             "model.200.2000000.0.000001",
    #             "model.200.2000000.0.0000001",
    #             "model.200.10000000.0.000001",
    #             "model.200.10000000.0.0000001",
    #             "model.500.2000000.0.000001",
    #             "model.1000.2000000.0.000001"
    #         ]
    models = [
                "model.10.2000000.0.000001",
                "model.50.2000000.0.000001",
            ]

    data = []   
    for model in models:
        mdl_data = [model, 0, 0]
        print(model)
        for repl in repls:
            print("\t" + str(repl))
            input_file = "/Users/john/Desktop/Phylo2VecTests/data/estimated-gene-trees/" + model + "/" + repl + "/estimatedgenetre"
            output_file = "/Users/john/Desktop/Phylo2VecTests/results/p2v/" + model + "/" + repl + "/p2vtree.tre"
            cmd_p2v = "python3 ./p2vm.py -i " + input_file + " -o " + output_file
            
            os.system(cmd_p2v)

            astral3_jar = "/Users/john/Desktop/Phylo2VecTests/Astral/astral.5.7.8.jar"
            astral3_output_file = "/Users/john/Desktop/Phylo2VecTests/results/p2v/" + model + "/" + repl + "/astral3tree.tre"


            cmd_astral = "java -jar " + astral3_jar + " -i " + input_file + " -o " + astral3_output_file
            os.system(cmd_astral)

            species_tree = "/Users/john/Desktop/Phylo2VecTests/data/true-species-trees/" + model + "/" + repl + "/s_tree.trees"
            # astral_tree = "/Users/john/Desktop/Phylo2VecTests/results/astral?/" + model + "/" + repl + "/astral-v474-p1-halfresolved.genes1000"
            
            output_p2v = []
            with open(output_file) as file:
                for line in file:
                    output_p2v.append(line)
            astral_newick = ""
            with open(astral3_output_file) as file:
                for line in file:
                    astral_newick += line
            species_newick = ""
            with open(species_tree) as file:
                for line in file:
                    species_newick += line
            p2v_score = 0.0
            for t in output_p2v:
                tmp = nrf_newicks(t, species_newick)
                if tmp > p2v_score:
                    p2v_score = tmp
            astral_score = nrf_newicks(astral_newick, species_newick)
            mdl_data[1] += p2v_score
            mdl_data[2] += astral_score
        mdl_data[1] = mdl_data[1] / 50
        mdl_data[2] = mdl_data[2] / 50
        data.append(mdl_data)
    for x in data:
        print(x)


if __name__ == "__main__":
    main(None)