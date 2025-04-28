def lexical_check(text: str):
    letters = "abcçdefghijklmnopqrstuvwxyzABCÇDEFGHIJKLMNOPQRSTUVWXYZáàéíóúêãâôõÁÀÉÍÓÚÊÃÂÔÕ"
    digits = "0123456789"
    punctuation = ".,;:!?()[]{}\"'`´°"
    specials = "@#$%&*-_+=\\/|<>^~\n\t\r "
    valid_chars = set(letters + digits + punctuation + specials)

    errors = []
    for index, char in enumerate(text):
        if char not in valid_chars:
            error_msg = f"❌ Erro léxico: caracter inválido '{char}' (code {ord(char)}) at position {index}"
            errors.append(error_msg)

    if errors:
        print("Lexical analysis found the following errors:")
        for error in errors:
            print(error)
    else:
        print("✅ No lexical errors found.")

# Test
if __name__ == "__main__":
    user_input = input("Enter a text for lexical analysis: ")
    lexical_check(user_input)