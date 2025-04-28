# https://www.nltk.org/howto/portuguese_en.html
# https://medium.com/turing-talks/uma-an%C3%A1lise-de-dom-casmurro-com-nltk-343d72dd47a7

import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords

# Baixando o necessário
nltk.download('stopwords')

def tokenize(text: str) -> list: return wordpunct_tokenize(text.lower())
    # Tokeniza o texto (quebra por palavras e pontuação)
    
def remove_stopwords(text: str) -> list:
    """
    Remove stopwords e pontuação.
    Retorna uma lista de palavras relevantes.
    """
    # Carrega a lista de stopwords em português
    stopwords_pt = set(stopwords.words('portuguese'))
    
    # Tokeniza o texto (quebra por palavras e pontuação)
    tokens = tokenize(text)

    # Filtra: apenas palavras alfanuméricas que não são stopwords
    return [t for t in tokens if t.isalnum() and t not in stopwords_pt]
    

# Teste rápido
# if __name__ == "__main__":
#     texto_exemplo = "Olá, eu estou criando um analisador léxico para o trabalho de compiladores!"
#     resultado = remove_stopwords(texto_exemplo)
#     print("Resultado:", resultado)