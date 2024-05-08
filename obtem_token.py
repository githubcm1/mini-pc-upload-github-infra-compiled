import base64
import os

path_base = os.path.abspath(__file__).replace("obtem_token.py", "./")
arq_token = path_base + 'token_push.txt'

try:
    with open(arq_token) as f:
        aux = f.readlines()
        print(base64.b64decode(aux[0].strip()).decode('utf-8'))
    f.close()
except Exception as e:
    print('')
