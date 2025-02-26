import scrapping_managers 
import scrapping_times
import scrapping_players
import asyncio

async def main():
    menu = 0
    while(menu != 5):
        print("|Coleta de dados|\n|Digite:\n|1-Coletar informações dos times(Tempo estimado:01:32 minutos)\n|2-Coletar informações dos técnicos(Tempo estimado:)\n|3-Coletar informações dos jogadores(Tempo estimado:)\n|4-Coletar tudo(Tempo estimado:)\n|5-sair\n")
        menu = int(input())
        while(menu < 1 and menu > 5):
            menu=int(input("|Opção invalida. Digite novamente:\n"))
asyncio.run(main())