# https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/

import Levenshtein

def find_similar_words(word, dictionary, max_errors=2):
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

# Example usage
dictionary = ["exception", "excecao", "excessão", "esceção"]
typed_word = "Esceção"
result = find_similar_words(typed_word, dictionary)

print(f"Words similar to '{typed_word}': {result}")


# Levenshtein.distance(): Calcula a distância de Levenshtein entre a palavra digitada e as palavras do dicionário. A distância de Levenshtein é o número mínimo de edições (inserção, exclusão ou substituição de um único caractere) necessárias para transformar uma string na outra.

# find_similar_words(): A função recebe a palavra digitada, o dicionário de palavras possíveis e um parâmetro que define o número máximo de erros permitidos. Ela retorna todas as palavras do dicionário que possuem uma distância de Levenshtein menor ou igual ao número de erros permitido.

# Essa será a ponte entre a tabela inicial de palavras exceto stopwords e a fila de tokens. As palavras consideradas similares irão para a fila

