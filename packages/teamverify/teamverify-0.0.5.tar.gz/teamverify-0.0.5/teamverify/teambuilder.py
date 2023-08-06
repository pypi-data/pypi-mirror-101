from teamverify.readTeamSyntax import parseTeam, getPokepaste
import argparse
import os
import sys
import owlready2
import pandas as pd

dirpath, _ = os.path.split(__file__)
owlready2.JAVA_EXE = os.path.join(dirpath,"java.exe")

def parseArgs():
    parser = argparse.ArgumentParser(description="Reads in Pokemon team from stdin.")
    parser.add_argument("team", help="txt file or url containing team")
    parser.add_argument("output", default= 'teamverify-out', help="name to of txt file to export results")
    return parser.parse_args()

def getTeamString(team, html):
    """Returns a dictoinary containing the six Pokemon in the provided team.

    Keyword arguments:\n
    team -- the path to the Smogon official team string\n
    html -- true if the team is given as a webpage, false if given as text
    """
    if html:
        teamList, data = getPokepaste(team)
    else:
        with open(team,'r') as textfile:
            data = textfile.read()
    
        teamList = parseTeam(data)
    
    #print(type(data))
    return teamList, data

def teamReasoner(teamList):
    onto = owlready2.get_ontology(os.path.join(dirpath,"pokemonprod.owl")).load()
    df = pd.read_csv(os.path.join(dirpath,'competitivePokedex.csv'))
    #team = onto.Playstyles()

    #debugi = 0

    classifiedList = []
    for pokemon in teamList:
        #print(pokemon)
        newPokemon = onto.Pokemon()
        newPokemon.hasSpecies = onto.Pokemon('spec'+pokemon['Species'])
        newPokemon.hasItem = onto.Items('it'+pokemon['Item'])

        newPokemon.hasHPEVs = pokemon['HPEVs']
        newPokemon.hasAtkEVs = pokemon['AtkEVs']
        newPokemon.hasDefEVs = pokemon['DefEVs']
        newPokemon.hasSpAEVs = pokemon['SpAEVs']
        newPokemon.hasSpDEVs = pokemon['SpDEVs']
        newPokemon.hasSpeEVs = pokemon['SpeEVs']

        row = df.loc[df['Pokemon'] == pokemon['Species']]
        spe = row.iloc[0]['Spe']
        newPokemon.hasBaseSpeed.append(int(spe))

        newPokemon.hasMove.append(onto.Moves('mv'+pokemon['Move1']))
        newPokemon.hasMove.append(onto.Moves('mv'+pokemon['Move2']))
        newPokemon.hasMove.append(onto.Moves('mv'+pokemon['Move3']))
        newPokemon.hasMove.append(onto.Moves('mv'+pokemon['Move4']))

        classifiedList.append(newPokemon)
        #debugi+=1
        #if debugi > 5:
        #    break

    with onto:
        owlready2.sync_reasoner()
    #onto.save(file='pokemonprod.owl',format='rdfxml')

    characteristics = {'Off':[],'Def':[],'Rocks':[],'HazCon':[],'DefPiv':[],
                       'Walls':[],'Breakers':[],'Sweepers':[],'OffPiv':[],'Stallbreakers':[],
                       'Screens':[], 'Ground':[], 'Water':[], 'Ghost':[], 
                       'Dark':[],'Fire':[],'Grass':[],'CorviknightCounters':[], 'ToxapexCounters':[], 
                       'MandibuzzCounters':[], 'FerrothornCounters':[],
                       'ClefableCounters':[], 'MoltresCounters':[],'SlowbroCounters':[],'ZapdosCounters':[],
                       'HippowdonCounters':[]}

    for classified in classifiedList:
        if classified in list(onto.OffensivePokemon.instances()):
            characteristics['Off'].append(classified)
        if classified in list(onto.DefensivePokemon.instances()):
            characteristics['Def'].append(classified)
        if classified in list(onto.StealthRockers.instances()):
            characteristics['Rocks'].append(classified)
        if classified in list(onto.HazardControllers.instances()):
            characteristics['HazCon'].append(classified)
        if classified in list(onto.DefensivePivots.instances()):
            characteristics['DefPiv'].append(classified)
        if classified in list(onto.Walls.instances()):
            characteristics['Walls'].append(classified)
        if classified in list(onto.Wallbreakers.instances()):
            characteristics['Breakers'].append(classified)
        if classified in list(onto.Sweepers.instances()):
            characteristics['Sweepers'].append(classified)
        if classified in list(onto.OffensivePivots.instances()):
            characteristics['OffPiv'].append(classified)
        if classified in list(onto.ScreenSetters.instances()):
            characteristics['Screens'].append(classified)
        if classified in list(onto.Stallbreakers.instances()):
            characteristics['Stallbreakers'].append(classified)
        if classified in list(onto.GroundResists.instances()):
            characteristics['Ground'].append(classified)
        if classified in list(onto.WaterResists.instances()):
            characteristics['Water'].append(classified)
        if classified in list(onto.GhostResists.instances()):
            characteristics['Ghost'].append(classified)
        if classified in list(onto.DarkResists.instances()):
            characteristics['Dark'].append(classified)
        if classified in list(onto.FireResists.instances()):
            characteristics['Fire'].append(classified)
        if classified in list(onto.GrassResists.instances()):
            characteristics['Grass'].append(classified)
        if classified in list(onto.CorviknightCounters.instances()):
            characteristics['CorviknightCounters'].append(classified)
        if classified in list(onto.ToxapexCounters.instances()):
            characteristics['ToxapexCounters'].append(classified)
        if classified in list(onto.MandibuzzCounters.instances()):
            characteristics['MandibuzzCounters'].append(classified)
        if classified in list(onto.FerrothornCounters.instances()):
            characteristics['FerrothornCounters'].append(classified)
        if classified in list(onto.ClefableCounters.instances()):
            characteristics['ClefableCounters'].append(classified)
        if classified in list(onto.MoltresCounters.instances()):
            characteristics['MoltresCounters'].append(classified)
        if classified in list(onto.SlowbroCounters.instances()):
            characteristics['SlowbroCounters'].append(classified)
        if classified in list(onto.HippowdonCounters.instances()):
            characteristics['HippowdonCounters'].append(classified)
        if classified in list(onto.ZapdosCounters.instances()):
            characteristics['ZapdosCounters'].append(classified)

    #the following code is obsolete since the addition of makeRecommendations()

    #graph = owlready2.default_world.as_rdflib_graph()
    #print(characteristics['MandibuzzCounters'])
    
    #r = list(graph.query(
    #        """
    #        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #        PREFIX owl: <http://www.w3.org/2002/07/owl#>
    #        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    #        PREFIX poke: <http://web.cs.miami.edu/home/dver751/csc751/pokemon#>
    #        SELECT ?species
	#            WHERE { ?subject rdf:type  poke:FerrothornCounters .
    #                    ?subject poke:hasSpecies ?species }
    #        """
    #))
    #print('Consider using',str(r[0]).split('spec')[1].split('\'')[0],'to counter Ferrothorn')
    ##Remember to delete the text instance from the ontology

    return characteristics

#def teamReport(team,recommendations):
def teamReport(team):
    print('-------Team Report-------')
    print('|Playstyle              |')
    print('-------------------------')
    if len(team['Off']) > 4:
        print('Hyper Offense','\n')
    elif len(team['Off']) < 2:
        print('Stall','\n')
    elif len(team['Off']) == 4:
        print('Bulky Offense','\n')
    else:
        print('Balance','\n')
    print('Offensive Pokemon: ', len(team['Off']))
    print('Defensive Pokemon: ', len(team['Def']))
    print('-------------------------')
    print('|Offensive Roles        |')
    print('-------------------------')
    print('Wallbreakers: ',[str(x.hasSpecies).split('spec')[1] for x in team['Breakers']])
    print('Sweepers: ',[str(x.hasSpecies).split('spec')[1] for x in team['Sweepers']])
    print('Pivots: ',[str(x.hasSpecies).split('spec')[1] for x in team['OffPiv']])
    print('-------------------------')
    print('|Defensive Roles        |')
    print('-------------------------')
    print('Walls: ',[str(x.hasSpecies).split('spec')[1] for x in team['Walls']])
    print('Pivots: ',[str(x.hasSpecies).split('spec')[1] for x in team['DefPiv']])
    print('-------------------------')
    print('|Miscellaneous Roles    |')
    print('-------------------------')
    print('Stealth Rockers: ',[str(x.hasSpecies).split('spec')[1] for x in team['Rocks']])
    print('Hazard Control: ',[str(x.hasSpecies).split('spec')[1] for x in team['HazCon']])
    print('Screen Setters: ',[str(x.hasSpecies).split('spec')[1] for x in team['Screens']])
    print('Stallbreakers: ',[str(x.hasSpecies).split('spec')[1] for x in team['Stallbreakers']])
    print('-------------------------')
    print('|Essential Switch-ins   |')
    print('-------------------------')
    print('Ground Resists: ',[str(x.hasSpecies).split('spec')[1] for x in team['Ground']])
    print('Water Resists: ',[str(x.hasSpecies).split('spec')[1] for x in team['Water']])
    print('Ghost Resists: ',[str(x.hasSpecies).split('spec')[1] for x in team['Ghost']])
    print('Dark Resists: ',[str(x.hasSpecies).split('spec')[1] for x in team['Dark']])
    print('Fire Resists: ',[str(x.hasSpecies).split('spec')[1] for x in team['Fire']])
    print('Grass Resists: ',[str(x.hasSpecies).split('spec')[1] for x in team['Grass']])
    print('-------------------------')
    print('|Essential Counters     |')
    print('-------------------------')
    print('Corviknight Counters: ',[str(x.hasSpecies).split('spec')[1] for x in team['CorviknightCounters']])
    print('Toxapex Counters: ',[str(x.hasSpecies).split('spec')[1] for x in team['ToxapexCounters']])
    print('Mandibuzz Counters: ',[str(x.hasSpecies).split('spec')[1] for x in team['MandibuzzCounters']])
    print('Ferrothorn Counters: ',[str(x.hasSpecies).split('spec')[1] for x in team['FerrothornCounters']])
    print('Clefable Counters: ',[str(x.hasSpecies).split('spec')[1] for x in team['ClefableCounters']])
    print('Moltres Counters: ',[str(x.hasSpecies).split('spec')[1] for x in team['MoltresCounters']])
    print('Hippowdon Counters: ',[str(x.hasSpecies).split('spec')[1] for x in team['HippowdonCounters']])
    print('Slowbro Counters: ',[str(x.hasSpecies).split('spec')[1] for x in team['SlowbroCounters']])
    print('Zapdos Counters: ',[str(x.hasSpecies).split('spec')[1] for x in team['ZapdosCounters']])
    print('-------------------------')

    #for item in recommendations:
        #print(item)
        #recommendations are very basic and not helpful, so we're scrapping this function for now

def makeRecommandations(characteristics):
    onto = owlready2.get_ontology(os.path.join(dirpath,"pokemonprod.owl")).load()
    with onto:
        graph = owlready2.default_world.as_rdflib_graph()

    recommendations = []
    for role, pokemon in characteristics.items():
        #print(role,pokemon)
        if role == 'Screens':
            continue
        
        if pokemon == []:
            r = list(graph.query(
                """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX poke: <http://web.cs.miami.edu/home/dver751/csc751/pokemon#>
                SELECT ?species
	                WHERE { ?subject rdf:type  poke:"""+role+""" .
                            ?subject poke:hasSpecies ?species }
            """
            ))
            #print('hi',r)
            if len(r) > 0:
                recommendations.append('Consider using '+str(r[0]).split('spec')[1].split('\'')[0]+' as a '+role+'.')

    numberOfRoles = {}
    for role, pokemon in characteristics.items():
        #print(pokemon)
        for i in pokemon:
            if str(i.hasSpecies) in numberOfRoles:
                numberOfRoles[str(i.hasSpecies)] += 1
            else:
                numberOfRoles[str(i.hasSpecies)] = 1
    
    m = 100
    mostExpendable = ''
    for name, roles in numberOfRoles.items():
        if roles < m:
            m = roles
            mostExpendable = name.split('spec')[1].split('\'')[0]
    recommendations.append('Consider replacing '+mostExpendable+' because it fills the least roles of all Pokemon.')
    
    return recommendations

def teamScore(teamDict):
    #print(teamDict)

    score = 0.0

    for key, value in teamDict.items():
        #print(key, len(value))
        count = 1
        if key in ['DefPiv','Walls','Breakers','Sweepers','OffPiv']:
            for _ in value:
                score += 1
                count += 1
        elif key in ['Off','Def']:
            pass
        else:
            for _ in value:
                score += (1/count)
                count += 1
    print('Team Score: ',score)
    return score

def main():
    args = parseArgs()

    if 'pokepast.es' in args.team:
        team, _ = getTeamString(args.team,True)
    elif '.txt' in args.team:
        #teamPath = os.getcwd()+'\\'+args.team
        team, _ = getTeamString(args.team,False)
    else:
        print('-- ERROR: Unsupported input format --')
        exit()

    if len(team) < 6:
        print('-- Inputted team has fewer than 6 Pokemon --')
    #print(team)

    team2 = teamReasoner(team)
    #recom = makeRecommandations(team2)
    score = teamScore(team2)
    teamReport(team2)

    sys.stdout = open(str(args.output) + '.txt','w')
    #print(data,'\n')
    print(args.team,'\n')
    if len(team) < 6:
        print('-- Inputted team has fewer than 6 Pokemon --')
    teamReport(team2)
    print('Team Score: ',score)
    sys.stdout.close()


if __name__ == "__main__":
    main()