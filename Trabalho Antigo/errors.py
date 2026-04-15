import numpy


def generate(afd, final_states):
    # Obtem O Valor Do Ultimo Estado QUe Será Criado (Ultimo Estado Da Matriz + 1)
    last = int(afd[afd.shape[0] - 1, 0].replace('@', '')) + 1
    # Atualiza Dicionário
    final_states['ERROR'] = last
    # Cria Uma Nova Linha Começando Pelo Estado (Index Da Linha)
    row = [f'@{last}']
    # Preenche O Restante Da Linha Com Símbolos De Erro
    for i in range(afd.shape[1] - 1):
        row.append('Ø')
    # Atualiza A Matriz Com A Nova Linha
    afd = numpy.append(afd, numpy.matrix(row), axis=0)
    #
    # Substitui Todas As Celúlas Da Matriz Com "Ø" Para O Estado De Erro
    afd[afd == 'Ø'] = last
    return afd, final_states
