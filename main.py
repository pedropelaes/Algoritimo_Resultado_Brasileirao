import subprocess
import sys
import os

def is_pip_installed():
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

if not is_pip_installed():
    print("pip not found. Installing pip...")
    subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)

pip_command = [sys.executable, "-m", "pip"]

try:
    import playwright
except ImportError:
    print("Playwright not found. Installing playwright...")
    subprocess.run(pip_command + ["install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)

from backend.scrapping_managers import main as managers
from backend.scrapping_times import main as times
from backend.scrapping_players import main as players
import asyncio
from pathlib import Path

def check_Json_files_folder():
    path = Path.cwd() / "Json_files"
    try:
        path.mkdir(exist_ok=True)
        print("Json_files Exists.")
        return path
    except PermissionError:
        print("Error: No permission for directory creation. Try setting up the program on another directory.")

async def main():
    menu = 0
    path = check_Json_files_folder()
    while(menu != 5 and path):
        print("\n|Coleta de dados|\n|Digite:\n|1-Coletar informações dos times(Tempo estimado: 01:32 minutos)\n|2-Coletar informações dos técnicos(Tempo estimado: 45 segundos)\n|3-Coletar informações dos jogadores(Tempo estimado: 30 minutos)\n|4-Coletar tudo(Tempo estimado: 33 minutos)\n|5-sair\n")
        menu = int(input())
        while(menu < 1 and menu > 5):
            menu=int(input("|Opção invalida. Digite novamente:\n"))
        if menu == 1:
            print("Iniciando scrapping_times.py")
            await asyncio.to_thread(times, path)
        elif menu == 2:
            print("Iniciando scrapping_managers.py")
            await managers(path)
        elif menu == 3:
            print("Iniciando scrapping_players.py")
            await players(path)
        elif menu == 4:
            print("Iniciando coleta completa: ")
            times(path)
            await managers(path)
            await players(path)
    if not path:
        print("Error in the creation for Json_files folder.")


asyncio.run(main())
