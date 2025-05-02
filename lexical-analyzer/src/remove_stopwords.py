# https://www.nltk.org/howto/portuguese_en.html
# https://medium.com/turing-talks/uma-an%C3%A1lise-de-dom-casmurro-com-nltk-343d72dd47a7

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def tokenize(text: str) -> list:
    nltk.download('punkt')
    stopwords_pt = set(stopwords.words('portuguese'))
    words = word_tokenize(text, language='portuguese')
    return [w for w in words if w.lower() not in stopwords_pt]

['Olá', ',', 'criando', 'analisador', 'léxico', 'trabalho', 'compiladores', '!']