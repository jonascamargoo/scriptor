import string
from nltk.corpus import stopwords
from collections import deque
import Levenshtein

# Prototipo final do lexico

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


# Devo ignorar o caracter inválido e continuar a análise, ou parar tudo e retornar um erro?
def lexical_check(text: str) -> deque:
    letters = "abcçdefghijklmnopqrstuvwxyzABCÇDEFGHIJKLMNOPQRSTUVWXYZáàéíóúêãâôõÁÀÉÍÓÚÊÃÂÔÕ"
    digits = "0123456789"
    punctuation = ".,;:!?()[]{}\"'`´°"
    specials = "@#$%&*-_+=\\/|<>^~\n\t\r "
    valid_chars = set(letters + digits + punctuation + specials)

    errors = []
    for index, char in enumerate(text):
        if char not in valid_chars:
            error_msg = f"{RED}Erro léxico: caractere inválido '{char}' (código {ord(char)}) na posição {index}{RESET}"
            errors.append(error_msg)

    if errors:
        print(f"{RED}A análise léxica encontrou os seguintes erros:{RESET}")
        for error in errors:
            print(error)
        return deque()
    else:
        print(f"{GREEN}Nenhum erro léxico encontrado.{RESET}")
        return process_tokens(text)  

# https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/ Relativo ao item 3 do trabalho
def find_similar_words(word: str, dictionary: list, max_errors: int = 2) -> list:
    similar_words = []
    for correct_word in dictionary:
        distance = Levenshtein.distance(word.lower(), correct_word.lower())
        if distance <= max_errors:
            similar_words.append(correct_word)
    return similar_words

# def process_tokens(text: str) -> deque:
#     stopwords_pt = get_stopwords_portuguese()
#     text_without_punctuation = remove_punctuation(text)
#     words = text_without_punctuation.split()
#     tokens_queue = deque()
#     symbol_table = [] # Sua tabela de símbolos preliminar - relativo ao item 4 do trabalho

#     for word in words:
#         word_lower = word.lower()
#         if word_lower not in stopwords_pt:
#             # candidate words = find_similar_words(word, your_dictionary)
#             # if candidate words:
#             #     # Decida qual sugestão usar (a primeira? a mais similar?)
#             #     word_to_add = candidate words[0]
#             #     tokens_queue.append(word_to_add)
#             #     symbol_table.append(word_to_add)
#             # else:
#             tokens_queue.append(word)
#             symbol_table.append(word)

#     print("\n✅ Tabela de Símbolos Preliminar:", symbol_table)
#     return tokens_queue

def process_tokens(text: str) -> deque:
    stopwords_pt = get_stopwords_portuguese()
    text_without_punctuation = remove_punctuation(text)
    words = text_without_punctuation.split()
    tokens_queue = deque()
    symbol_table = []  # Tabela de símbolos preliminar

    for word in words:
        word_lower = word.lower()
        if word_lower not in stopwords_pt:
            similar = find_similar_words(word_lower, list(stopwords_pt), max_errors=2)
            if similar:
                print(f"{RED}Aviso: '{word}' se parece com a stopword '{similar[0]}' e será ignorada.{RESET}")
                continue  # Ignora a palavra parecida com stopword
            tokens_queue.append(word)
            symbol_table.append(word)

    print("\n✅ Tabela de Símbolos Preliminar:", symbol_table)
    print(f"{GREEN}Tabela de Símbolos preliminar: caractere inválido '{char}' (código {ord(char)}) na posição {index}{RESET}"errors.append(error_msg))
    return tokens_queue


def remove_punctuation(text: str) -> str: return text.translate(str.maketrans('', '', string.punctuation))
    
def get_stopwords_portuguese() -> set: return set(stopwords.words('portuguese'))


# Test
if __name__ == "__main__":
    user_input = input("Enter a text for lexical analysis: ")
    tokens = lexical_check(user_input)

    if tokens:
        print("➡️ Fila de Tokens:", list(tokens))