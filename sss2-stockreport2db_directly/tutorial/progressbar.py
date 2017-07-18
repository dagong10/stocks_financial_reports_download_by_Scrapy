from tqdm import trange
from time import sleep
from tqdm import tqdm


'''pbar = tqdm(total=4000,ncols=150)

pbar.update(10)
pbar.close()'''
import sys, time

for i in range(5):
    sys.stdout.write(' ' * 10 + '\r')
    sys.stdout.flush()
    print i
    sys.stdout.write(str(i) * (5 - i) + '\r')
    sys.stdout.flush()
    time.sleep(1)