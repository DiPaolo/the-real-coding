import random
import string
import time

PHRASE = 'PASSWORD'

cur_phrase = ['>', ' ']
for ch in PHRASE:
    cur_phrase.append(' ')
    for i in range(random.randint(300, 3000)):
        print('', end='\r', flush=True)
        cur_phrase[-1:] = random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        print(''.join(cur_phrase), end='')
        time.sleep(0.001)

    cur_phrase[-1:] = ch

print('', end='\r', flush=True)
print(''.join(cur_phrase))
