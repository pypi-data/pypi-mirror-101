import os
import owlready2
import pandas as pd
from teamverify import scrapePokedex

#owlready2.set_log_level(9)

dirpath, _ = os.path.split(__file__)
owlready2.JAVA_EXE = os.path.join(dirpath,"java.exe")

def main():
    path = os.path.join(dirpath,'geckodriver.exe')
    scrapePokedex.scrollPage(path,'ss')

    df = pd.read_csv(os.path.join(dirpath,'competitivePokedex.csv'))

    df = df.drop_duplicates()
#print(df)

    baseKBpath = os.path.join(dirpath,"pokemonBase.owl")
    baseKBpath = os.path.normpath(baseKBpath)
    onto = owlready2.get_ontology(baseKBpath).load()
    #newPokemon = onto.Pokemon()
    #print(newPokemon)

    tiers = ['OU','UU','UUBL']

    df = df[df['Tier'].isin(tiers)]

    for _, row in df.iterrows():
        typea = onto['ty'+row['Type1']]

        tempPkmn = onto.Pokemon('spec'+row['Pokemon'].replace(' ',''))
        tempPkmn.hasBaseSpeed.append(row['Spe'])
        tempPkmn.hasType.append(typea)
        if pd.notna(row['Type2']):
            #print(row['type2'])
            typeb = onto['ty'+row['Type2']]
            tempPkmn.hasType.append(typeb)

    with onto:
        owlready2.sync_reasoner(infer_property_values=True)

    #print(onto.base_iri)
    #print(list(onto.classes()))
    #print(list(onto.OffensivePokemon.instances()))

    prodKBpath = os.path.join(dirpath,"pokemonprod.owl")
    prodKBpath = os.path.normpath(prodKBpath)
    onto.save(file=prodKBpath,format='rdfxml')

    #print(onto.specHawlucha.isResistantTo)

if __name__ == '__main__':
    main()
