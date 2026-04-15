import numpy


def generate(afd, final_states):
    # Dicionário Vazio Inicial -> Cabeçalho (Nenhuma Transição)
    al = [dict()]
    # Posição, (Index), Dos Estados -> {Estado: Linha Da Matriz} -> Linha Da Matriz = Posição Da Lista No AL)
    states_position = dict()
    # Percorre As Linhas Da Matriz (Para Popular O Dicionário Acima)
    for row in range(afd.shape[0]):
        # Percorre As Colunas Da Matriz
        for column in range(afd.shape[1]):
            # Se É A Primeira Coluna (Index De Estados)
            if column == 0:
                states_position[str(afd[row, column]).strip('@')] = row
    # Cria O Analizador Léxico (Lista De Dicionários)
    # Percorre As Linhas Da Matriz
    for row in range(afd.shape[0]):
        # Ignora O Cabeçalho
        if row == 0:
            continue
        state_transitions = dict()
        # Percorre As Colunas Da Matriz
        for column in range(afd.shape[1]):
            # Ignora O Index
            if column == 0:
                continue
            # Adiciona A Transição
            state_transitions[str(afd[0, column])] = states_position[afd[row, column]]
        # Salva O Dicionário De Transições Por Estado
        al.append(state_transitions)
    # Corrige Dicionário De Estados Finais
    new_final_states = dict()
    for key in final_states.keys():
        new_final_states[final_states[key]] = key
    return al, new_final_states


def process(al, final_states, symbols_list, string):
    current_state = 1
    tape = []
    invalid_character = False
    # Para Cada Linha Da String De Entrada
    for line in string:
        empty_line = False
        # Para Cada Token, (Caractere), Na Linha
        for character in line:
            # Se A Linha É Vazia
            if not line.strip("\n"):
                empty_line = True
                continue
            # Se O Token Acabou
            if character == ' ' or character == '\n':
                # If -> Token Possui Caractere Inválido
                if invalid_character:
                    tape.append('ERROR')
                    invalid_character = False
                else:
                    # Para Todos Os Estados Finais
                    for key in final_states.keys():
                        # Se O Estado Atual Pertence A Algum Dos Estados Finais
                        if str(current_state - 1) in str(key).split(','):  # -1 Por Conta Do Index Dos Estados (Coluna)
                            tape.append(final_states[key])
                            break
                current_state = 1
                continue
            # If -> O Token Pertence A Linguagem
            if character in symbols_list:
                current_state = al[current_state][character]
            # Else -> O Token Não Pertence A Linguagem
            else:
                invalid_character = True
        # Se A Linha Não For Vazia (Ignorada)
        if not empty_line:
            tape.append('NEW_LINE')

    return tape
