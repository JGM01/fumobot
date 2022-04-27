from fumo_purchaser import FumoPurchaser
import sys
from concurrent import futures
from fumo import Fumo

FumosTest = [
    'https://www.amiami.com/eng/detail/?gcode=FIGURE-138984', 
    'https://www.amiami.com/eng/detail/?gcode=FIGURE-138817',
    'https://www.amiami.com/eng/detail?gcode=GOODS-04233282',
    'https://www.amiami.com/eng/detail?gcode=GOODS-04233294',
    'https://www.amiami.com/eng/detail/?gcode=GOODS-04229578',
    'https://www.amiami.com/eng/detail/?gcode=FIGURE-138984', 
    'https://www.amiami.com/eng/detail/?gcode=FIGURE-138817',
    'https://www.amiami.com/eng/detail?gcode=GOODS-04233282',
    'https://www.amiami.com/eng/detail?gcode=GOODS-04233294',
    'https://www.amiami.com/eng/detail/?gcode=GOODS-04229578']

Fumos =[
    Fumo.cirno,
    Fumo.cirno,
    Fumo.cirno,
    Fumo.koishi,
    Fumo.koishi,
    Fumo.koishi,
    Fumo.sanae,
    Fumo.sanae,
    Fumo.sanae,
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
    main()
    print(sys.argv)