# Analisador Léxico e Tabela de Símbolos para Português

Este projeto implementa as fases iniciais de um processador de linguagem natural ou compilador simplificado, focando na análise léxica e na construção de uma tabela de símbolos para textos em português.

## Funcionalidades Principais

1.  **Verificação e Limpeza Léxica (`lexical_check`):**
    * Verifica o texto de entrada caractere por caractere contra um conjunto pré-definido de caracteres válidos (letras, dígitos, pontuação, símbolos específicos).
    * Remove caracteres inválidos do texto.
    * Reporta quais caracteres foram removidos e suas posições originais.
    * Passa o texto limpo para a próxima fase.

2.  **Tokenização e Fila de Tokens (`tokenize`):**
    * Utiliza a biblioteca NLTK (`word_tokenize`) para dividir o texto limpo em tokens (palavras e pontuação).
    * Remove stopwords comuns do português (ex: "eu", "o", "de", "para").
    * Retorna uma **Fila de Tokens** (`deque`) contendo os tokens relevantes na ordem em que apareceram (exceto stopwords).

3.  **Tabela de Símbolos (`update_symbol_table`):**
    * Processa a Fila de Tokens para construir e atualizar uma Tabela de Símbolos.
    * **Filtro Semântico:** Ignora tokens que são puramente pontuação ou números, considerando apenas palavras que provavelmente carregam significado.
    * **Lematização (Forma Canônica):** Utiliza a biblioteca spaCy (com o modelo `pt_core_news_sm`) para encontrar o lemma (forma base/dicionário) de cada palavra válida. Isso ajuda a agrupar variações (ex: "compilador", "compiladores" -> "compilador").
    * **Verificação de Similaridade (Levenshtein):** Antes de adicionar um novo lemma à tabela, calcula a distância de Levenshtein entre ele e os lemas já existentes. Se um lemma muito similar (distância <= `similarity_threshold`, padrão 1) já estiver presente, o novo lemma não é adicionado, evitando entradas quasi-duplicadas (ex: "compilador" vs "compiladorez").
    * **Unicidade e Ordenação:** Garante que cada lemma apareça apenas uma vez e mantém a tabela (uma lista Python) ordenada alfabeticamente.

## Conceitos Implementados

* **Análise Léxica:** A primeira fase, que lida com a validação de caracteres e a identificação de unidades básicas (tokens).
* **Fila de Tokens:** Uma estrutura (`deque`) que armazena a sequência de tokens válidos (sem stopwords) para processamento posterior (ex: análise sintática, não implementada aqui).
* **Tabela de Símbolos:** Uma estrutura (lista ordenada) que armazena representações únicas e canônicas (lemas) das palavras semanticamente relevantes encontradas no texto.
* **Lematização vs. Stemming:** Optou-se pela lematização (via spaCy) por produzir formas canônicas mais significativas (palavras reais) do que o stemming (que apenas corta radicais). Isso alinha-se com a ideia de representar conceitos de forma consistente na Tabela de Símbolos.
[nltk](https://medium.com/turing-talks/uma-an%C3%A1lise-de-dom-casmurro-com-nltk-343d72dd47a7).
* **Distância de Levenshtein:** Usada como métrica de similaridade para evitar a inserção de lemas que são provavelmente erros de digitação ou variações muito próximas de lemas já existentes na tabela. [Levenshtein](https://github.com/rapidfuzz/Levenshtein)


### Pipeline spaCy para Lematização

A lematização precisa de contexto gramatical. O spaCy utiliza um pipeline de componentes para isso:
    * **`tok2vec`**: Gera vetores para os tokens.
    * **`tagger`**: Atribui a classe gramatical (POS tag - ex: Verbo, Substantivo). Essencial para o lematizador.
    * **`parser`**: Analisa a estrutura de dependências da frase.
    * **`attribute_ruler` / `lemmatizer`**: Usa regras e as informações do tagger para determinar o lemma correto.

## Dependências

* Python 3.x
* NLTK (`pip install nltk`)
* spaCy (`pip install spacy`)
* Modelo de linguagem spaCy para português (`python -m spacy download pt_core_news_sm`)
* python-Levenshtein (`pip install python-Levenshtein`)

## Configuração e Instalação

1.  **Instale as bibliotecas Python:**
    ```bash
    pip install nltk spacy python-Levenshtein
    ```
2.  **Baixe os recursos NLTK:**
    O script tenta baixar automaticamente (`punkt`, `stopwords`). Se falhar, execute manualmente em um console Python:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    ```
3.  **Baixe o modelo spaCy:**
    O script tenta carregar o modelo. Se não estiver instalado, execute no terminal:
    ```bash
    python -m spacy download pt_core_news_sm
    ```

## Como Usar

1.  Certifique-se de que todas as dependências e modelos estão instalados.
2.  Execute o script Python (contendo as funções `lexical_check`, `tokenize`, `update_symbol_table` e as inicializações).
3.  O script processará as frases de exemplo definidas no final do arquivo e imprimirá:
    * O relatório de limpeza léxica (caracteres inválidos removidos).
    * A Fila de Tokens resultante (após tokenização e remoção de stopwords).
    * O processo de atualização da Tabela de Símbolos (mostrando lematização e comparações de similaridade).
    * A Fila de Tokens final.
    * A Tabela de Símbolos final (lista ordenada de lemas únicos).

```python
# Exemplo de como chamar as funções principais

texto_entrada = "Um compilador compila código, compilando rapidamente!"
fila_tokens = lexical_check(texto_entrada)
tabela_simbolos_inicial = []
tabela_simbolos_final = update_symbol_table(fila_tokens, tabela_simbolos_inicial)

print("--- RESULTADO ---")
print(f"Fila de Tokens: {list(fila_tokens)}")
print(f"Tabela de Símbolos: {tabela_sim
