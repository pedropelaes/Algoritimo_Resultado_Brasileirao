import asyncio
from playwright.async_api import async_playwright; from playwright._impl._errors import TimeoutError
import json
from datetime import datetime 
import time as tempo
start_time = tempo.time()

async def get_manager_info():
    with open("teams_data_2025-02-20.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        links = []
        team = []
        name = []
    #após buscar informações no .json gerado do código "scrapping times.py", pega apenas os links dos tecnicos e adiciona em uma lista
    for i in range (1, 21):
        links.append(data[str(i)]["link_treinador"])
        team.append(data[str(i)]["nome"])
        name.append(data[str(i)]["treinador"])
    return links, team, name

async def get_manager_score(manager_page, link, time, nome):
    await manager_page.goto("https://www.sofascore.com" + link)
    print("Acessando", "https://www.sofascore.com" + link)
    await manager_page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    #buscar a div da media

    try:
        media_element = manager_page.locator("span").filter(has_text="Total de média de pontos por jogo").locator("..")
        media = await media_element.locator("xpath=following-sibling::span").inner_text()

    except:
        media = "N/A"
    return nome, media, time
    

async def main():
    async with async_playwright() as p:
        data = await get_manager_info()
        links = data[0]
        times = data[1]
        nomes = data[2]
        browser = await p.chromium.launch(headless=True, slow_mo=100, args=["--disable-popup-blocking", "--new-window"])
        context = await browser.new_context(
                locale="br_BR",  
                geolocation={"latitude": -33.86882, "longitude": 151.209296, "accuracy": 100}, 
            )#may need to be changed to run properly because of timeout errors
        
        resultado = []
        batch_size = 10
        for i in range(0, len(links), batch_size):
            batch_links = links[i:i + batch_size]
            batch_times = times[i:i + batch_size] 
            batch_nomes = nomes[i:i + batch_size]

            results = await asyncio.gather(
                *[get_manager_score(await context.new_page(), link, time, nome) for link, time, nome in zip(batch_links, batch_times, batch_nomes)]
            )
            resultado.extend(results)
        print(resultado)
        
        treinadores = {
            str(k): { "nome":nome, "nota":nota, "time":time}
            for k, (nome, nota, time) in enumerate(resultado)
        }
    #criação dos arquivos .json
    data_atual = datetime.now().strftime("%Y-%m-%d")
    manager_data_file = f"manager_{data_atual}.json"

    with open(manager_data_file, "w", encoding="utf-8") as dados_treinadores:
        json.dump(treinadores, dados_treinadores, indent=4, ensure_ascii=False)

    end_time = tempo.time()
    print(f"Tempo de execução: {(end_time - start_time) / 60:.2f} minutos")
    print(f"Coleta de dados finalizada. Arquivos gerados: {manager_data_file}")



asyncio.run(main())