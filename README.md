# Analisador Léxico com AFD

Este projeto implementa um analisador léxico (lexical analyzer) para uma linguagem simples, utilizando um Autômato Finito Determinístico (AFD) para reconhecimento de tokens. O analisador lê um arquivo de entrada (`entrada.txt`), reconhece tokens definidos em `tokens.txt`, gera uma fita de saída (FITA) e uma Tabela de Símbolos (TS).

## Requisitos

1. **Definição dos tokens da linguagem**: Palavras reservadas, identificadores, símbolos especiais e constantes são definidos no arquivo `tokens.txt`. Exemplos incluem palavras como "se", "sai", "foi" e regras gramaticais para padrões como vogais.

2. **Construção do AFND e determinização**: O código constrói um Autômato Finito Não-Determinístico (AFND) a partir das definições em `tokens.txt` e o converte em um AFD determinístico.

3. **Implementação do algoritmo de mapeamento do AFD para reconhecimento léxico**: O algoritmo percorre o AFD para reconhecer tokens no texto de entrada, tratando transições de estados.

4. **Geração da fita de saída (FITA)**: A FITA é uma lista de identificadores de tokens reconhecidos, no formato `E1 E2 E3... $`, onde `En` representa cada token.

5. **Geração da Tabela de Símbolos (TS)**: A TS contém informações sobre cada token reconhecido, incluindo linha, identificador e status (aceito ou erro).

## Passos Implementados

- **Definir conjunto de tokens**: Tokens são definidos em `tokens.txt` como palavras simples (ex: "se") e regras gramaticais (ex: `<S> ::= a<A> | ...`).

- **Construir AFND e determinizar**: 
  - AFND é construído processando palavras e regras em `tokens.txt`.
  - Determinização converte AFND em AFD usando o algoritmo de determinização.

- **Adicionar estado de erro no AFD**: Um estado de erro `~` é adicionado ao AFD para lidar com símbolos não reconhecidos.

- **Implementar algoritmo de reconhecimento**:
  - **Reconhecimento**: Percorre o AFD para cada caractere da entrada.
  - **Gera TS e FITA**: Adiciona entradas à TS e FITA quando um token é reconhecido.
  - **Separadores**: Trata espaços e quebras de linha como separadores de tokens.
  - **Tratamento de erro**: Se um símbolo não está nos símbolos definidos, vai para estado de erro.
  - **Gera FITA de saída**: FITA é uma lista de tokens reconhecidos.
  - **Gera informações na Tabela de Símbolos**: TS inclui linha, token e status.

## Estrutura do Código

### Arquivos

- `afd.py`: Responsável pela construção do AFD a partir de `tokens.txt`.
- `al.py`: Implementa o analisador léxico, usando o AFD para processar `entrada.txt`.
- `tokens.txt`: Define os tokens e regras gramaticais.
- `entrada.txt`: Arquivo de entrada a ser analisado.

### Detalhes por Arquivo

#### `afd.py`

Este arquivo contém funções para construir e determinizar o autômato.

- **Definição dos tokens (Requisito 1)**: Tokens são lidos de `tokens.txt` em `gerar_afnd()`. Palavras simples são processadas em `processar_palavra()`, regras gramaticais em `processar_gramatica()`.

- **Construção do AFND e determinização (Requisito 2)**: 
  - AFND é construído em `gerar_afnd()` chamando `processar_palavra()` e `processar_gramatica()`.
  - Determinização ocorre em `determinizar_afnd()`, chamada de `gerar_afd()`.

- **Estado de erro (Passo 3)**: Adicionado em `gerar_afd()`: `estado_de_erro = ['~'] * len(simbolos); afd['~'] = estado_de_erro`.

- **Função principal**: `gerar_afd()` retorna o AFD, símbolos, dicionário de símbolos e estados finais.

#### `al.py`

Este arquivo executa o reconhecimento léxico.

- **Algoritmo de reconhecimento (Requisito 3)**: O loop principal percorre cada caractere de `entrada.txt`, atualizando o estado atual baseado no AFD.

- **Geração da FITA (Requisito 4)**: FITA é uma lista (`FITA = []`) que adiciona tokens reconhecidos com `FITA.append(TOKEN)`.

- **Geração da TS (Requisito 5)**: TS é uma lista de dicionários (`TS = []`), cada um com 'token', 'linha', 'status'.

- **Passos detalhados**:
  - **Separadores**: Verifica `if char != ' ' and char != '\n'`, senão processa o token atual.
  - **Tratamento de erro**: Se `char not in simbolos`, vai para estado `~`.
  - **Gera FITA**: Adiciona à FITA quando token é aceito.
  - **Gera TS**: Adiciona entrada à TS com status 'aceito' ou 'ERRO'.

## Como Executar

1. Certifique-se de que `tokens.txt` e `entrada.txt` estão presentes.
2. Execute `python al.py`.
3. O programa imprimirá o AFD, símbolos, etc., e ao final a TS e FITA.

## Exemplo de Saída

Para `entrada.txt` contendo "se sair e foi au xx", a saída incluirá:

- Tabela de Símbolos: Lista de tokens com linha e status.
- FITA: Lista como ['se', 'sair', 'e', 'foi', 'au', 'xx'] (dependendo dos tokens definidos).

## Notas

- O projeto assume que `tokens.txt` define tokens simples e regras para padrões.
- Estados são numerados inicialmente e podem ser renomeados para letras (comentado em `renomear_estados_letras()`).
- Tratamento de erro marca tokens inválidos como 'ERRO' na TS.