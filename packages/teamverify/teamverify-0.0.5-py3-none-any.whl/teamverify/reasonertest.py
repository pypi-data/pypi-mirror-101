import os
import owlready2
owlready2.set_log_level(9)

dirpath, _ = os.path.split(__file__)
print(dirpath)

baseKBpath = os.path.join(dirpath,"pokemonprod.owl")
baseKBpath = os.path.normpath(baseKBpath)
print(baseKBpath)
onto = owlready2.get_ontology(baseKBpath).load()

#namespace = onto.get_namespace("https://github.com/danielverd/teamverify/pokemon#")

print([i for i in onto.individuals()])
print(onto.base_iri)
print(onto.Pokemon.iri)
print(list(onto.Pokemon.subclasses())[-1].iri)

newpk = onto.Pokemon()
newpk.hasSpecies = onto.Pokemon('specZapdos')
newpk.hasAtkEVs = 252
newpk.hasItem = onto.Items('itChoiceBand')
print(newpk.is_a)
with onto:
    owlready2.sync_reasoner(infer_property_values=True,debug=9)

print(newpk.is_a)
print(list(onto.GrassResists.instances()))