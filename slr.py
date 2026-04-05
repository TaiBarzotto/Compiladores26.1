def parse(tape):
    # Diferente Do AFD E AL O SRL Funciona Apenas Para Linguagem Abaixo
    #
    # E' -> E
    # E -> E + T | E - T | T
    # T -> T * F | T / F | F
    # F -> ( E ) | id
    #
    # Tabela SlR
    # A Tabela Não Tem Label Para Os Estados (Linhas) Pois Basta Adicionar/Subtrair 1 Do Index Da Matriz
    # S = Stack (Empilha) | R = Reduce (Reduz)
    # $ = NEW_LINE
    slr_table = [
        ['TK_+', 'TK_-', 'TK_*', 'TK_/', 'TK_(', 'TK_)', 'TK_NUMBER', 'NEW_LINE', 'E', 'T', 'F'],
        ['', '', '', '', 'S,4', '', 'S,5', '', '1', '2', '3'],     # Estado 0  (Linha 1)
        ['S,6', 'S,7', '', '', '', '', '', 'ACEITA', '', '', ''],        # Estado 1  (Linha 2)
        ['R,3', 'R,3', 'S,8', 'S,9', '', 'R,3', '', 'R,3', '', '', ''],  # Estado 2  (Linha 3)
        ['R,6', 'R,6', 'R,6', 'R,6', '', 'R,6', '', 'R,6', '', '', ''],  # Estado 3  (Linha 4)
        ['', '', '', '', 'S,4', '', 'S,5', '', '10', '2', '3'],    # Estado 4  (Linha 5)
        ['R,8', 'R,8', 'R,8', 'R,8', '', 'R,8', '', 'R,8', '', '', ''],  # Estado 5  (Linha 6)
        ['', '', '', '', 'S,4', '', 'S,5', '', '', '11', '3'],       # Estado 6  (Linha 7)
        ['', '', '', '', 'S,4', '', 'S,5', '', '', '12', '3'],       # Estado 7  (Linha 8)
        ['', '', '', '', 'S,4', '', 'S,5', '', '', '', '13'],          # Estado 8  (Linha 9)
        ['', '', '', '', 'S,4', '', 'S,5', '', '', '', '14'],          # Estado 9  (Linha 10)
        ['S,6', 'S,7', '', '', '', 'S,15', '', '', '', '', ''],          # Estado 10 (Linha 11)
        ['R,1', 'R,1', 'S,8', 'S,9', '', 'R,1', '', 'R,1', '', '', ''],  # Estado 11 (Linha 12)
        ['R,2', 'R,2', 'S,8', 'S,9', '', 'R,2', '', 'R,2', '', '', ''],  # Estado 12 (Linha 13)
        ['R,4', 'R,4', 'R,4', 'R,4', '', 'R,4', '', 'R,4', '', '', ''],  # Estado 13 (Linha 14)
        ['R,5', 'R,5', 'R,5', 'R,5', '', 'R,5', '', 'R,5', '', '', ''],  # Estado 14 (Linha 15)
        ['R,7', 'R,7', 'R,7', 'R,7', '', 'R,7', '', 'R,7', '', '', ''],  # Estado 15 (Linha 16)
    ]
    # Produções (Número Da Produção -> "Nome" Da Produção) (Usado Para Empilhar)
    slr_productions = {
        '0': 'E',  # E' -> E
        '1': 'E',  # E -> E + T
        '2': 'E',  # E -> E - T
        '3': 'E',  # E -> T
        '4': 'T',  # T -> T * F
        '5': 'T',  # T -> T / F
        '6': 'T',  # T -> F
        '7': 'F',  # F -> ( E )
        '8': 'F',  # F -> id
    }
    # Tamanho Das Produções (Número Da Produção -> Tamanho (2 * "Tokens"))
    slr_sizes = {
        '0': 2,  # E' -> E
        '1': 6,  # E -> E + T
        '2': 6,  # E -> E - T
        '3': 2,  # E -> T
        '4': 6,  # T -> T * F
        '5': 6,  # T -> T / F
        '6': 2,  # T -> F
        '7': 6,  # F -> ( E )
        '8': 2,  # F -> id
    }
    # Dicionário Para Facilitar O Uso Da Tabela (Símbolo -> Coluna)
    slr_dict = {
        'TK_+': 0,
        'TK_-': 1,
        'TK_*': 2,
        'TK_/': 3,
        'TK_(': 4,
        'TK_)': 5,
        'TK_NUMBER': 6,
        'NEW_LINE': 7,
        'E': 8,
        'T': 9,
        'F': 10
    }
    # Resultado (ACEITA/REJEITA)
    result = []
    # Estado Inicial Da Pilha
    stack = [0]
    # Roda ENquanto Houver Itens Na Fita
    while tape:
        # Usa O Topo Da Pilha E Início Da Fita Para Encontrar A Ação Correspondente Na Tabela
        # stack[-1] + 1 -> Topo Da Pilha (Estado) + 1 Por Conta Do Index (Ler Comentário Da slr_table)
        # tape[0] -> Início Da Fita
        try:
            action = slr_table[stack[-1] + 1][slr_dict[tape[0]]]
        except KeyError:
            action = None

        if action:
            # Verifica Se A Fita Foi Aceita
            if action == 'ACEITA':
                result.append(action)
                stack = [0]
                tape.pop(0)
                continue
            # Separa A Ação Do Estado (R,11 -> [R, 11])
            action = action.split(',')
            # Verifica A Ação
            if action[0] == 'S':  # Empilha
                # Empilha O Símbolo Da Fita
                stack.append(tape[0])
                tape.pop(0)
                # Empilha O Estado Na Fita
                stack.append(int(action[1]))
            elif action[0] == 'R':  # Reduz
                production = slr_productions[action[1]]
                # Remove Da Pilha (Tamanho Da Produção)
                for i in range(slr_sizes[action[1]]):
                    stack.pop(-1)
                # Verifica O Estado Que Irá EMpilhar Baseado Na Produção Reduzida
                state = slr_table[stack[-1] + 1][slr_dict[production]]
                # Empilha A Produção E O Estado
                stack.append(production)
                stack.append(int(state))
            else:
                exit('ERRO: AÇÃO INVÁLIDA NA TABELA SLR!!!')
        else:
            # Ação Inválida, Rejeita A Linha
            result.append('REJEITA')
            stack = [0]
            # Remove Tokens Da Fita Até Chegar Na Próxima Linha
            while tape[0] != 'NEW_LINE':
                tape.pop(0)
            # Remove O Token NEW_LINE
            tape.pop(0)
            continue

    return result
