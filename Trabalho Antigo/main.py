# Mateus Azor, Daniel Salvini
#
# Símbolos De Controle
# '[' Representa O Inicio Do Nome De Um Estado
# ']' Representa O Final Do Nome De Um Estado
# '|' Representa A Divisão Entre Transições De Um Estado
# '&' Representa ε
# '#', '@' São Utilizados Na Lógica Do Programa
# Obs.: As Gramáticas Devem Ser Escritas Antes Das Palavras
# Obs.: GRs Devem Possuir Pelo Menos Dois Estados E Seguir O Padrão De Escrita Dos Exemplos À Seguir
# Obs.: Além Disso GRs Terminando Com Símbolos Terminais Ao Invés De & (Exemplo: [S]|a|b) Não São Suportadas
#
# Obs.: Os Arquivos De Entrada Devem Terminar Com Uma Linha Em Branco (\n)
#
# [ARITHMETIC_OPERATORS] <- Label (Nome Dos Tokens Identificados)
# [S]|+[A]|-[A]|*[A]|/[A] <- [Nome Da Regra]|PRODUÇÃO[Estado]|PRODUÇÃO[Estado]|...
# [A]|& <- Toda GR Deve Possuir & (Para Construção Do Estado Final)
#
# [ASSIGNMENT_COMPARISON_OPERATORS]
# [S]|=[A]|>[A]|<[A]
# [A]|=[B]|&
# [B]|&
#
# [VARIABLES]
# [S]|a[A]|e[A]|i[A]|o[A]|u[A]
# [A]|a[A]|e[A]|i[A]|o[A]|u[A]|&

import pandas

import header as _header
import afnd as _afnd
import afd as _afd
import errors as _errors
import al as _al
import slr as _slr

# Cria O Cabeçalho (Lista Com Todos Os Tokens)
header, symbol_position, symbols_list = _header.generate(open('input_language.txt', 'r').readlines())
# Cria O Autômato Finito Não Determinístico
afnd, final_states = _afnd.generate(header, symbol_position)
# Cria O Autômato Finito Determinístico
afd, final_states = _afd.generate(afnd, header, symbol_position, final_states)
# Cria O Estado De Erro E Suas Transições
afd, final_states = _errors.generate(afd, final_states)
# Gera Um Arquivo .csv Do AFD & Imprime No Console
print('\n', 'AUTÔMATO FINITO DETERMINÍSTICO')
pandas.DataFrame(afd).to_csv("afd.csv")
print('\n', afd, '\n\n ESTADOS FINAIS\n\n', final_states)
# Cria O Analisador Léxico
al, final_states = _al.generate(afd, final_states)
# Interpreta A String De Entrada
tape = _al.process(al, final_states, symbols_list, open('input_string.txt', 'r').readlines())
# Gera Um Arquivo .txt Da Fita De Saida & Imprime No Console
print('\n', 'FITA DE SAÍDA')
open('output_tape.txt', 'w').write(str(tape))
print('\n', tape)
slr_list = _slr.parse(tape)
print('\n', 'ANÁLISE SLR')
print('\n', slr_list)
