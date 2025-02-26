from scrapping_managers import main as managers
from scrapping_times import main as times
from scrapping_players import main as players
import asyncio

async def main():
    menu = 0
    while(menu != 5):
        print("|Coleta de dados|\n|Digite:\n|1-Coletar informações dos times(Tempo estimado: 01:32 minutos)\n|2-Coletar informações dos técnicos(Tempo estimado: 45 segundos)\n|3-Coletar informações dos jogadores(Tempo estimado: 30 minutos)\n|4-Coletar tudo(Tempo estimado: 33 minutos)\n|5-sair\n")
        menu = int(input())
        while(menu < 1 and menu > 5):
            menu=int(input("|Opção invalida. Digite novamente:\n"))
        if menu == 1:
            print("Iniciando scrapping_times.py")
            times()
        elif menu == 2:
            print("Iniciando scrapping_managers.py")
            managers()
        elif menu == 3:
            print("Iniciando scrapping_players.py")
            players()
        elif menu == 4:
            print("Iniciando coleta completa: ")
            times()
            managers()
            players()
        


asyncio.run(main())
