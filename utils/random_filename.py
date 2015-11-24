import sys
import random
import string

sys.stdout.write(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32)))
