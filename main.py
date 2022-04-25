from fumo_purchaser import FumoPurchaser
from concurrent.futures import ThreadPoolExecutor
import sys
from datetime import datetime

start = datetime.now()

# Test URLs, not the actual fumos
Fumos = [
    'https://www.amiami.com/eng/detail/?gcode=GOODS-04228618', 
    'https://www.amiami.com/eng/detail/?gcode=GOODS-04228617',
    'https://www.amiami.com/eng/detail/?gcode=GOODS-04228616',
    'https://www.amiami.com/eng/detail/?gcode=GOODS-04228619']

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
MAX_THREADS = int(sys.argv[3])

def spawn_FumoPurchaser(fumo):
    bot = FumoPurchaser(fumo, USERNAME, PASSWORD)
    bot.execute()    
    print("Success!")

def main():
    with ThreadPoolExecutor(max_workers = MAX_THREADS) as executor:
        results = executor.map(spawn_FumoPurchaser, Fumos)

if __name__ == "__main__":
    main()
    print(sys.argv)
    print(datetime.now()-start)