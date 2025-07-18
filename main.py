import sys
import json
from collections import deque

# Importa os componentes dos outros módulos
from config import GRAMMAR, NON_TERMINALS_VALIDATORS, GREEN, RED, BLUE, RESET, load_spacy_model
from linguistic_processing import get_tokens_for_parser, update_symbol_table
from syntactic_analyzer import SyntacticAnalyzer

def main_loop():
    """Simula um interpretador de linha de comando usando apenas spaCy."""
    
    # 1. Setup inicial do modelo spaCy
    nlp = load_spacy_model()
    if nlp is None:
        sys.exit(1)

    # 2. Prepara componentes
    parser = SyntacticAnalyzer(GRAMMAR, NON_TERMINALS_VALIDATORS)
    symbol_table = []

    # Extrai palavras-chave da gramática para não serem removidas como stopwords
    grammar_keywords = {
        value.lower()
        for rule in GRAMMAR
        for token_type, value in rule['pattern']
        if token_type == 'KEYWORD'
    }
    print(f"Palavras-chave da gramática (não serão removidas): {sorted(list(grammar_keywords))}")

    print("\nInterpretador de Comandos de Documentos (spaCy). Digite 'sair' para terminar.")
    
    while True:
        user_input = input("> ")
        if user_input.lower() == 'sair':
            break

        # --- PROCESSAMENTO UNIFICADO COM SPACY ---
        
        # 1. Processa o texto UMA VEZ para criar o objeto 'doc'
        doc = nlp(user_input)

        # 2. Obtém a fila de tokens para o analisador sintático
        token_queue = get_tokens_for_parser(doc, grammar_keywords)
        
        # 3. Atualiza a tabela de símbolos (usando o mesmo 'doc')
        update_symbol_table(doc, symbol_table)

        # 4. Executa a Análise Sintática
        ast, message = parser.parse(token_queue)
        
        if ast:
            print(f"{GREEN}--- Análise Sintática OK ---{RESET}")
            print(f"Mensagem: {message}")
            print(f"Árvore Sintática Abstrata (AST) gerada:")
            print(json.dumps(ast, indent=2, ensure_ascii=False))
        else:
            print(f"{RED}--- Erro Sintático ---{RESET}")
            print(f"Mensagem: {message}{RESET}")

if __name__ == "__main__":
    main_loop()