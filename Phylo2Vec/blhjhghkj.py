import treeswift, dendropy

# Example Newick string
# newick_tree = "(((7:0.00175,6:0.00259)1.000:0.12463,(10:0.02213,1:0.04178)0.963:0.01880)1.000:0.05016,(5:0.04086,3:0.01992)0.997:0.02821,(9:0.15292,(4:0.05423,(0:0.33772,(2:0.00585,8:0.00391)1.000:0.15674)0.333:0.02692)0.170:0.01160)0.014:0.00518);"
newick_tree = "(((ANAPL:0.15004701289883681792,(MELGA:0.06852746966292433406,GALGA:0.02806991309533716020)98:0.01129333118898663210)100:0.02839209972802107101,(((((((((APAVI:0.17211920844527911489,(COLST:0.13991950440335995665,MERNU:0.16144552155733596366)17:0.00010597275077815566)27:0.00610459560581358765,(PICPU:0.16265556361328128987,LEPDI:0.10112194675189489779)47:0.01066218020461296920)9:0.00000156363365135683,BUCRH:0.13054089272829674795)56:0.00342935692048223400,(FALPE:0.08844243002416672661,((MELUN:0.08268494893562179648,NESNO:0.07675912018149405602)100:0.04456231160774062894,(ACACH:0.24634382123087894545,(MANVI:0.09460264239946025722,(CORBR:0.07321830563188426455,(GEOFO:0.03186964505905238998,TAEGU:0.05044455691259962932)100:0.06006081286235149391)100:0.19679021737956406413)99:0.02358347808824740738)94:0.03535211760463262409)40:0.00151576014609972726)65:0.00434822233619993302)78:0.00349456612925147167,TYTAL:0.06328685801957038837)48:0.00067085657263923849,(CARCR:0.07329354289057132821,(CATAU:0.02988308638341550388,(HALLE:0.00200924537597809132,HALAL:0.00121972015064305975)100:0.02890596368590006224)99:0.00744601022464197460)53:0.00127395336385111306)57:0.00319074138938787348,BALRE:0.07053327920445486010)92:0.00583751513405914892,((((PHALE:0.06679994003398197211,CUCCA:0.16101453375324997763)46:0.00591871452285576503,((CHAVO:0.08107165479201602909,COLLI:0.11105262789986017347)81:0.01714341864500404725,(MESUN:0.08020237485190495619,CHLUN:0.10651677458832237155)53:0.00878373521762731806)10:0.00000156363365135683)64:0.00379045562562694725,PTEGU:0.11220285161076389013)13:0.00000156363365135683,OPHHO:0.11351711526636036609)43:0.00099303125533518541)80:0.00288228986214429965,(((CALAN:0.15700973860552491779,CHAPE:0.09433725707767888491)100:0.10832352039358227047,TAUER:0.07694859963433779704)54:0.00554723207629068127,((CAPCA:0.10218584130992136583,(EURHE:0.13905544839977709848,(PODCR:0.07334212179928764619,PHORU:0.05611782168892624073)100:0.04815596212938678955)30:0.00110065079999781810)32:0.00114644822115179436,((PHACA:0.08434588739249335165,(((EGRGA:0.06881741012211126107,NIPNI:0.05617975507327876983)63:0.00039545164776056270,PELCR:0.04110876500684533530)97:0.00875871604758548736,(FULGL:0.03612791740039868194,(PYGAD:0.01232028446008543755,APTFO:0.01325404673668620359)100:0.02394902133644447040)74:0.00162136894622639887)50:0.00054233735770363803)97:0.00393996059743883555,GAVST:0.04214378888772779552)95:0.00400740031082684293)26:0.00039370878405453060)97:0.00918300904225779341)100:0.02626198536811132078)100:0.02595623883875774335,(STRCA:0.13869640603606264717,TINMA:0.18851053475181184238)100:0.02595623883875774335);"
# Create a treeswift tree from the Newick string
tree = treeswift.read_tree_newick(newick_tree)

relabelling = {}
i = 0
for node in tree.traverse_postorder():
    print(node)
    node.set_edge_length(-999.999)
    if node.is_leaf():
        relabelling[node.get_label()] = i
        i += 1
    else:
        node.set_label(None)
tree.rename_nodes(relabelling)


print(tree.newick().replace(':-999.999', ""))
tree_str = tree.newick().replace(':-999.999', "")
tree_str = "[&R] " + tree_str
tree = dendropy.Tree.get(data=tree_str, schema="newick")
mrca = tree.mrca(taxon_labels=["0"])
tree.reroot_at_edge(mrca.edge, update_bipartitions=False)
print(tree.as_string(schema='newick')[5:-2])