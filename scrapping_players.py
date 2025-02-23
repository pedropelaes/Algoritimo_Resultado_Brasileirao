import asyncio
from playwright.async_api import async_playwright; from playwright._impl._errors import TimeoutError
import json
import re
from datetime import datetime 
import time as tempo
import random
start_time = tempo.time()

async def get_players_cartoes_notas(player_page, link):
    await asyncio.sleep(random.uniform(2,5))
    await player_page.goto("https://www.sofascore.com" + link, wait_until="load")
    await player_page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    print("Acessando", "https://www.sofascore.com" + link)
    #buscar a div da nota e dos cartões
    data = {}
    try:
        div_player_summary = player_page.get_by_test_id("player_summary")
        if(await div_player_summary.is_visible()):
            nota_element = div_player_summary.locator(".Text.jwYwht")
            nota = await nota_element.text_content()
        else:
            nota = "N/A"
        
        div_estatisticas = player_page.locator("span:has-text('Estatísticas do jogador')").locator("..").locator("..").locator("..")
        span_cartoes = div_estatisticas.locator("span:has-text('Cartões')").first
        if(await span_cartoes.is_visible()):
            div_cartoes = span_cartoes.locator("..").locator("..")

            n_cartoes = [int(n) for n in re.findall(r'\d+', await div_cartoes.inner_text())]
            amarelos = n_cartoes[0] if len(n_cartoes) > 0 else "N/A"
            seg_amarelo = n_cartoes[1] if len(n_cartoes) > 1 else 0
            vermelhos = n_cartoes[2] if len(n_cartoes) > 2 else 0

            amarelos += seg_amarelo
        else:
            amarelos = "N/A"
            vermelhos = "N/A"

        data["amarelos"] = amarelos
        data["vermelhos"] = vermelhos
        data["nota"] = nota

    except TimeoutError:
        data["amarelos"] = "N/A"
        data["vermelhos"] = "N/A"
        data["nota"] = "N/A"
    finally:
        await player_page.close()

    
    return data
        
async def get_players(context):
    page = await context.new_page()
    await page.goto("https://www.sofascore.com/pt/torneio/futebol/brazil/brasileirao-serie-a/325")
    times = page.get_by_test_id("standings_row")
    q_times = await times.count()
    print(f"Quantidade de times da liga:{q_times}")
    player_data = {}
    player_links = {}
    for t in range(q_times):
        time = await context.new_page()
        await time.goto("https://www.sofascore.com" + await times.nth(t).get_attribute("href"))
        print(f"Acessando: {time.goto}")

        await time.wait_for_selector('label[for^="listTeamPlayers-"]') #exibe a lista de jogadores no site
        await time.click('label[for^="listTeamPlayers-"]')

        await time.wait_for_selector("table.Table.fEUhaC") #busca a tabela que contém os jogadores
        tabela_jogadores =time.locator("table.Table.fEUhaC")
        linhas = tabela_jogadores.locator("tr")

        jogadores = []
        links = []
        for i in range(1, await linhas.count()):
            celulas = linhas.nth(i).locator('td')  # Cada célula da linha
            linha_dados = [await celulas.nth(j).inner_text() for j in range(await celulas.count())]
            
            nome = linha_dados[0] = linha_dados[0].split('\n', 1)[-1] if len(linha_dados) > 0 else "Desconhecido"
            posicao = linha_dados[1] if len(linha_dados) > 1 else "N/A"
            idade = linha_dados[2] if len(linha_dados) > 2 else "N/A"
            link = await celulas.nth(0).locator('a').get_attribute('href')  
            if link:
                links.append(link)

            jogadores.append({
            "nome": nome,
            "posicao": posicao,
            "idade": idade
            })
        
        player_data[t] = jogadores
        player_links[t] = links
        await time.close()
    data = [player_data, player_links]
    mid = tempo.time()
    print(f"Links dos jogadores coletados, iniciando coleta de dados de cada jogador. Tempo de execução : {(mid - start_time)/60:.2f} minutos")
    return data
        

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=100, args=["--disable-popup-blocking", "--new-window"])
        context = await browser.new_context(
            locale="jp_JP",  
            geolocation={"latitude": -33.86882, "longitude": 151.209296, "accuracy": 100}, 
        )#may need to be changed to run properly because of timeout errors
        
        player_data = await get_players(context)
        batch_size = 10
        
        coleta_result = []

        links = [link for time_links in player_data[1].values() for link in time_links]
        for i in range(0, len(links), batch_size):
            batch = links[i:i + batch_size]
            results = await asyncio.gather(*[get_players_cartoes_notas(await context.new_page(), link) for link in batch])
            coleta_result.extend(results)
        

        index = 0
        for time_id, jogadores in player_data[0].items():
            for jogador in jogadores:
                if index < len(coleta_result): 
                    jogador.update(coleta_result[index])
                    index += 1  
        
        await browser.close()
        

        #criação dos arquivos .json
        data_atual = datetime.now().strftime("%Y-%m-%d")
        player_data_file = f"player_data_{data_atual}.json"
        player_links_file = f"plyer_links_{data_atual}.json"

        #gera arquivos json contendo as informações e links de cada jogador de cada time do campeonato
        with open(player_data_file, "w", encoding="utf-8") as dados_jogadores:
            json.dump(player_data[0], dados_jogadores, indent=4, ensure_ascii=False)
        with open(player_links_file, "w", encoding="utf-8") as links_jogares:
            json.dump(player_data[1], links_jogares, indent=4, ensure_ascii=False)


        end_time = tempo.time()
        print(f"Tempo de execução: {(end_time - start_time) / 60:.2f} minutos")
        print(f"Coleta de dados finalizada. Arquivos gerados: {player_data_file} | {player_links_file}")


asyncio.run(main())


