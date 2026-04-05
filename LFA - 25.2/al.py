from afd import gerar_afd

afd, simbolos, dict_simbolos, estados_finais = gerar_afd()
ESTADO_ATUAL_AL = '0'
FITA = []
TOKEN = ''
TS = []
print(afd)
print(simbolos, dict_simbolos, estados_finais)
with open('entrada.txt', 'r') as file:
    for num_linha, line in enumerate(file):
        for char in line:
            if char != ' ' and char != '\n':
                if char not in simbolos:
                    ESTADO_ATUAL_AL = '~'
                    TOKEN+=char
                else:
                    posicao = dict_simbolos[char]
                    aux = afd[ESTADO_ATUAL_AL][posicao]
                    ESTADO_ATUAL_AL = aux
                    TOKEN+=char
            else:
                FITA.append(ESTADO_ATUAL_AL)
                if ESTADO_ATUAL_AL in estados_finais:
                    ts_token = {
                        'token': TOKEN,
                        'linha': num_linha,
                        'status': 'aceito'
                    }
                    TS.append(ts_token)
                    TOKEN = ''
                elif ESTADO_ATUAL_AL == '~':
                    ts_token = {
                        'token': TOKEN,
                        'linha': num_linha,
                        'status': 'ERRO'
                    }
                    TS.append(ts_token)
                    TOKEN = ''
                    print("TOKEN NÃO RECONHECIDO")
                ESTADO_ATUAL_AL = '0'
print("Tabela de Simbolos: ", TS)
print("Fita de Estados: ", FITA)        
                    
                    
                    

