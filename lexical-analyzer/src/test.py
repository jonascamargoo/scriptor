from collections import deque
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string # Import string for use in tokenize function example later
import sys # For potentially exiting on critical NLTK errors

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m" # Added for info messages
RESET = "\033[0m"

# --- NLTK Resource Download (Recommended: Run once outside functions) ---
# Encapsulate download attempts for clarity
def download_nltk_resources():
    resources = {'tokenizers/punkt': 'punkt', 'corpora/stopwords': 'stopwords'}
    downloaded_all = True
    for resource_path, resource_name in resources.items():
        try:
            nltk.data.find(resource_path)
            # print(f"NLTK resource '{resource_name}' found.") # Optional confirmation
        except LookupError:
            print(f"{YELLOW}NLTK resource '{resource_name}' not found. Attempting download...{RESET}")
            try:
                nltk.download(resource_name, quiet=True)
                print(f"{GREEN}NLTK resource '{resource_name}' downloaded.{RESET}")
            except Exception as e:
                print(f"{RED}Failed to download NLTK resource '{resource_name}': {e}{RESET}")
                downloaded_all = False
    return downloaded_all

# Attempt downloads at the start
if not download_nltk_resources():
    print(f"{RED}Essential NLTK resources could not be downloaded. Exiting.{RESET}")
    sys.exit(1) # Exit if downloads fail

# --- lexical_check MODIFIED ---
def lexical_check(text: str):
    """
    Checks for invalid characters based on predefined sets, removes them,
    reports removals, and then calls tokenize() on the cleaned string.
    Returns the result of tokenize() (a list of tokens).
    """
    # Definition of valid characters
    letters = "abcçdefghijklmnopqrstuvwxyzABCÇDEFGHIJKLMNOPQRSTUVWXYZáàéíóúêãâôõÁÀÉÍÓÚÊÃÂÔÕ"
    digits = "0123456789"
    punctuation = ".,;:!?()[]{}\"'`´°" # Includes standard punctuation
    whitespace = " \t\n\r" # Explicit whitespace chars
    # Explicitly list allowed special symbols, avoid overly broad definitions
    specials = "@#$%&*-_+=\\/|<>^~" # Example: Removed space/newline duplicates from original

    # Combine into the set of valid characters
    valid_chars = set(letters + digits + punctuation + whitespace + specials)

    removed_info = [] # To store messages about removed characters
    cleaned_chars = [] # To build the string with only valid characters

    print(f"{GREEN}--- Verificação de Caracteres Iniciada ---{RESET}")
    print(f"Texto original: '{text}'")

    # Iterate through original text to clean it and record removals
    for index, char in enumerate(text):
        if char in valid_chars:
            cleaned_chars.append(char)
        else:
            # Character is invalid, record its removal
            removal_msg = (
                f"{YELLOW}Info: Caractere inválido '{char}' (código {ord(char)}) "
                f"na posição original {index} foi removido.{RESET}"
            )
            removed_info.append(removal_msg)

    # Create the final cleaned string
    cleaned_string = "".join(cleaned_chars)

    # Report if any characters were removed
    if removed_info:
        print(f"\n{YELLOW}--- Relatório de Limpeza Léxica ---{RESET}")
        for msg in removed_info:
            print(msg)
        print(f"Texto após limpeza: '{cleaned_string}'")
    else:
        print(f"{GREEN}Nenhum caractere inválido encontrado para remover.{RESET}")

    # --- MODIFIED ACTION ---
    # Instead of conditional return or calling a non-existent function,
    # ALWAYS call the provided 'tokenize' function with the cleaned string.
    print(f"\n{GREEN}Prosseguindo para a tokenização (com remoção de stopwords)...{RESET}")
    return tokenize(cleaned_string) # Call the existing tokenize function

# --- tokenize function (Provided by user, with added error handling) ---
def tokenize(text: str) -> list:
    """
    Tokenizes the text using NLTK and removes Portuguese stopwords.
    Returns a list of tokens (words and potentially punctuation, excluding stopwords).
    """
    if not text:
        print(f"{YELLOW}Info: Texto para tokenizar está vazio.{RESET}")
        return []

    try:
        # Load stopwords inside try block in case resource is missing despite download attempt
        stopwords_pt = set(stopwords.words('portuguese'))
    except LookupError:
         print(f"{RED}Erro fatal: Recurso 'stopwords' do NLTK não encontrado ou corrompido.{RESET}")
         return [] # Return empty list on critical error

    try:
        # Tokenize using NLTK's recommended function
        words = word_tokenize(text, language='portuguese')
    except LookupError:
        print(f"{RED}Erro fatal: Recurso 'punkt' do NLTK não encontrado ou corrompido.{RESET}")
        return [] # Return empty list on critical error

    # List comprehension to filter out stopwords (case-insensitive)
    filtered_tokens = [w for w in words if w.lower() not in stopwords_pt]
    print(f"Tokens após remoção de stopwords: {filtered_tokens}")
    return filtered_tokens


# --- Example Usage ---
sentence_ok = 'Olá, eu estou criando um analisador léxico para o trabalho de compiladores!'
sentence_with_invalid = 'Processo © concluído! ✅ Vamos testar...' # Added more text

print("\n--- Executando Exemplo 1 (OK) ---")
result_list1 = lexical_check(sentence_ok)
print(f"Resultado Final (Lista de Tokens): {result_list1}")

print("\n" + "="*40 + "\n") # Separator

print("--- Executando Exemplo 2 (Inválido) ---")
result_list2 = lexical_check(sentence_with_invalid)
print(f"Resultado Final (Lista de Tokens): {result_list2}")

# agora preciso preciso implementar a tabela de simbolos, utilizando a funcao de similaridade