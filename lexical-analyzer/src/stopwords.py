# https://www.nltk.org/howto/portuguese_en.html
# https://medium.com/turing-talks/uma-an%C3%A1lise-de-dom-casmurro-com-nltk-343d72dd47a7


from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

# Texto de exemplo
texto = "O amor da glória era a coisa mais verdadeiramente humana que há no homem."

# Tokenização
# words = word_tokenize(texto, language='portuguese')

# Carregar stopwords do português
stopwords_pt = set(stopwords.words('portuguese'))

# Filtrar palavras que não são stopwords
filtered_words = [word for word in words if word.lower() not in stopwords_pt]

print("Texto original:")
print(words)
print(texto)
print("\nTexto sem stopwords:")
print(filtered_words)


