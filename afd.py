import numpy


def generate(afnd, matrix, symbol_position, final_states):
    # Coloca A Primeira Linha Matriz (A Matriz Começa Apenas Com O Cabeçalho)
    matrix = numpy.append(matrix, numpy.matrix(afnd[1]), axis=0)
    # Parâmetros Iniciais E De Controle
    transitions_handled = ['0']
    new_transitions = dict()
    width = len(symbol_position) + 1
    total_rows, current_row = 1, 1
    # Loop Principal (Determinização)
    while True:
        first = True
        # Para Cada Trasição Na Linha
        for index, value in numpy.ndenumerate(matrix[current_row]):
            # Ignora O Primeiro Símbolo (Regra)
            if first:
                first = False
                continue
            # Ignora Transições Vazias
            if value == 'Ø':
                continue
            # Se A Trasição Não Foi Tratada
            if value not in transitions_handled:
                # If -> Há Indeterminismo
                if '|' in value:
                    # Marca Transição Como Tratada
                    transitions_handled.append(value)
                    transitions = value.split('|')
                    rows = []
                    # Para Cada Possivel Transição
                    for transition in transitions:
                        # Exemplo (Ex.): X|Y
                        new_transitions[transition] = value  # Ex.: Atualiza O Dicionário: {X: X|Y, Y: X|Y}
                        rows.append(numpy.matrix(afnd[int(transition) + 1]))  # Ex.: Adiciona A Linha X E Y Na Lista
                    # Cria Uma Nova Linha Iniciando Com A Transição Indeterminista (X|Y|...)
                    # Essa Linha Será Chamada De "Nova Linha" Nos Comentários
                    row = [value]
                    # Preenche O Restante Da Linha Com Símbolos De Erro
                    for i in range(width - 1):
                        row.append('Ø')
                    # Parâmetros De Controle
                    is_final_state = False
                    _final_states = []  # Armazena Quais Estados Do Indeterminismo (Linhas) São Finais
                    # Para Cada Linha Do Indeterminismo (Exemplo: Para X|Y -> Linha X E Linha Y)
                    for _row in rows:
                        first = True
                        # Para Cada Trasição Na Linha Do Indeterminismo
                        for index_, value_ in numpy.ndenumerate(_row):
                            # Se É A Primeira Célula, (Index Das Linhas)
                            if first:
                                # Se É Estado Final
                                if value_[0] == '@':
                                    _final_states.append(value_[1:])
                                    is_final_state = True
                                first = False
                                continue
                            # Se A Trasição Não For Inválida (Erro)
                            if value_ != 'Ø':
                                # If -> A Nova Linha Não Possui Transições Por Esse Símbolo
                                if row[index_[1]] == 'Ø':
                                    row[index_[1]] = value_
                                # Else -> A Nova Linha Já Possui Transições Por Esse Símbolo
                                else:
                                    row[index_[1]] = f'{row[index_[1]]}|{value_}'
                    # Se É Estado Final
                    if is_final_state:
                        # Atualiza Dicionário De Estados Finais
                        # Para Cada Estado Final Das Linhas Da Trasição Indeterminística
                        for _final_state in _final_states:
                            # Para Cada Estado Final (Label)
                            for key in final_states.keys():
                                # Se A Label Corresponde Ao Estado Final Da Linha Da Trasição Indeterminística
                                if _final_state in final_states[key].split(','):
                                    final_states[key] = f'{final_states[key]},{row[0]}'
                        row[0] = f'@{row[0]}'
                    # Coloca A Nova Linha, (X|Y|...), Na Matriz E Atualiza O Total De Linhas Da Matriz
                    matrix = numpy.append(matrix, numpy.matrix(row), axis=0)
                    total_rows += 1
                # Else -> Não Há Indeterminismo
                else:
                    # If -> A Transição Não Foi Tratada
                    if value not in new_transitions.keys():
                        # Marca Transição Como Tratada
                        transitions_handled.append(value)
                        # Coloca A Linha Da Transição Na Matriz
                        matrix = numpy.append(matrix, numpy.matrix(afnd[int(value) + 1]), axis=0)
                        # Atualiza O Total De Linhas Da Matriz
                        total_rows += 1
                    # Else -> A Transição Já Foi Tratada
                    else:
                        # Atualiza A Matriz
                        matrix[current_row, index[1]] = new_transitions[value]
        # Se Toda A Matriz Foi Percorrida (Determinização Completa)
        if current_row >= total_rows:
            break
        current_row += 1
    # Refaz O Index De Estados, (Linhas), Da Matriz
    # Para Cada Linha Da Matriz
    for row in range(matrix.shape[0] - 1):
        # If -> Não É Estado Final
        if '@' not in matrix[row + 1, 0]:
            # Substitui Todas As Transições Da Matriz Com Index Antigo Para O Index Novo
            matrix[matrix == matrix[row + 1, 0]] = f'#{row}'
        # Else -> É Estado Final
        else:
            state = matrix[row + 1, 0]
            # Substitui Todas As Transições Da Matriz Com Index Antigo Para O Index Novo
            matrix[matrix == str(state).replace('@', '')] = f'#{row}'
            # Substitui O Nome De Estado Na Matriz
            matrix[row + 1, 0] = f'@#{row}'
            # Atualiza Estados Finais
            # Para Cada Label No Dicionário De Estados Finais
            for key in final_states.keys():
                # Se A Label Corresponde Ao Estado
                if str(state).replace('@', '') in final_states[key].split(','):
                    # Separa Os Estados Finais
                    __final_states = final_states[key].split(',')
                    # Percorre Os Estados Finais Separados (Via Contador)
                    for counter in range(len(__final_states)):
                        # Se É O Estado Que Precisa Ser Substituido
                        if str(state).replace('@', '') == __final_states[counter]:
                            __final_states[counter] = f'#{row}'
                    # Atualiza Dicionário
                    final_states[key] = ','.join(__final_states)
    # Remove Símbolos De Controle Criados Durante A Atualização Do Index De Estados, (Linhas), Da Matriz
    # Para Cada Célula Da Matriz
    for index, value in numpy.ndenumerate(matrix):
        # Se Houver "#" (Símbolo De Controle)
        if '#' in value:
            matrix[index] = str(value).replace('#', '')
    # Para Cada Label No Dicionário De Estados Finais
    for key in final_states.keys():
        # Remove Símbolos De Controle (#)
        final_states[key] = final_states[key].replace('#', '')
    return matrix, final_states
