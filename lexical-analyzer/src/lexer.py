from collections import deque

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def lexical_check(text: str):
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


def process_tokens(text):
    print("Processando tokens...")
    return deque(["EXEMPLO_TOKEN"])

# Teste
if __name__ == "__main__":
    user_input = input("Digite um texto para análise léxica: ")
    lexical_check(user_input)
