# import dendropy

# tree_str = "[&R] (A, (B, (C, (D, E))));"

# tree = dendropy.Tree.get(
#         data=tree_str,
#         schema="newick")

# print("Before:")
# print(tree.as_string(schema='newick'))
# mrca = tree.mrca(taxon_labels=["D"])
# tree.reroot_at_edge(mrca.edge, update_bipartitions=False)
# print("After:")
# print(tree.as_string(schema='newick'))

from phylo2vec import vecToNewick
arr = [0, 0, 2, 2, 6, 8, 3, 6, 12, 3, 6, 19, 22, 24]
print(vecToNewick(arr))