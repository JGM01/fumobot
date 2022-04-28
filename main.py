from datetime import datetime
import sys

from fumo_purchaser import FumoPurchaser
from concurrent import futures
from fumo import Fumo

Fumos1 =[
    Fumo.cirno,
    Fumo.chen,
    Fumo.eirin,
    Fumo.flandre
]

Fumos = [
    Fumo.test1,
    Fumo.test2,
    Fumo.test3,
    Fumo.test4,
    Fumo.test5,
    Fumo.test6,
    Fumo.test7,
    Fumo.test8,
    Fumo.test9
]

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

def spawn_FumoPurchaser(fumo):
    bot = FumoPurchaser(fumo, USERNAME, PASSWORD)
    bot.run()  

def main():
    with futures.ThreadPoolExecutor() as executor:
        purchasers = list(executor.map(spawn_FumoPurchaser, Fumos))

if __name__ == "__main__":
    start = datetime.now()
    main()
    print(sys.argv)
    print(datetime.now()-start)