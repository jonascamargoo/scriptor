from collections import deque
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# from nltk.stem import RSLPStemmer
import spacy
import string
import sys
import Levenshtein

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def download_nltk_resources():
    resources = {
        'tokenizers/punkt': 'punkt',
        'corpora/stopwords': 'stopwords',
        # 'stemmers/rslp': 'rslp'
    }
    downloaded_all = True
    for resource_path, resource_name in resources.items():
        try:
            nltk.data.find(resource_path)
        except LookupError:
            print(f"{YELLOW}NLTK resource '{resource_name}' not found. Attempting download...{RESET}")
            try:
                nltk.download(resource_name, quiet=True)
                print(f"{GREEN}NLTK resource '{resource_name}' downloaded.{RESET}")
            except Exception as e:
                print(f"{RED}Failed to download NLTK resource '{resource_name}': {e}{RESET}")
                downloaded_all = False
    return downloaded_all

def load_spacy_model(model_name="pt_core_news_sm"):
    """Tenta carregar um modelo spaCy. Se não estiver instalado, instrui como instalar."""
    try:
        # Tenta carregar o modelo pequeno para português
        nlp = spacy.load(model_name)
        print(f"{GREEN}Modelo spaCy '{model_name}' carregado com sucesso.{RESET}")
        return nlp
    except OSError:
        print(f"{RED}Erro: Modelo spaCy '{model_name}' não encontrado.{RESET}")
        print(f"{YELLOW}Por favor, instale o modelo executando: python -m spacy download {model_name}{RESET}")
        return None
    except ImportError:
         print(f"{RED}Erro: Biblioteca spaCy não encontrada. Instale com 'pip install spacy'.{RESET}")
         return None


if not download_nltk_resources():
    print(f"{RED}Essential NLTK resources could not be downloaded. Exiting.{RESET}")
    sys.exit(1)
    
nlp = load_spacy_model()
if nlp is None:
    sys.exit(1)

# temmer = RSLPStemmer()  

# optei por utilizar a lematização (poderia ser o stemmer) pra trabalhar com a ideia de Forma Canônica - algoritmo utilizado por grande processadores de linguagem natural - exemplo google dado pelo professor. Optarei por utilizar o Lematizador posteriormente, já que é mais preciso, porém menos eficiente.

# Para explicar forma canônica. As palavras na tabela de símbolos não devem se repetir. Vamos #supor que eu insira a palavra Compiladorez na tabela. Caso receba um token chamado #Compiladores, ele será validado como similar e a palavra Comiladorez será responsável por #representá-lo na tabela. Para evitar esse tipo de "deselegância" e por questões de #processamento, optei por utilizar o stemmer, deessa forma, em vez de adicionar Compiladorez #inicialmente, será adicionado "compil". O que eu disse para o stemmer, serve para lematização da mesma forma.

# -------------------------------------------------------

# Explicando um pouco para o caso de lematização - componentes da pipeline do spaCy:

# - tok2vec (Token-to-Vector): Cria representações vetoriais (embeddings) para cada token. Esses vetores capturam informações semânticas e contextuais e são frequentemente usados como entrada para os componentes seguintes.

# tagger (Part-of-Speech Tagger): Atribui uma etiqueta de classe gramatical (Part-of-Speech - POS) a cada token. Ele identifica se a palavra é um VERBO, SUBSTANTIVO (NOUN), ADJETIVO (ADJ), ADVÉRBIO (ADV), etc. Este é crucial para a lematização.

# parser (Dependency Parser): Analisa a estrutura gramatical da sentença, identificando as relações de dependência entre as palavras (ex: qual palavra é o sujeito do verbo, qual adjetivo modifica qual substantivo).

# attribute_ruler: Um componente flexível que usa regras (muitas vezes baseadas nas saídas do tagger e parser) para definir atributos dos tokens. É aqui que a lógica de lematização frequentemente reside nos modelos mais recentes do spaCy. Ele pode usar tabelas de consulta e regras para determinar o lemma correto com base na palavra e na sua etiqueta POS.

# -------------------------------------------------------

def lexical_check(text: str) -> deque:
    letters = "abcçdefghijklmnopqrstuvwxyzABCÇDEFGHIJKLMNOPQRSTUVWXYZáàéíóúêãâôõÁÀÉÍÓÚÊÃÂÔÕ"
    digits = "0123456789"
    punctuation = ".,;:!?()[]{}\"'`´°"
    whitespace = " \t\n\r"
    specials = "@#$%&*-_+=\\/|<>^~"
    valid_chars = set(letters + digits + punctuation + whitespace + specials)
    removed_info = []
    cleaned_chars = []
    print(f"{GREEN}--- Verificação de Caracteres Iniciada ---{RESET}")
    print(f"Texto original: '{text}'")
    for index, char in enumerate(text):
        if char in valid_chars:
            cleaned_chars.append(char)
        else:
            removal_msg = (
                f"{YELLOW}Info: Caractere inválido '{char}' (código {ord(char)}) "
                f"na posição original {index} foi removido.{RESET}"
            )
            removed_info.append(removal_msg)
    cleaned_string = "".join(cleaned_chars)
    if removed_info:
        print(f"\n{YELLOW}--- Relatório de Limpeza Léxica ---{RESET}")
        for msg in removed_info:
            print(msg)
        print(f"Texto após limpeza: '{cleaned_string}'")
    else:
        print(f"{GREEN}Nenhum caractere inválido encontrado para remover.{RESET}")
    print(f"\n{GREEN}Prosseguindo para a tokenização (com remoção de stopwords)...{RESET}")
    return tokenize(cleaned_string)

def tokenize(text: str) -> deque:
    if not text:
        print(f"{YELLOW}Info: Texto para tokenizar está vazio.{RESET}")
        return deque()
    try:
        stopwords_pt = set(stopwords.words('portuguese'))
    except LookupError:
         print(f"{RED}Erro fatal: Recurso 'stopwords' do NLTK não encontrado ou corrompido.{RESET}")
         return deque()
    try:
        words = word_tokenize(text, language='portuguese')
    except LookupError:
        print(f"{RED}Erro fatal: Recurso 'punkt' do NLTK não encontrado ou corrompido.{RESET}")
        return deque()
    filtered_tokens_list = [w for w in words if w.lower() not in stopwords_pt]
    print(f"Tokens (Fila) após remoção de stopwords: {filtered_tokens_list}")
    return deque(filtered_tokens_list)

def update_symbol_table(token_queue: deque, current_symbol_table: list, similarity_threshold: int = 1) -> list:
    global nlp
    if nlp is None:
         print(f"{RED}Erro: Modelo spaCy não está carregado. Não é possível lematizar.{RESET}")
         return current_symbol_table 
    print(f"\n{BLUE}--- Atualizando Tabela de Símbolos (com Lematização) ---{RESET}")
    processed_token_count = 0

    for token_text in list(token_queue): 
        processed_token_count += 1
        print(f"\n{processed_token_count}. Token a ser processado: '{token_text}'")

        # 1. Validar se é palavra com semântica
        is_punctuation = all(c in string.punctuation for c in token_text)
        is_number = token_text.isdigit()
        has_letter = any(c.isalpha() for c in token_text)

        if is_punctuation or is_number or not has_letter:
            print(f"   Ignorando: token inválido para a tabela de símbolos.")
            continue

        # 2. Aplicar Lematização com spaCy - inventando moda
        try:
            doc = nlp.make_doc(token_text)
            # aplica o pipeline mínimo necessário
            # nlp.pipe_names: Contém a lista dos nomes dos componentes no pipeline carregado (ex: ['tok2vec', 'tagger', 'parser', 'attribute_ruler', 'lemmatizer', 'ner'])
            for component_name in nlp.pipe_names:
                 if component_name not in doc.user_hooks: # Evita reprocessar
                     doc = nlp.get_pipe(component_name)(doc)

            # pega o lemma do primeiro (e único) token no Doc processado
            # converte para minúsculas após obter o lemma (optei por isso porque não faz sentido diferenciar lemas por maiúsculas/minúsculas na maioria dos casos, eu acho)
            if len(doc) > 0:
                 lemma = doc[0].lemma_.lower()
                 print(f"   Lematização: '{token_text}' -> '{lemma}'")
            else:
                 print(f"   {YELLOW}Aviso: spaCy não produziu tokens para '{token_text}'. Usando forma original em minúsculas.{RESET}")
                 lemma = token_text.lower() # Fallback

        except Exception as e:
            print(f"   {RED}Erro ao aplicar lematização em '{token_text}': {e}{RESET}")
            continue

        # 3. Verificar Similaridade (Levenshtein) com a tabela existente
        is_similar_found = False
        most_similar_word = None
        min_distance = float('inf')

        for existing_lemma in current_symbol_table:
            distance = Levenshtein.distance(lemma, existing_lemma)
            print(f"      Comparando lemma '{lemma}' com '{existing_lemma}' (Tabela): Distância = {distance}")

            if distance <= similarity_threshold:
                is_similar_found = True
                if distance < min_distance:
                    min_distance = distance
                    most_similar_word = existing_lemma
                print(f"      -> Similaridade encontrada com '{existing_lemma}' (Distância: {distance} <= Limiar: {similarity_threshold}).")
                break

        # 4. Adicionar à Tabela se não for similar (e ainda não existir nela)
        if not is_similar_found:
            if lemma not in current_symbol_table:
                print(f"   {GREEN}Adicionando lemma '{lemma}' à Tabela de Símbolos.{RESET}")
                current_symbol_table.append(lemma)
                current_symbol_table.sort()
                print(f"   Tabela atual: {current_symbol_table}")
            else:
                 print(f"   Ignorando: Lemma '{lemma}' já existe na tabela.")
        else:
            print(f"   Ignorando: Lemma '{lemma}' é considerado similar a '{most_similar_word}' já existente na tabela.")

    print(f"\n{BLUE}--- Tabela de Símbolos Finalizada ---{RESET}")
    return current_symbol_table


# Teste
sentence_ok = 'Olá, eu estou criando um analisador léxico para o trabalho de compiladores! Compilador é legal.'
sentence_with_invalid = 'Processo © concluído! ✅ Vamos testar... testando compiladores compilador correndo corre' # Adicionado verbos

print("\n--- Executando Exemplo 1 (OK) ---")
token_queue1 = lexical_check(sentence_ok)
symbol_table1 = []
symbol_table1 = update_symbol_table(token_queue1, symbol_table1, similarity_threshold=1)
print(f"\n{BLUE}Resultado Final Exemplo 1:{RESET}")
print(f"  Fila de Tokens (Deque): {list(token_queue1)}")
print(f"  Tabela de Símbolos (Lista Ordenada de Lemas): {symbol_table1}")

print("\n" + "="*50 + "\n")

print("--- Executando Exemplo 2 (Inválido + Repetições + Verbos) ---")
token_queue2 = lexical_check(sentence_with_invalid)
symbol_table2 = []
symbol_table2 = update_symbol_table(token_queue2, symbol_table2, similarity_threshold=1)
print(f"\n{BLUE}Resultado Final Exemplo 2:{RESET}")
print(f"  Fila de Tokens (Deque): {list(token_queue2)}")
print(f"  Tabela de Símbolos (Lista Ordenada de Lemas): {symbol_table2}")