import re

def parseTeam(teamString):
    """Parse strings for data from official Pokemon Showdown format.

    Keyword arguemnts:\n
    teamString -- a team string, copied from pokepaste or pokemon showdown
    """
    pokemonList = teamString.split('\n\n')

    teamList = []
    #print(pokemonList)
    for pokemon in pokemonList:
        currentPokemonDict = {}
        moveCounter = 1
        currentPokemon = pokemon.split('\n')
        if 'Ability' not in pokemon:
            continue
        
        for attribute in currentPokemon:
            if 'Happiness:' or 'IVs:' or 'Shiny:' in attribute:
                pass
            if '@' in attribute:
                attribute = attribute.split('@')
                currentPokemonDict['Species'] = attribute[0].strip().replace(' ','')
                if '(' in currentPokemonDict['Species']:
                    currentPokemonDict['Species'] = re.search(r'\(([^)]+)', currentPokemonDict['Species']).group(1)
                    if len(currentPokemonDict['Species']) == 1:
                        temp = attribute[0].split('(')[0]
                        currentPokemonDict['Species'] = temp.strip()
                currentPokemonDict['Item'] = attribute[1].strip().replace(' ','')
            if 'Nature' in attribute:
                attribute = attribute.strip()
                attribute = attribute.split(' ')
                currentPokemonDict['Nature'] = attribute[0].strip()
            if '- ' in attribute:
                currentPokemonDict['Move'+str(moveCounter)] = attribute.split('- ')[1].strip().replace(' ','')
                moveCounter += 1
            if 'EVs' in attribute:
                currentPokemonDict['HPEVs'] = 0
                currentPokemonDict['AtkEVs'] = 0
                currentPokemonDict['DefEVs'] = 0
                currentPokemonDict['SpAEVs'] = 0
                currentPokemonDict['SpDEVs'] = 0
                currentPokemonDict['SpeEVs'] = 0

                attribute = attribute.split(':')
                attribute = attribute[1].split('/')
                for item in attribute:
                    item = item.strip()
                    item = item.split(' ')
                    currentPokemonDict[item[1]+'EVs'] = int(item[0])

        teamList.append(currentPokemonDict)
    return teamList

def removeHtmlTags(html):
    clean = re.compile('<.*?>')
    return re.sub(clean,'',html)

def getPokepaste(url):
    import requests
    response = requests.get(url)
    teamString = removeHtmlTags(response.text).replace('\t','')

    teamTemp = parseTeam(teamString)
    teamList = []
    for item in teamTemp:
        if item:
            teamList.append(item)
    return teamList, teamString


if __name__ == "__main__":
    exampleSet = """Tyranitar (M) @ Assault Vest  
    Ability: Sand Stream  
    EVs: 252 HP / 252 Atk / 4 SpD  
    Adamant Nature  
    - Stone Edge  
    - Stealth Rock  
    - Crunch  
    - Earthquake"""

    exampleTeam = """Grimmsnarl @ Light Clay  
    Ability: Prankster  
    Happiness: 160  
    EVs: 252 HP / 4 Atk / 252 SpD  
    Careful Nature  
    - Taunt  
    - Reflect  
    - Light Screen  
    - Drain Punch  

    Dragapult @ Leftovers  
    Ability: Infiltrator  
    EVs: 252 Atk / 4 SpD / 252 Spe  
    Adamant Nature  
    - Dragon Dance  
    - Dragon Darts  
    - Substitute  
    - Phantom Force  

    Cloyster @ King's Rock  
    Ability: Skill Link  
    EVs: 252 Atk / 4 SpD / 252 Spe  
    Adamant Nature  
    - Shell Smash  
    - Ice Shard  
    - Icicle Spear  
    - Rock Blast  

    Bisharp @ Black Glasses  
    Ability: Defiant  
    EVs: 4 HP / 252 Atk / 252 Spe  
    Jolly Nature  
    - Swords Dance  
    - Sucker Punch  
    - Iron Head  
    - Throat Chop  

    Sylveon @ Pixie Plate  
    Ability: Pixilate  
    EVs: 252 HP / 252 SpA / 4 SpD  
    Modest Nature  
    IVs: 0 Atk  
    - Calm Mind  
    - Hyper Voice  
    - Mystical Fire  
    - Draining Kiss  

    Toxtricity @ Throat Spray  
    Ability: Punk Rock  
    EVs: 252 SpA / 252 Spe  
    Timid Nature  
    IVs: 0 Atk  
    - Volt Switch  
    - Sludge Wave  
    - Overdrive  
    - Boomburst  
    """

    webExample = 'https://pokepast.es/8c28cd9d9febe492'

    print(parseTeam(exampleSet),'\n')
    print(parseTeam(exampleTeam),'\n')
    print(getPokepaste(webExample)[0])
