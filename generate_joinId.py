import math 
import random
import string

def generate_joinId()->str:
    chars=string.ascii_letters + string.digits
    s=5
    joinId= ''.join(random.sample(chars,s))
    return joinId

print(generate_joinId())