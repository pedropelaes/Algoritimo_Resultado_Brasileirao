from playwright.sync_api import sync_playwright; from playwright._impl._errors import TimeoutError
import json
import re
from datetime import datetime 
import time as tempo
start_time = tempo.time()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100, args=["--disable-popup-blocking", "--new-window"])
    
    context = browser.new_context(
    locale="pt_br",  
    geolocation={"latitude": -33.86882, "longitude": 151.209296, "accuracy": 100},
    
    )

    page = context.new_page()
    page.goto("https://www.sofascore.com/pt/torneio/futebol/brazil/brasileirao-serie-a/325")

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
        jogadores = []
        #cartoes = []
        for i in range(1, linhas.count()):
            celulas = linhas.nth(i).locator('td')  # Cada célula da linha
            linha_dados = [celulas.nth(j).inner_text() for j in range(celulas.count())]
            
            nome = linha_dados[0] = linha_dados[0].split('\n', 1)[-1] if len(linha_dados) > 0 else "Desconhecido"
            posicao = linha_dados[1] if len(linha_dados) > 1 else "N/A"
            idade = linha_dados[2] if len(linha_dados) > 2 else "N/A"
            link = celulas.nth(0).locator('a').get_attribute('href')
            if link:
                links.append(link)
            

            #cartões de cada jogador
            player_page = context.new_page()
            player_page.goto("https://www.sofascore.com" + link)
            #buscar a div dos cartões
            try:
                div_estatisticas = player_page.locator("span:has-text('Estatísticas do jogador')").locator("..").locator("..").locator("..")
                span_cartoes = div_estatisticas.locator("span:has-text('Cartões')").first
                if(span_cartoes.is_visible()):
                    div_cartoes = span_cartoes.locator("..").locator("..")
                    div_cartoes.inner_text()
                

                    #cartoes.append(div_cartoes.inner_text())
                    n_cartoes = [int(n) for n in re.findall(r'\d+', div_cartoes.inner_text())]
                    amarelos = n_cartoes[0] if len(n_cartoes) > 0 else "N/A"
                    seg_amarelo = n_cartoes[1] if len(n_cartoes) > 1 else 0
                    vermelhos = n_cartoes[2] if len(n_cartoes) > 2 else 0

                    amarelos += seg_amarelo
                    
                    #print(cartoes)
                else:
                    amarelos = "N/A"
                    vermelhos = "N/A"

            except TimeoutError:
                amarelos = "N/A"
                vermelhos = "N/A"

            finally: 
                print(f"Jogador {link}:")
                print(n_cartoes)
                player_page.close()

                
            jogadores.append({
            "nome": nome,
            "posicao": posicao,
            "idade": idade,
            "amarelos": amarelos,
            "vermelhos": vermelhos
        })
            
        for i in jogadores:
            player_data[t] = jogadores
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
tempo_execução = (end_time - start_time) / 60
print(f"Tempo de execução: {tempo_execução:.2f} segundos")
print(f"Coleta de dados finalizada. Arquivos gerados: {player_data_file} | {player_links_file}")