from collections import deque
import string
import Levenshtein
from config import GREEN, BLUE, RESET


def get_tokens_for_parser(doc, grammar_keywords: set) -> deque:
    """
    Extrai tokens de um objeto Doc do spaCy para alimentar o analisador sintático.
    - Remove pontuação e stopwords, mas preserva qualquer token que seja
      uma palavra-chave da gramática (incluindo pontuação como '?').
    """
    token_list = [
        token.text for token in doc
        if token.lower_ in grammar_keywords or (not token.is_stop and not token.is_punct)
    ]
    
    print(f"Tokens para o parser (após filtro spaCy): {token_list}")
    return deque(token_list)


def update_symbol_table(doc, current_symbol_table: list, similarity_threshold: int = 1) -> list:
    """
    Atualiza a tabela de símbolos usando lemas de um objeto Doc do spaCy.
    """
    print(f"\n{BLUE}--- Atualizando Tabela de Símbolos (com Lematização spaCy) ---{RESET}")
    
    lemmas_to_process = set()
    for token in doc:
        # Considera apenas palavras com letras, ignorando números, pontuações e stopwords
        if token.is_alpha and not token.is_stop:
            lemmas_to_process.add(token.lemma_.lower())

    for lemma in sorted(list(lemmas_to_process)):
        is_similar_found = False
        most_similar_word = None
        min_distance = float('inf')

        for existing_lemma in current_symbol_table:
            distance = Levenshtein.distance(lemma, existing_lemma)
            if distance <= similarity_threshold:
                if distance < min_distance:
                    min_distance = distance
                    most_similar_word = existing_lemma
                is_similar_found = True
                break
        
        if is_similar_found:
            print(f"   Ignorando: Lemma '{lemma}' é similar a '{most_similar_word}' já existente.")
        elif lemma not in current_symbol_table:
            print(f"   {GREEN}Adicionando lemma '{lemma}' à Tabela de Símbolos.{RESET}")
            current_symbol_table.append(lemma)
            current_symbol_table.sort()

    print(f"\n{BLUE}--- Tabela de Símbolos Finalizada ---{RESET}")
    print(f"Tabela atual: {current_symbol_table}")
    return current_symbol_table


# Entrada de Texto Bruto: "Qual documento tem o título 'Relatório'?"
#            |
#            V
# [ main.py: doc = nlp(user_input) ] -> Cria o objeto Doc com todos os dados linguísticos
#            |
#            +-------------------------------------------------------------+
#            |                                                             |
#            V                                                             V
# [ get_tokens_for_parser(doc) ]                            [ update_symbol_table(doc) ]
#  |                                                         |
#  V                                                         V
# Filtra tokens:                                            Filtra e lematiza:
#  - Remove pontuação '?'                                    - 'documento' -> 'documento'
#  - Remove stopwords 'o'                                    - 'tem' (verbo, stopword) -> IGNORA
#  - Mantém keywords 'qual', 'documento'                     - 'título' -> 'título'
#  - Mantém outras palavras 'tem', 'título', 'Relatório'     - 'Relatório' -> 'relatório'
#  |                                                         |
#  V                                                         V
# Saída para o Parser:                                      Atualiza a Tabela de Símbolos:
#  deque(['Qual', 'documento', 'tem', 'título', 'Relatório'])  - Adiciona 'documento', 'título', 'relatório' se forem novos