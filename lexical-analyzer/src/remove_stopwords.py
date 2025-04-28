# # https://www.nltk.org/howto/portuguese_en.html
# # https://medium.com/turing-talks/uma-an%C3%A1lise-de-dom-casmurro-com-nltk-343d72dd47a7

# # import nltk
# import string
# # from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords

# # retorna tabela de simbolos preliminar
# # def remove_stopwords(text: str) -> list:
# #     nltk.download('punkt')
# #     stopwords_pt = set(stopwords.words('portuguese'))
# #     words = word_tokenize(text, language='portuguese')
# #     return [w for w in words if w.lower() not in stopwords_pt and w.isalpha()]

# # print(remove_stopwords("Olá, eu estou criando um analisador léxico para o trabalho de compiladores!"))


# def remove_stopwords(text: str) -> list:
#     stopwords_pt = set(stopwords.words('portuguese'))
#     translator = str.maketrans('', '', string.punctuation)
#     text = text.translate(translator) # remover pontuação
#     words = text.split()
#     return [w for w in words if w.lower() not in stopwords_pt]


# # test_cases = [
# #     "Eu gosto de programar em Python.",
# #     "Olá!!! Tudo bem? Espero que sim.",
# #     "A Máquina de Café está funcionando perfeitamente.",
# #     "o a de em para com sem",
# #     "Hoje é dia 27 de abril de 2025.",
# #     "Compiladores, Analisadores-Léxicos... Geradores de Código!",
# #     "Este é um teste simples para remover stopwords",
# #     "",
# #     "Pythonéumaótimalinguagem"
# # ]

# # for i, text in enumerate(test_cases, 1):
# #     print(f"Teste {i}: {remove_stopwords(text)}")


