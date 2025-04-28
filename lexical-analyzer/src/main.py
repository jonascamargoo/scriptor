import string
from nltk.corpus import stopwords
from collections import deque
import Levenshtein

# Prototipo final do lexico

def lexical_check(text: str):
    print("🔍 Iniciando a análise léxica... \t se os caracteres fazem parte do alfabeto.\n") #substituir por range
    letters = "abcçdefghijklmnopqrstuvwxyzABCÇDEFGHIJKLMNOPQRSTUVWXYZáàéíóúêãâôõÁÀÉÍÓÚÊÃÂÔÕ"
    digits = "0123456789"
    punctuation = ".,;:!?()[]{}\"'`´°"
    specials = "@#$%&*-_+=\\/|<>^~\n\t\r "
    valid_chars = set(letters + digits + punctuation + specials)

    errors = []
    for index, char in enumerate(text):
        if char not in valid_chars:
            error_msg = f"❌ Erro léxico: lexema inválido '{char}' (code {ord(char)}) at position {index}"
            errors.append(error_msg)

    if errors:
        print("Lexical analysis found the following errors:")
        for error in errors:
            print(error)
        return deque() # Retorna uma fila vazia em caso de erros léxicos
    else:
        print("✅ Todos os lexemas foram validados e aprovados.")
        return process_tokens(text)   

# https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/ Relativo ao item 3 do trabalho
def find_similar_words(word: str, dictionary: list, max_errors: int = 2) -> list:
    """
    Returns words from the dictionary that are similar to the input word with a maximum of 'max_errors' 
    characters of difference based on Levenshtein distance.

    :param word: The word to be checked.
    :param dictionary: A list of possible words.
    :param max_errors: The maximum number of allowed character differences (Levenshtein distance).
    :return: A list of similar words.
    """
    similar_words = []
    for correct_word in dictionary:
        distance = Levenshtein.distance(word.lower(), correct_word.lower())
        if distance <= max_errors:
            similar_words.append(correct_word)
    return similar_words

def process_tokens(text: str) -> deque:
    stopwords_pt = get_stopwords_portuguese()
    text_without_punctuation = remove_punctuation(text)
    words = text_without_punctuation.split()
    tokens_queue = deque()
    symbol_table = [] # Sua tabela de símbolos preliminar - relativo ao item 4 do trabalho

    for word in words:
        word_lower = word.lower()
        if word_lower not in stopwords_pt:
            # candidate words = find_similar_words(word, your_dictionary)
            # if candidate words:
            #     # Decida qual sugestão usar (a primeira? a mais similar?)
            #     word_to_add = candidate words[0]
            #     tokens_queue.append(word_to_add)
            #     symbol_table.append(word_to_add)
            # else:
            tokens_queue.append(word)
            symbol_table.append(word)

    print("\n✅ Tabela de Símbolos Preliminar:", symbol_table)
    return tokens_queue

def remove_punctuation(text: str) -> str: return text.translate(str.maketrans('', '', string.punctuation))
    
def get_stopwords_portuguese() -> set: return set(stopwords.words('portuguese'))


# Test
if __name__ == "__main__":
    user_input = input("Enter a text for lexical analysis: ")
    tokens = lexical_check(user_input)

    if tokens:
        print("➡️ Fila de Tokens:", list(tokens))