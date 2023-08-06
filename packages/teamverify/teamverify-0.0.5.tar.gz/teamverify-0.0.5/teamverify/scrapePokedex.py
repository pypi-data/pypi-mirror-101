import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

dirpath, _ = os.path.split(__file__)

def scrollPage(path,gen='ss'):
    print('Populating the Competitive Pokedex. This may take a few minutes.')
    print('If a browser window opens, do not touch it.')

    driver = webdriver.Firefox(executable_path=path)
    driver.get('https://www.smogon.com/dex/'+gen+'/pokemon/')

    csv_file = open(os.path.join(dirpath,'competitivePokedex.csv'),'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Pokemon','Type1','Type2','Tier','HP','Atk','Def','SpA','SpD','Spe'])

    height = driver.get_window_size()['height'] - 150
    newHeight = height

    scrolls = 0
    while scrolls < 120:
        scrapeDex(driver.page_source,csv_writer)
        driver.execute_script("window.scrollTo(0, "+str(newHeight)+");")
        time.sleep(0.1)
        scrolls += 1
        newHeight += height

    csv_file.close()
    print('Success!')
    print('You may now close the browser window.')

def scrapeDex(source,csv_writer):
    soup = BeautifulSoup(source,'lxml')

    for pokemon in soup.find_all('div',class_='PokemonAltRow'):
        row = []
        elementaltypes = []

        name = pokemon.find('div',class_='PokemonAltRow-name').text
        name = name.replace(' ','')
        tier = pokemon.find('div',class_='PokemonAltRow-tags').text
        hp = pokemon.find('div',class_='PokemonAltRow-hp').span.text
        atk = pokemon.find('div',class_='PokemonAltRow-atk').span.text
        dfs = pokemon.find('div',class_='PokemonAltRow-def').span.text
        spa = pokemon.find('div',class_='PokemonAltRow-spa').span.text
        spd = pokemon.find('div',class_='PokemonAltRow-spd').span.text
        spe = pokemon.find('div',class_='PokemonAltRow-spe').span.text

        types = pokemon.find('div',class_='PokemonAltRow-types')
        for poketype in types.find_all('a'):
            elementaltypes.append(poketype.text)
        if len(elementaltypes) == 1:
            elementaltypes.append(None)
    
        row = [name,elementaltypes[0],elementaltypes[1],tier,hp,atk,dfs,spa,spd,spe]
    
        if tier not in ['NFE','LC','Uber','','CAP','National Dex','AG']:
            csv_writer.writerow(row)
       
        #print(row)

if __name__ == '__main__':
    genkey = 'ss'
    path = os.path.join(dirpath,'geckodriver.exe')

    scrollPage(path,genkey)
