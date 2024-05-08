import json

path_padrao = "/home/pi/mini-pc-upload-github-infra-compiled/"

def get_limites_por_release():
    try:
        with open(path_padrao + "/config/limite_releases.json") as json_data:
            aux = json.load(json_data)
            limite = aux['limite_maquinas']
    except:
        limite = 0

    return limite

# Checamos se o total de maquinas nao ultrapassou o limite do release
# True: excesso
# False: limite permitido
def check_excesso_maquinas_release(release):
    path = path_padrao + "/releases/" + str(release) + "/lista_maquinas/maquinas.txt"

    try:
        with open(path, 'r') as fp:
            x = len(fp.readlines())

            if x > get_limites_por_release():
                return True
            else:
                return False
    except:
        return True

def obtem_ip_maquina(maquina):
    try:
        with open(path_padrao + "/lista_maquinas/maquinas_ips.txt") as fil:
            lines = fil.readlines()
            lines = [line.strip() for line in lines]

            for linha in lines:
                pos_pipe = linha.find("|")
                maquina_linha = linha[0:pos_pipe].strip()
                ip = linha[pos_pipe+1:len(linha)].strip()

                if maquina_linha == maquina:
                    return ip
    except:
        pass

    return ""

def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

