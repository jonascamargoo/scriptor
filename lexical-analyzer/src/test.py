from collections import deque
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import sys


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# vou criar um jeito pra rodar essa função uma vez só função https://chatgpt.com/g/g-5XtVuRE8Y-prompt-engineer
def download_nltk_resources():
    resources = {'tokenizers/punkt': 'punkt', 'corpora/stopwords': 'stopwords'}
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

if not download_nltk_resources():
    print(f"{RED}Essential NLTK resources could not be downloaded. Exiting.{RESET}")
    sys.exit(1)

# --- lexical_check MODIFIED ---
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
        # as stopwords tao sendo carregadas aqui no try, pq eh um ponto onde possivelmente daria um erro inicial
        stopwords_pt = set(stopwords.words('portuguese'))
    except LookupError:
         print(f"{RED}Erro fatal: Recurso 'stopwords' do NLTK não encontrado ou corrompido.{RESET}")
         return deque()

    try:
        words = word_tokenize(text, language='portuguese') # o método retorna em lista, não posso criar a fila diretamente aqui, ent converto pra deque depois
    except LookupError:
        print(f"{RED}Erro fatal: Recurso 'punkt' do NLTK não encontrado ou corrompido.{RESET}")
        return deque()

    # List comprehension to filter out stopwords (case-insensitive)
    filtered_tokens = [w for w in words if w.lower() not in stopwords_pt]
    print(f"Tokens após remoção de stopwords: {filtered_tokens}")
    return deque(filtered_tokens)

# --- Examplos para fins de testes ---
sentence_ok = 'Olá, eu estou criando um analisador léxico para o trabalho de compiladores!'
sentence_with_invalid = 'Processo © concluído! ✅ Vamos testar...'

print("\n--- Executando Exemplo 1 (OK) ---")
result_deque1 = lexical_check(sentence_ok)


print(f"Resultado Final (Fila de Tokens): {result_deque1}")

print("\n" + "="*40 + "\n") # Separator

print("--- Executando Exemplo 2 (Inválido) ---")
result_deque2 = lexical_check(sentence_with_invalid)
print(f"Resultado Final (Fila de Tokens): {result_deque2}")

# agora preciso preciso implementar a tabela de simbolos, aplicando o stemming e utilizando a funcao de similaridade para verificar se