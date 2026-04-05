import numpy


def generate(matrix, symbol_position):
    # Le O Arquivo De Input
    file = open('input_language.txt', 'r')
    lines = file.readlines()
    file.close()
    # Parâmetros Iniciais (Geral)
    final_states = dict()
    width = len(symbol_position) + 1  # +1 Por Conta Do Símbolo Inicial Da Matriz (δ)
    next_transition = 0
    # Parâmetros Iniciais (Tratamento De Gramáticas)
    rules_rows = dict()
    new_grammar = True
    grammar_label = True
    label = ''
    last = 0
    # Cria Uma Nova Linha Iniciando Com Número Da Transição
    row = [next_transition]
    # Preenche O Restante Da Linha Com Símbolos De Erro
    for i in range(width - 1):
        row.append('Ø')
    # Atualiza A Próxima Transição & Adiciona A Linha Na Matriz
    next_transition += 1
    matrix = numpy.append(matrix, numpy.matrix(row), axis=0)
    # Loop Principal (Linhas)
    for line in lines:
        # Remove Caracteres Inúteis
        line = line.strip()
        # Detecta Linhas Vazias
        if not line:
            new_grammar = True  # Pode Haver Uma Próxima Gramática
            grammar_label = True  # Pode Haver Uma Próxima Gramática
            rules_rows = dict()  # Limpa O Dicionário De {Regra -> Linha} Para Próxima Gramática
            continue
        # If -> Palavra
        if line[0] != '[':
            label = f'TK_{line.strip().upper()}'
            # Tratamento Do Primeiro Símbolo
            first_simbol = line[0]
            # If -> Não Existe Nenhuma Transição Pelo Símbolo
            if matrix[1, symbol_position[first_simbol]] == 'Ø':
                matrix[1, symbol_position[first_simbol]] = next_transition
            # Else -> Já Existem Transições Pelo Símbolo
            else:
                matrix[1, symbol_position[first_simbol]] = \
                    f'{matrix[1, symbol_position[first_simbol]]}|{next_transition}'
            # Obs.: matrix[1, ... Se Refere A Primeira Linha De Transições (Linha 0 -> Cabeçalho)
            # Tratamento Do Restante Dos Símbolos
            for symbol in line[1:]:
                # Cria Uma Nova Linha Iniciando Com Número Da Transição
                row = [next_transition]
                # Preenche A Linha Com Símbolos De Erro Até A Posição Do Símbolo
                for i in range(symbol_position[symbol] - 1):
                    row.append('Ø')
                # Preenche A Posição Do Símbolo Com A Transição
                row.append(next_transition + 1)
                # Preenche O Restante Da Linha Com Símbolos De Erro
                for i in range(width - len(row)):
                    row.append('Ø')
                # Atualiza A Próxima Transição & Adiciona A Linha Na Matriz
                next_transition += 1
                matrix = numpy.append(matrix, numpy.matrix(row), axis=0)
            # Cria Uma Nova Linha, (Estado Final), Iniciando Com Número Da Transição
            row = [f'@{next_transition}']
            # Preenche O Restante Da Linha Com Símbolos De Erro
            for i in range(width - 1):
                row.append('Ø')
            # Atualiza Estados Finais, Atualiza A Próxima Transição, Adiciona A Linha Na Matriz
            final_states[label] = str(next_transition)
            next_transition += 1
            matrix = numpy.append(matrix, numpy.matrix(row), axis=0)
        # Else -> Gramática
        else:
            # Obtem A Label Da Gramática
            if grammar_label:
                label = line[1:-1]
                final_states[label] = '-1'
                grammar_label = False
                continue
            # Parâmetros Iniciais
            first = True  # Nome Da Regra
            line = line.split('|')
            origin_state = None
            for transition in line:
                # Caso Seja Uma Nova Gramática (Por Consequência O Nome Da Regra)
                if new_grammar:
                    origin_state = transition[1:-1]  # Nome Da Regra
                    last = transition[1:-1]
                    rules_rows[origin_state] = 0  # Posição Da Regra
                    new_grammar = False
                    first = False
                    continue
                # Caso Seja O Nome Da Regra
                if first:
                    origin_state = transition[1:-1]
                    first = False
                    continue
                # If -> Produção & (Estado É Final)
                if transition == '&':
                    if final_states[label] == '-1':
                        final_states[label] = str(rules_rows[origin_state])
                    else:
                        final_states[label] = f'{final_states[label]},{rules_rows[origin_state]}'
                    # Adiciona @, (Símbolo De Estado Final), Na Matriz
                    matrix[rules_rows[origin_state] + 1, 0] = f'@{matrix[rules_rows[origin_state] + 1, 0]}'
                    # Obs.: +1 Por Conta Do Cabeçalho Da Matriz
                # Else -> Outras Produções
                else:
                    # Separa Não Terminais De Terminais
                    transition = transition.split('[')
                    # Caso Regra Não Possua Uma Linha Correspondente Na Matriz
                    if transition[1][:-1] not in rules_rows.keys():
                        last = transition[1][:-1]
                        # Caso A Próxima Linha Já Esteja Sendo Utilizada
                        if next_transition in rules_rows.values():
                            next_transition += 1
                        # Atualiza O Dicionario De {Regra -> Linha}
                        rules_rows[transition[1][:-1]] = next_transition
                        # Cria Uma Nova Linha Iniciando Com Número Da Transição
                        row = [next_transition]
                        # Preenche O Restante Da Linha Com Símbolos De Erro
                        for i in range(width - 1):
                            row.append('Ø')
                        # Atualiza A Próxima Transição & Adiciona A Linha Na Matriz
                        matrix = numpy.append(matrix, numpy.matrix(row), axis=0)
                        next_transition += 1
                    # If -> Não Existe Nenhuma Transição Pelo Símbolo
                    if matrix[rules_rows[origin_state] + 1, symbol_position[transition[0]]] == 'Ø':
                        matrix[rules_rows[origin_state] + 1, symbol_position[transition[0]]] = \
                            rules_rows[transition[1][:-1]]
                    # Else -> Já Existem Transições Pelo Símbolo
                    else:
                        matrix[rules_rows[origin_state] + 1, symbol_position[transition[0]]] = \
                            f'''{matrix[rules_rows[origin_state] + 1, symbol_position[transition[0]]]}
                            |{rules_rows[transition[1][:-1]]}'''
    return matrix, final_states
