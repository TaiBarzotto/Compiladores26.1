import numpy


def generate(lines):
    # Cria Os Parâmetros De Controle
    symbol_position = dict()
    symbols = ['δ']
    new_symbol_position = 1
    # Loop Principal (Linhas)
    for line in lines:
        # Remove Caracteres Inúteis
        line = line.strip()
        # Ignora Linhas Vazias
        if not line:
            continue
        # If -> Palavra
        if line[0] != '[':
            for symbol in line:
                if symbol not in symbols:
                    symbols.append(symbol)
                    symbol_position[symbol] = new_symbol_position
                    new_symbol_position += 1
        # Else -> Gramática
        else:
            productions = line.split('|')
            for production in productions[1:]:
                if production != '&':
                    production = production.split('[')
                    if production[0] not in symbols:
                        symbols.append(production[0])
                        symbol_position[production[0]] = new_symbol_position
                        new_symbol_position += 1
    # Cria Um Matriz (Cabealho)
    symbols_matrix = numpy.matrix(symbols)
    return symbols_matrix, symbol_position, symbols
