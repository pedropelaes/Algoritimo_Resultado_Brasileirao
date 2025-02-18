from playwright.sync_api import sync_playwright
import json
from datetime import datetime 
import time as tempo
start_time = tempo.time()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500, args=["--disable-popup-blocking", "--new-window"])
    
    context = browser.new_context(
    locale="en-US",  
    geolocation={"latitude": 38.71689, "longitude": -9.139705, "accuracy": 100}
    )

    page = context.new_page()
    page.goto("https://www.sofascore.com/pt/torneio/futebol/brazil/brasileirao-serie-a/325#id:58766")

    times = page.get_by_test_id("standings_row")
    print(f"Quantidade de times da liga:{times.count()}")
    #l_times = []
    #for i in range(times.count()):
        #times.nth(i).screenshot(path="teste" + str(i) + ".png") tira print de cada time da pagina
        #l_times.append(times.nth(i).get_attribute("href"))
    #print(l_times)
    player_data = {}
    player_links = {}
    for t in range(times.count()):
        time = context.new_page()
        time.goto("https://www.sofascore.com" + times.nth(t).get_attribute("href"))
        
        
        #time.locator("button.DropdownButton[role='combobox']").nth(0).click() 
        #time.wait_for_selector("ul.Box li.DropdownItem") 
        #time.click("ul.Box li.DropdownItem:nth-child(2)")
        
        time.wait_for_selector('label[for^="listTeamPlayers-"]') #exibe a lista de jogadores no site
        time.click('label[for^="listTeamPlayers-"]')

        time.wait_for_selector("table.Table.fEUhaC") #pega a tabela que contém os jogadores
        tabela_jogadores = time.locator("table.Table.fEUhaC")
        linhas = tabela_jogadores.locator("tr")

        links = []
        nomes_posicao = []
        for i in range(linhas.count()):
            celulas = linhas.nth(i).locator('td')  # Cada célula da linha
            linha_dados = [celulas.nth(j).inner_text() for j in range(celulas.count())]
            if(i != 0):
                linha_dados[0] = linha_dados[0].split('\n', 1)[-1]
                
                link = celulas.nth(0).locator('a').get_attribute('href')
                if link:
                    links.append(link)
            nomes_posicao.append(linha_dados)
            
        for i in nomes_posicao:
            player_data[t]=nomes_posicao
            #print(i)
        for i in links:
            player_links[t]=links
            #print(i)
        
        time.close()
    page.close()
    browser.close()

#formatação dos arquivos json
data_atual = datetime.now().strftime("%Y-%m-%d")
player_data_file = f"player_data_{data_atual}.json"
player_links_file = f"plyer_links_{data_atual}.json"

#gera arquivos json contendo as informações e links de cada jogador de cada time do campeonato
with open(player_data_file, "w", encoding="utf-8") as dados_jogadores:
    json.dump(player_data, dados_jogadores, indent=4, ensure_ascii=False)
with open(player_links_file, "w", encoding="utf-8") as links_jogares:
    json.dump(player_links, links_jogares, indent=4, ensure_ascii=False)


end_time = tempo.time()
print(f"Tempo de execução: {end_time - start_time:.2f} segundos")
print(f"Coleta de dados finalizada. Arquivos gerados: {player_data_file} | {player_links_file}")